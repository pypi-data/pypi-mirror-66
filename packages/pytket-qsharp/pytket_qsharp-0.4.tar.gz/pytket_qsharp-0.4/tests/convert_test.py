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
from pytket.circuit import Circuit, Pauli, PauliExpBox, fresh_symbol
from pytket.qsharp import tk_to_qsharp
from sympy import Symbol

def test_convert():
    c = Circuit(3)
    c.H(0)
    c.H(1)
    c.CX(1, 0)
    c.X(1)
    pbox = PauliExpBox([Pauli.X, Pauli.Z, Pauli.X], 0.25)
    c.add_pauliexpbox(pbox, [2,0,1])
    qs = tk_to_qsharp(c)
    assert('H(q[1]);' in qs)

def test_convert_symbolic():
    c = Circuit(2)
    alpha = Symbol("alpha")
    c.Rx(alpha, 0)
    beta = fresh_symbol("alpha")
    c.Rz(beta*2, 1)
    with pytest.raises(RuntimeError):
        qs = tk_to_qsharp(c)
    s_map = {alpha : 0.5, beta : 3.2}
    c.symbol_substitution(s_map)
    qs = tk_to_qsharp(c)
    assert('Rx' in qs)

if __name__ == '__main__':
    test_convert()
    test_convert_symbolic()
