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
import math
from collections import namedtuple
from shutil import which

import docker
import numpy as np
import pytest

from pytket.backends.forest import ForestBackend, ForestStateBackend
from pytket.circuit import BasisOrder, Circuit, OpType
from pytket.passes import CliffordSimp, PauliSimp
from pytket.predicates import CompilationUnit
from pytket.routing import Architecture, route
from pytket.utils.expectations import (
    _get_operator_expectation_value,
    _get_pauli_expectation_value,
)
from pytket.utils.results import compare_statevectors


@pytest.fixture(scope="module")
def qvm(request):
    print("running qvm container")
    dock = docker.from_env()
    container = dock.containers.run(
        image="rigetti/qvm", command="-S", detach=True, ports={5000: 5000}, remove=True
    )
    # container = dock.containers.run(image="rigetti/qvm", command="-S", detach=True, publish_all_ports=True, remove=True)
    request.addfinalizer(container.stop)
    return None


@pytest.fixture(scope="module")
def quilc(request):
    dock = docker.from_env()
    container = dock.containers.run(
        image="rigetti/quilc",
        command="-S",
        detach=True,
        ports={5555: 5555},
        remove=True,
    )
    request.addfinalizer(container.stop)
    return None


def circuit_gen(measure=False):
    c = Circuit(2, 2)
    c.H(0)
    c.CX(0, 1)
    if measure:
        c.measure_all()
    return c


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_statevector(qvm, quilc):
    c = circuit_gen()
    b = ForestStateBackend()
    state = b.get_state(c)
    assert compare_statevectors(
        state, np.asarray([math.sqrt(0.5), 0, 0, math.sqrt(0.5)])
    )


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
@pytest.mark.filterwarnings("ignore:strict=False")
def test_sim(qvm, quilc):
    c = circuit_gen(True)
    b = ForestBackend("9q-square")
    b.compile_circuit(c)
    shots = b.get_shots(c, 1024)
    print(shots)


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_measures(qvm, quilc):
    n_qbs = 9
    c = Circuit(n_qbs, n_qbs)
    x_qbs = [2, 5, 7, 8]
    for i in x_qbs:
        c.X(i)
    c.measure_all()
    b = ForestBackend("9q-square")
    b.compile_circuit(c)
    shots = b.get_shots(c, 10)
    print(shots)
    all_ones = True
    all_zeros = True
    for i in x_qbs:
        all_ones = all_ones and np.all(shots[:, i])
    for i in range(n_qbs):
        if i not in x_qbs:
            all_zeros = all_zeros and (not np.any(shots[:, i]))
    assert all_ones
    assert all_zeros


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_pauli_statevector(qvm, quilc):
    c = Circuit(2, 2)
    c.Rz(0.5, 0)
    b = ForestStateBackend()
    zi = [(0, "Z")]
    assert _get_pauli_expectation_value(c, zi, b) == 1
    c.X(0)
    assert _get_pauli_expectation_value(c, zi, b) == -1


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_pauli_sim(qvm, quilc):
    c = Circuit(2, 2)
    c.Rz(0.5, 0)
    b = ForestBackend("9q-square")
    zi = [(0, "Z")]
    energy = _get_pauli_expectation_value(c, zi, b, 10)
    assert abs(energy - 1) < 0.001
    c.X(0)
    energy = _get_pauli_expectation_value(c, zi, b, 10)
    assert abs(energy + 1) < 0.001


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_operator_statevector(qvm, quilc):
    c = Circuit(2, 2)
    c.Rz(0.5, 0)
    b = ForestStateBackend()
    zi = ((0, "Z"),)
    iz = ((1, "Z"),)
    op = namedtuple("Operator", "terms")({zi: 0.3, iz: -0.1})
    assert _get_operator_expectation_value(c, op, b) == pytest.approx(0.2)
    c.X(0)
    assert _get_operator_expectation_value(c, op, b) == pytest.approx(-0.4)


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_operator_sim(qvm, quilc):
    c = Circuit(2, 2)
    c.Rz(0.5, 0)
    b = ForestBackend("9q-square")
    zi = ((0, "Z"),)
    iz = ((1, "Z"),)
    op = namedtuple("Operator", "terms")({zi: 0.3, iz: -0.1})
    assert _get_operator_expectation_value(c, op, b, 10) == pytest.approx(
        0.2, rel=0.001
    )
    c.X(0)
    assert _get_operator_expectation_value(c, op, b, 10) == pytest.approx(
        -0.4, rel=0.001
    )


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_counts(qvm, quilc):
    c = circuit_gen(True)
    b = ForestBackend("9q-square")
    b.compile_circuit(c)
    counts = b.get_counts(c, 10)
    assert list(counts.keys()) == [(0, 0), (1, 1)]


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_default_pass():
    b = ForestBackend("9q-square")
    comp_pass = b.default_compilation_pass
    circ = circuit_gen(False)
    cu = CompilationUnit(circ)
    comp_pass.apply(cu)
    c = cu.circuit
    for pred in b.required_predicates:
        assert pred.verify(c)


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_ilo(qvm, quilc):
    b = ForestBackend("9q-square")
    bs = ForestStateBackend()
    c = Circuit()
    nodes = c.add_q_register("node", 2)
    c.CZ(nodes[0], nodes[1])
    c.Rx(1.0, nodes[1])
    assert compare_statevectors(bs.get_state(c), np.asarray([0, 1, 0, 0]))
    assert compare_statevectors(
        bs.get_state(c, basis=BasisOrder.dlo), np.asarray([0, 0, 1, 0])
    )
    c.measure_all()
    assert (b.get_shots(c, 2) == np.asarray([[0, 1], [0, 1]])).all()
    assert (
        b.get_shots(c, 2, basis=BasisOrder.dlo) == np.asarray([[1, 0], [1, 0]])
    ).all()
    assert b.get_counts(c, 2) == {(0, 1): 2}
    assert b.get_counts(c, 2, basis=BasisOrder.dlo) == {(1, 0): 2}


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_swaps():
    # Check that unitaries match even when implicit swaps have been introduced.
    b = ForestStateBackend()
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
    assert np.isclose(np.abs(np.dot(s, s1)), 1)


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_swaps_basisorder():
    # Check that implicit swaps can be corrected irrespective of BasisOrder
    b = ForestStateBackend()
    c = Circuit(4)
    c.X(0)
    c.CX(0, 1)
    c.CX(1, 0)
    CliffordSimp(True).apply(c)
    assert c.n_gates_of_type(OpType.CX) == 1
    s_ilo = b.get_state(c, basis=BasisOrder.ilo)
    s_dlo = b.get_state(c, basis=BasisOrder.dlo)
    correct_ilo = np.zeros((16,))
    correct_ilo[4] = 1.0
    assert compare_statevectors(s_ilo, correct_ilo)
    correct_dlo = np.zeros((16,))
    correct_dlo[2] = 1.0
    assert compare_statevectors(s_dlo, correct_dlo)


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_handle():
    b = ForestBackend("9q-square")
    c0 = Circuit(1)
    c0.measure_all()
    c1 = Circuit(1)
    c1.X(0)
    c1.measure_all()
    b.compile_circuit(c0)
    b.compile_circuit(c1)
    handles = b.process_circuits([c0, c1], 10)
    counts0 = b.get_counts(handles[0])
    counts1 = b.get_counts(handles[1])
    assert counts0 == {(0,): 10}
    assert counts1 == {(1,): 10}


@pytest.mark.skipif(
    which("docker") is None, reason="Can only run Rigetti QVM if docker is installed"
)
def test_state_handle():
    b = ForestStateBackend()
    c0 = Circuit(1)
    c1 = Circuit(1)
    c1.X(0)
    b.compile_circuit(c0)
    b.compile_circuit(c1)
    handles = b.process_circuits([c0, c1], 10)
    state0 = b.get_state(handles[0])
    state1 = b.get_state(handles[1])
    assert compare_statevectors(state0, np.asarray([1.0, 0.0]))
    assert compare_statevectors(state1, np.asarray([0.0, 1.0]))


def test_non_contiguous_architecture():
    b = ForestBackend("Aspen-4-2Q-C")
    c = Circuit(2, 2)
    c.X(0)
    c.measure_all()
    b.compile_circuit(c)
    counts = b.get_counts(c, 10)
    assert counts[(1, 0)] == 10


def test_delay_measures():
    b = ForestBackend("9q-square")
    # No triangles in architecture, so third CX will need a bridge
    # This will happen after the measurement on qubit 1
    c = Circuit(3, 3)
    c.CX(0, 1)
    c.CX(1, 2)
    c.CX(0, 2)
    c.Measure(0, 0)
    c.Measure(1, 1)
    c.Measure(2, 2)
    b.compile_circuit(c)
    assert b.valid_circuit(c)


if __name__ == "__main__":
    test_statevector(None, None)
    test_sim(None, None)
    test_measures(None, None)
    # test_device()
    test_pauli_statevector(None, None)
    test_pauli_sim(None, None)
    test_counts(None, None)
    test_swaps(None, None)
