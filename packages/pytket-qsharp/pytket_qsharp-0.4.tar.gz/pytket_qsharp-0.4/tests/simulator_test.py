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
from pytket.backends.qsharp import QsharpSimulatorBackend


def test_bell():
    """
    Simulate a circuit that generates a Bell state, and check that the results
    are all (0,0) or (1,1).
    """
    b = QsharpSimulatorBackend()
    c = Circuit(2)
    c.H(0)
    c.CX(0, 1)
    b.compile_circuit(c)
    n_shots = 10
    counts = b.get_counts(c, n_shots)
    assert all(m[0] == m[1] for m in counts.keys())
    assert sum(counts.values()) == n_shots


def test_rotations():
    """
    Check that Rz(0.5) acts as the identity.
    """
    b = QsharpSimulatorBackend()
    c = Circuit(1)
    c.Rz(0.5, 0)
    b.compile_circuit(c)
    n_shots = 10
    shots = b.get_shots(c, n_shots)
    assert all(shots[i, 0] == 0 for i in range(n_shots))


def test_rebase():
    """
    Check that we can compile from a circuit containing non-Q# gates.
    """
    b = QsharpSimulatorBackend()
    c = Circuit(2)
    c.CY(0, 1)
    b.compile_circuit(c)


def test_cnx():
    """
    Simulate a CnX gate.
    """
    b = QsharpSimulatorBackend()
    c = Circuit(4)
    c.X(0).X(1).X(2)
    c.add_gate(OpType.CnX, [0, 1, 2, 3])
    b.compile_circuit(c)
    n_shots = 3
    shots = b.get_shots(c, n_shots)
    assert all(shots[i, 3] == 1 for i in range(n_shots))


def test_handles():
    b = QsharpSimulatorBackend()
    c = Circuit(4)
    c.X(0).X(1).X(2)
    c.add_gate(OpType.CnX, [0, 1, 2, 3])
    b.compile_circuit(c)
    n_shots = 3
    handle = b.process_circuits([c], n_shots=n_shots)[0]
    shots = b.get_shots(handle, n_shots)
    assert all(shots[i, 3] == 1 for i in range(n_shots))


if __name__ == "__main__":
    test_bell()
    test_rotations()
    test_rebase()
    test_cnx()
    test_handles()
