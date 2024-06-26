#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from functools import cached_property
from typing import Optional, Sequence, Tuple

import attrs
import cirq
import numpy as np
from attrs import frozen
from numpy.typing import NDArray

from qualtran import BloqBuilder, BoundedQUInt, QBit, Register, SoquetT
from qualtran.bloqs.for_testing.random_gate import RandomGate
from qualtran.bloqs.qubitization_walk_operator import QubitizationWalkOperator
from qualtran.bloqs.select_and_prepare import PrepareOracle, SelectOracle


@frozen
class RandomPrepareOracle(PrepareOracle):
    U: RandomGate

    @property
    def selection_registers(self) -> tuple[Register, ...]:
        return (Register('selection', BoundedQUInt(bitsize=self.U.bitsize)),)

    @staticmethod
    def create(bitsize: int, *, random_state: np.random.RandomState):
        matrix = RandomGate.create(bitsize, random_state=random_state).matrix
        matrix = np.array(matrix)

        # make the first column (weights alpha_i) all reals
        alpha = matrix[:, 0]
        matrix = matrix * (alpha.conj() / np.abs(alpha))[:, None]

        # verify that it is still unitary
        np.testing.assert_allclose(matrix @ matrix.conj().T, np.eye(2**bitsize), atol=1e-10)
        np.testing.assert_allclose(matrix.conj().T @ matrix, np.eye(2**bitsize), atol=1e-10)

        return RandomPrepareOracle(RandomGate(bitsize, matrix))

    def build_composite_bloq(self, bb: BloqBuilder, selection: SoquetT) -> dict[str, SoquetT]:
        selection = bb.add(self.U, q=selection)
        return {'selection': selection}

    def __pow__(self, power):
        if power == -1:
            return self.U.adjoint()
        return NotImplemented

    @cached_property
    def alphas(self):
        column = np.array(self.U.matrix)[:, 0]
        np.testing.assert_almost_equal(np.imag(column), 0)
        return column**2


@frozen
class PauliSelectOracle(SelectOracle):
    select_bitsize: int
    target_bitsize: int
    select_unitaries: tuple[cirq.DensePauliString, ...]
    control_val: Optional[int] = None

    @staticmethod
    def random(
        select_bitsize: int, target_bitsize: int, *, random_state: np.random.RandomState
    ) -> 'PauliSelectOracle':
        dps = tuple(
            cirq.DensePauliString(random_state.randint(0, 4, size=target_bitsize))
            for _ in range(2**select_bitsize)
        )
        return PauliSelectOracle(select_bitsize, target_bitsize, dps)

    @property
    def control_registers(self) -> Tuple[Register, ...]:
        return () if self.control_val is None else (Register('control', QBit()),)

    @property
    def selection_registers(self) -> Tuple[Register, ...]:
        return (Register('selection', BoundedQUInt(bitsize=self.select_bitsize)),)

    @property
    def target_registers(self) -> Tuple[Register, ...]:
        return (Register('target', BoundedQUInt(bitsize=self.target_bitsize)),)

    def adjoint(self):
        return self

    def __pow__(self, power):
        if abs(power) == 1:
            return self
        return NotImplemented

    def controlled(
        self,
        num_controls: Optional[int] = None,
        control_values=None,
        control_qid_shape: Optional[Tuple[int, ...]] = None,
    ) -> 'cirq.Gate':
        if num_controls is None:
            num_controls = 1
        if control_values is None:
            control_values = [1] * num_controls
        if (
            isinstance(control_values, Sequence)
            and isinstance(control_values[0], int)
            and len(control_values) == 1
            and self.control_val is None
        ):
            return attrs.evolve(self, control_val=control_values[0])
        raise NotImplementedError()

    def decompose_from_registers(
        self,
        *,
        context: cirq.DecompositionContext,
        selection: NDArray[cirq.Qid],
        target: NDArray[cirq.Qid],
        **quregs: NDArray[cirq.Qid],
    ) -> cirq.OP_TREE:
        if self.control_val is not None:
            selection = np.concatenate([selection, quregs['control']])

        for cv, U in enumerate(self.select_unitaries):
            bits = tuple(map(int, bin(cv)[2:].zfill(self.select_bitsize)))[::-1]
            if self.control_val is not None:
                bits = (*bits, self.control_val)
            yield U.on(*target).controlled_by(*selection, control_values=bits)


def random_qubitization_walk_operator(
    select_bitsize: int, target_bitsize: int, *, random_state: np.random.RandomState
) -> tuple[QubitizationWalkOperator, cirq.PauliSum]:
    prepare = RandomPrepareOracle.create(select_bitsize, random_state=random_state)
    select = PauliSelectOracle.random(select_bitsize, target_bitsize, random_state=random_state)

    np.testing.assert_allclose(np.linalg.norm(prepare.alphas, 1), 1)

    ham = cirq.PauliSum.from_pauli_strings(
        [
            dp.on(*cirq.LineQubit.range(target_bitsize)) * alpha
            for dp, alpha in zip(select.select_unitaries, prepare.alphas)
        ]
    )

    return QubitizationWalkOperator(prepare=prepare, select=select), ham
