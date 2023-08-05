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
from pytket.circuit import Circuit, Pauli, PauliExpBox
from pytket.backends.qsharp import QsharpEstimatorBackend


def test_estimates():
    """
    Check that the resource estimator gives reasonable results.
    """
    b = QsharpEstimatorBackend()
    c = Circuit(3)
    c.H(0)
    c.CX(0, 1)
    c.CCX(0, 1, 2)
    c.Rx(0.3, 1)
    c.Ry(0.4, 2)
    c.Rz(1.1, 0)
    c.S(1)
    c.SWAP(0, 2)
    c.T(1)
    c.X(0)
    c.Y(1)
    c.Z(2)
    pbox = PauliExpBox([Pauli.X, Pauli.I, Pauli.Z], 0.25)
    c.add_pauliexpbox(pbox, [2, 0, 1])
    b.compile_circuit(c)
    resources = b.get_resources(c)
    assert resources["CNOT"] >= 1
    assert resources["QubitClifford"] >= 1
    assert resources["R"] >= 1
    assert resources["T"] >= 1
    assert resources["Depth"] >= 1
    assert resources["Width"] == 3
    assert resources["BorrowedWidth"] == 0


def test_ccx_resources():
    """
    Resources of a CCX.
    """
    b = QsharpEstimatorBackend()
    c = Circuit(3)
    c.CCX(0, 1, 2)
    b.compile_circuit(c)
    resources = b.get_resources(c)
    assert resources["T"] >= 7


def test_handles():
    b = QsharpEstimatorBackend()
    c = Circuit(3)
    c.CCX(0, 1, 2)
    b.compile_circuit(c)
    handle = b.process_circuits([c])[0]
    resources = b.get_resources(handle)
    assert resources["T"] >= 7


if __name__ == "__main__":
    test_estimates()
    test_ccx_resources()
    test_handles()
