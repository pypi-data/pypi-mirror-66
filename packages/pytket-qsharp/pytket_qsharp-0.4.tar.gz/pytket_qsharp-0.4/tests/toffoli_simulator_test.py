# Copyright 2020 Cambridge Quantum Computing
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

import pytest
from pytket.circuit import Circuit, OpType
from pytket.backends.qsharp import QsharpToffoliSimulatorBackend


def test_incrementer():
    """
    Simulate an 8-bit incrementer
    """
    b = QsharpToffoliSimulatorBackend()
    c = Circuit(8)
    c.add_gate(OpType.CnX, [0, 1, 2, 3, 4, 5, 6, 7])
    c.add_gate(OpType.CnX, [0, 1, 2, 3, 4, 5, 6])
    c.add_gate(OpType.CnX, [0, 1, 2, 3, 4, 5])
    c.add_gate(OpType.CnX, [0, 1, 2, 3, 4])
    c.add_gate(OpType.CnX, [0, 1, 2, 3])
    c.CCX(0, 1, 2)
    c.CX(0, 1)
    c.X(0)

    for x in [0, 23, 79, 198, 255]:  # some arbitrary 8-bit numbers
        circ = Circuit(8)
        # prepare the state corresponding to x
        for i in range(8):
            if (x >> i) % 2 == 1:
                circ.X(i)
        # append the incrementer
        circ.add_circuit(c, list(range(8)))
        # run the simulator
        b.compile_circuit(circ)
        bits = b.get_shots(circ, 1)[0]
        # check the result
        for i in range(8):
            assert bits[i] == ((x + 1) >> i) % 2


def test_compile():
    """
    Compile a circuit containing SWAPs and noops down to CnX's
    """
    b = QsharpToffoliSimulatorBackend()
    c = Circuit(4)
    c.CX(0, 1)
    c.CCX(0, 1, 2)
    c.add_gate(OpType.CnX, [0, 1, 2, 3])
    c.add_gate(OpType.noop, [2])
    c.X(3)
    c.SWAP(1, 2)
    b.compile_circuit(c)
    shots = b.get_shots(c, 2)
    assert all(shots[0] == shots[1])


def test_handles():
    b = QsharpToffoliSimulatorBackend()
    c = Circuit(4)
    c.CX(0, 1)
    c.CCX(0, 1, 2)
    c.add_gate(OpType.CnX, [0, 1, 2, 3])
    c.add_gate(OpType.noop, [2])
    c.X(3)
    c.SWAP(1, 2)
    b.compile_circuit(c)
    n_shots = 2
    handle = b.process_circuits([c], n_shots=n_shots)[0]
    shots = b.get_shots(handle, n_shots)
    assert all(shots[0] == shots[1])


if __name__ == "__main__":
    test_incrementer()
    test_compile()
    test_handles()
