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

# This test is adapted primarily from https://github.com/ProjectQ-Framework/ProjectQ/blob/develop/examples/variational_quantum_eigensolver.ipynb

import math
import warnings

import numpy as np
import projectq
import pytest
from openfermion import QubitOperator
from pytket.backends.backend_exceptions import CircuitNotRunError
from pytket.backends.status import StatusEnum
from pytket.backends.projectq import ProjectQBackend
from pytket.backends.resulthandle import ResultHandle
from pytket.circuit import BasisOrder, Circuit
from pytket.passes import PauliSimp
from pytket.predicates import CompilationUnit
from pytket.utils.results import compare_statevectors
from pytket.utils.expectations import (
    _get_operator_expectation_value,
    _get_pauli_expectation_value,
)

warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


# TODO add tests for `get_operator_expectation_value`


def circuit_gen(measure=False):
    c = Circuit(2)
    c.H(0)
    c.CX(0, 1)
    return c


@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
def test_statevector():
    c = circuit_gen()
    b = ProjectQBackend()
    state = b.get_state(c)
    assert np.allclose(state, [math.sqrt(0.5), 0, 0, math.sqrt(0.5)], atol=1e-10)


@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.filterwarnings("ignore:Casting complex values")
def test_pauli():
    c = Circuit(2)
    c.Rz(0.5, 0)
    b = ProjectQBackend()
    zi = [(0, "Z")]
    assert math.isclose(_get_pauli_expectation_value(c, zi, b), 1)
    c.X(0)
    assert math.isclose(_get_pauli_expectation_value(c, zi, b), -1)


@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.filterwarnings(
    "ignore:Casting complex values to real discards the imaginary part"
)
def test_operator():
    c = circuit_gen()
    b = ProjectQBackend()
    zz = QubitOperator("Z0 Z1", 1.0)
    assert math.isclose(_get_operator_expectation_value(c, zz, b), 1.0)
    c.X(0)
    assert math.isclose(_get_operator_expectation_value(c, zz, b), -1.0)


@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
def test_default_pass():
    b = ProjectQBackend()
    comp_pass = b.default_compilation_pass
    circ = circuit_gen(False)
    cu = CompilationUnit(circ)
    comp_pass.apply(cu)
    c = cu.circuit
    for pred in b.required_predicates:
        assert pred.verify(c)
    assert b.valid_circuit(c)


@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
def test_ilo():
    b = ProjectQBackend()
    c = Circuit(2)
    c.X(1)
    assert compare_statevectors(
        b.get_state(c), np.asarray([0, 1, 0, 0], dtype=np.complex)
    )
    assert compare_statevectors(
        b.get_state(c, basis=BasisOrder.dlo), np.asarray([0, 0, 1, 0], dtype=np.complex)
    )


@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
def test_swaps():
    # Check that unitaries match even when implicit swaps have been introduced.
    b = ProjectQBackend()
    c = Circuit(2)
    c.CX(0, 1)
    c.Ry(0.1, 1)
    cu = CompilationUnit(c)
    PauliSimp().apply(cu)
    c1 = cu.circuit
    b.compile_circuit(c)
    b.compile_circuit(c1)
    s = b.get_state(c)
    s1 = b.get_state(c1)
    assert compare_statevectors(s, s1)


@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
def test_resulthandle():
    c = Circuit(4, 4).H(0).CX(0, 2).measure_all()

    b = ProjectQBackend()

    handles = b.process_circuits([c, c.copy()], n_shots=100, seed=10)

    ids = [han[0] for han in handles]

    assert all(isinstance(idval, str) for idval in ids)
    assert ids[0] != ids[1]
    assert len(b.get_state(handles[0])) == (1 << 4)
    assert b.circuit_status(handles[1]).status == StatusEnum.COMPLETED
    with pytest.raises(TypeError) as errorinfo:
        sh = b.get_state(ResultHandle("43", 5))
    assert "ResultHandle('43', 5) does not match expected identifier types" in str(
        errorinfo.value
    )

    wronghandle = ResultHandle("asdf")

    with pytest.raises(CircuitNotRunError) as errorinfo:
        sh = b.get_state(wronghandle)
    assert "Circuit corresponding to {0!r} has not been run by this backend instance.".format(
        wronghandle
    ) in str(
        errorinfo.value
    )


if __name__ == "__main__":
    test_statevector()
    test_swaps()
    test_resulthandle()
