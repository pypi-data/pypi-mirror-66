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

from typing import Iterable
from pytket.circuit import Qubit, Pauli
from pytket.measurement import QubitPauliTensor


def _qubit_operator_to_qubit_pauli_tensor_list(
    operator: "QubitOperator",
) -> Iterable[QubitPauliTensor]:
    """Converts the tuples in a QubitOperator object to lists of Qubit/Pauli pairs.
    
    :param operator: The operator
    :type operator: openfermion.QubitOperator
    :return: A list of QubitPauliTensors
    :rtype: Iterable[QubitPauliTensor]
    """
    qpt_list = list()
    for pauli_string, _ in operator.terms.items():
        if not pauli_string:
            continue
        qpt = QubitPauliTensor()
        for qb_idx, p in pauli_string:
            qb = Qubit(qb_idx)
            if p == "X":
                pauli = Pauli.X
            elif p == "Y":
                pauli = Pauli.Y
            elif p == "Z":
                pauli = Pauli.Z
            elif p == "I":
                pauli = Pauli.I
            qpt[qb] = pauli
        qpt_list.append(qpt)
    return qpt_list


def _get_coeff_from_qubit_operator(
    operator: "QubitOperator", pauli_map: QubitPauliTensor
) -> complex:
    """Converts a `QubitPauliTensor` object into a tuple to retrieve its coefficient from a `QubitOperator`.
    
    :param operator: The operator
    :type operator: openfermion.QubitOperator
    :param pauli_map: The tensor of Paulis over some Qubits
    :type pauli_map: QubitPauliTensor
    :return: The corresponding coefficient
    :rtype: complex
    """
    paulis = list()
    for qubit, pauli in pauli_map.items():
        i = qubit.index[0]
        if pauli == Pauli.I:
            p = "I"
        elif pauli == Pauli.X:
            p = "X"
        elif pauli == Pauli.Y:
            p = "Y"
        elif pauli == Pauli.Z:
            p = "Z"
        paulis.append((i, p))
    paulis = operator._parse_sequence(paulis)
    coeff = operator.terms[paulis]
    return coeff
