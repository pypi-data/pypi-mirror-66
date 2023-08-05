# Copyright 2019-2020 Cambridge Quantum Computing
#
# Licensed under a Non-Commercial Use Software Licence (the "Licence");
# you may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence, but note it is strictly for non-commercial use.
from typing import TYPE_CHECKING, Dict, Iterable, Optional, Tuple

import numpy as np
from pytket.circuit import Circuit, Pauli
from pytket.measurement import PauliPartitionStrat, measurement_reduction
from pytket._simulation import operator_matrix, pauli_tensor_matrix
from pytket.predicates import CompilationUnit

from .measurements import _all_pauli_measurements, append_pauli_measurement
from .results import KwargTypes
from .operators import (
    _get_coeff_from_qubit_operator,
    _qubit_operator_to_qubit_pauli_tensor_list,
)

if TYPE_CHECKING:
    from pytket.backends.backend import Backend


def expectation_from_shots(shot_table: np.ndarray) -> float:
    """Estimates the expectation value of a circuit from its shots.
    Computes the parity of '1's across all bits to determine a +1 or -1 contribution from each row, and returns the average.

    :param shot_table: The table of shots to interpret.
    :type shot_table: np.ndarray
    :return: The expectation value in the range [-1, 1].
    :rtype: float
    """
    aritysum = 0.0
    for row in shot_table:
        aritysum += np.sum(row) % 2
    return -2 * aritysum / len(shot_table) + 1


def expectation_from_counts(counts: Dict[Tuple[int, ...], int]) -> float:
    """Estimates the expectation value of a circuit from shot counts.
    Computes the parity of '1's across all bits to determine a +1 or -1 contribution from each readout, and returns the weighted average.

    :param counts: Counts of each measurement outcome observed.
    :type counts: Dict[Tuple[int, ...], int]
    :return: The expectation value in the range [-1, 1].
    :rtype: float
    """
    aritysum = 0.0
    total_shots = 0
    for row, count in counts.items():
        aritysum += count * (np.sum(row) % 2)
        total_shots += count
    return -2 * aritysum / total_shots + 1


def _get_pauli_expectation_value(
    state_circuit: Circuit,
    pauli: Iterable[Tuple[int, str]],
    backend: "Backend",
    n_shots: Optional[int] = None,
) -> complex:
    """Estimates the expectation value of the given circuit with respect to the Pauli term by preparing measurements in the appropriate basis, running on the backend and interpreting the counts/statevector

    :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
    :type state_circuit: Circuit
    :param pauli: Sparse Pauli operator :math:`P` [p1, p2, p3, ...] where each pi = (q, s) with qubit index q and Pauli s ("I", "X", "Y", "Z").
    :type pauli: Iterable[Tuple[int,str]]
    :param backend: pytket backend to run circuit on.
    :type backend: Backend
    :param n_shots: Number of shots to run if backend supports shots/counts. Set to None to calculate using statevector if supported by the backend. Defaults to None
    :type n_shots: Optional[int], optional
    :return: :math:`\\left<\\psi | P | \\psi \\right>`
    :rtype: float
    """
    if not pauli:
        return 1
    if not n_shots:
        if backend.supports_expectation:
            return backend.get_pauli_expectation_value(state_circuit, pauli)
        state = backend.get_state(state_circuit)
        op = pauli_tensor_matrix(pauli, state_circuit.n_qubits)
        return np.vdot(state, op.dot(state))
    measured_circ = state_circuit.copy()
    append_pauli_measurement(pauli, measured_circ)
    backend.compile_circuit(measured_circ)
    if backend.supports_counts:
        counts = backend.get_counts(measured_circ, n_shots)
        return expectation_from_counts(counts)
    elif backend.supports_shots:
        shot_table = backend.get_shots(measured_circ, n_shots)
        return expectation_from_shots(shot_table)
    else:
        raise ValueError("Backend does not support counts or shots")


def _get_operator_expectation_value(
    state_circuit: Circuit,
    operator: "QubitOperator",
    backend: "Backend",
    n_shots: Optional[int] = None,
    partition_strat: Optional[PauliPartitionStrat] = None,
    **kwargs: KwargTypes,
) -> complex:
    """Estimates the expectation value of the given circuit with respect to the operator based on its individual Pauli terms.
    The input circuit must belong to the default qubit register and have contiguous qubit ordering.

    :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`
    :type state_circuit: Circuit
    :param operator: Operator :math:`H`.
    :type operator: openfermion.QubitOperator
    :param backend: pytket backend to run circuit on.
    :type backend: Backend
    :param n_shots: Number of shots to run if backend supports shots/counts. None will force the backend to give the full state if available. Defaults to None
    :type n_shots: Optional[int], optional
    :param partition_strat: If retrieving shots, can perform measurement reduction using a chosen strategy
    :type partition_strat: Optional[PauliPartitionStrat], optional
    :return: :math:`\\left<\\psi | H | \\psi \\right>`
    :rtype: complex
    """
    # TODO use submit-retrieve with handles
    if not n_shots:
        if backend.supports_expectation:
            return backend.get_operator_expectation_value(state_circuit, operator)
        state = backend.get_state(state_circuit)
        terms = [(list(p), c) for p, c in operator.terms.items()]
        op = operator_matrix(terms, state_circuit.n_qubits)
        return np.vdot(state, op.dot(state))
    energy: complex
    if () in operator.terms:
        energy = operator.terms[()]
    else:
        energy = 0
    if not partition_strat:
        coeffs = [c for p, c in operator.terms.items() if p]
        pauli_circuits = list(_all_pauli_measurements(operator, state_circuit))
        for c in pauli_circuits:
            backend.compile_circuit(c)
        if backend.supports_counts:
            for circ, coeff in zip(pauli_circuits, coeffs):
                counts = backend.get_counts(circ, n_shots, **kwargs)
                energy += coeff * expectation_from_counts(counts)
            return energy
        elif backend.supports_shots:
            for circ, coeff in zip(pauli_circuits, coeffs):
                shots = backend.get_shots(circ, n_shots, **kwargs)
                energy += coeff * expectation_from_shots(shots)
            return energy
        else:
            raise ValueError("Backend does not support counts or shots")
    else:
        qp_list_list = _qubit_operator_to_qubit_pauli_tensor_list(operator)
        measurement_expectation = measurement_reduction(qp_list_list, partition_strat)
        # note: this implementation requires storing all the results
        # in memory simultaneously to filter through them.
        list_results = list()
        for pauli_circ in measurement_expectation.measurement_circs:
            circ = state_circuit.copy()
            circ.append(pauli_circ)
            backend.compile_circuit(circ)
            if backend.supports_counts:
                counts = backend.get_counts(circ, n_shots, **kwargs)
                list_results.append(counts)
            elif backend.supports_shots:
                shots = backend.get_shots(circ, n_shots, **kwargs)
                list_results.append(shots)
            else:
                raise ValueError("Backend does not support counts or shots")

        for pauli_map in measurement_expectation.results:
            bitmaps = measurement_expectation.results[pauli_map]
            coeff = _get_coeff_from_qubit_operator(operator, pauli_map)
            for bm in bitmaps:
                index = bm.circ_index
                result_table = list_results[index]
                aritysum = 0.0
                if backend.supports_counts:
                    total_shots = 0
                    for row, count in result_table.items():
                        aritysum += count * (np.sum([row[i] for i in bm.bits]) % 2)
                        total_shots += count
                    e = ((-1) ** bm.invert) * coeff * (-2 * aritysum / total_shots + 1)
                    energy += e
                elif backend.supports_shots:
                    for row in result_table:
                        aritysum += np.sum([row[i] for i in bm.bits]) % 2
                    e = (
                        ((-1) ** bm.invert)
                        * coeff
                        * (-2 * aritysum / len(result_table) + 1)
                    )
                    energy += e
                else:
                    raise ValueError("Backend does not support counts or shots")
        return energy
