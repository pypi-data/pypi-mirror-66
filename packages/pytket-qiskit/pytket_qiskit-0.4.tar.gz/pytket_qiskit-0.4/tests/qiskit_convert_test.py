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
import pytest
import numpy as np
import qiskit
from qiskit import (
    QuantumCircuit,
    QuantumRegister,
    ClassicalRegister,
    execute,
    Aer,
    IBMQ,
    execute,
    transpile,
)
from qiskit.aqua.operators import WeightedPauliOperator
from qiskit.converters import dag_to_circuit, circuit_to_dag
from qiskit.quantum_info import Pauli
from qiskit.transpiler import PassManager

from math import pi
from pytket.circuit import Circuit, CircBox, Unitary2qBox, OpType, Qubit, Bit
from pytket.qiskit import tk_to_qiskit, qiskit_to_tk
from pytket.qiskit.tket_pass import TketPass
from sympy import Symbol
from pytket.passes import USquashIBM, DecomposeBoxes


def get_test_circuit(measure):
    qr = QuantumRegister(4)
    cr = ClassicalRegister(4)
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.cx(qr[1], qr[0])
    qc.h(qr[0])
    qc.cx(qr[0], qr[3])
    qc.barrier(qr[3])
    qc.rx(pi / 2, qr[3])
    qc.z(qr[2])
    if measure:
        qc.measure(qr[0], cr[0])
        qc.measure(qr[1], cr[1])
        qc.measure(qr[2], cr[2])
        qc.measure(qr[3], cr[3])
    return qc


def test_convert():
    qc = get_test_circuit(False)
    backend = Aer.get_backend("statevector_simulator")
    job = execute([qc], backend)
    state0 = job.result().get_statevector(qc)
    tkc = qiskit_to_tk(qc)
    qc = tk_to_qiskit(tkc)
    job = execute([qc], backend)
    state1 = job.result().get_statevector(qc)
    assert np.allclose(state0, state1, atol=1e-10)


def test_symbolic():
    pi2 = Symbol("pi2")
    pi3 = Symbol("pi3")

    tkc = Circuit(3, 3).Ry(pi2, 1).Rx(pi3, 1).CX(1, 0)
    USquashIBM().apply(tkc)

    tkc.symbol_substitution({pi2: pi / 2, pi3: pi / 3})

    backend = Aer.get_backend("statevector_simulator")
    qc = tk_to_qiskit(tkc)
    job = execute([qc], backend)
    state1 = job.result().get_statevector(qc)
    state0 = np.array(
        [
            [
                0.6252345 + 0.0j,
                0.0 + 0.0j,
                0.0 + 0.0j,
                -0.78000172 + 0.02606021j,
                0.0 + 0.0j,
                0.0 + 0.0j,
                0.0 + 0.0j,
                0.0 + 0.0j,
            ]
        ]
    )
    assert np.allclose(state0, state1, atol=1e-10)


def test_measures():
    qc = get_test_circuit(True)
    backend = Aer.get_backend("qasm_simulator")
    job = execute([qc], backend, seed_simulator=7)
    counts0 = job.result().get_counts(qc)
    tkc = qiskit_to_tk(qc)
    qc = tk_to_qiskit(tkc)
    job = execute([qc], backend, seed_simulator=7)
    counts1 = job.result().get_counts(qc)
    for result, count in counts1.items():
        result_str = result.replace(" ", "")
        if counts0[result_str] != count:
            assert False


def test_boxes():
    c = Circuit(2)
    c.S(0)
    c.H(1)
    c.CX(0, 1)
    cbox = CircBox(c)
    d = Circuit(3)
    d.add_circbox(cbox, [0, 1])
    d.add_circbox(cbox, [1, 2])
    u = np.asarray([[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0]])
    ubox = Unitary2qBox(u)
    d.add_unitary2qbox(ubox, 0, 1)
    qsc = tk_to_qiskit(d)
    d1 = qiskit_to_tk(qsc)
    assert len(d1.get_commands()) == 3
    DecomposeBoxes().apply(d)
    DecomposeBoxes().apply(d1)
    assert d == d1


def test_Unitary2qBox():
    c = Circuit(2)
    u = np.asarray([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    ubox = Unitary2qBox(u)
    c.add_unitary2qbox(ubox, 0, 1)
    # Convert to qiskit
    qc = tk_to_qiskit(c)
    # Verify that unitary from simulator is correct
    back = Aer.get_backend("unitary_simulator")
    job = execute(qc, back).result()
    a = job.get_unitary(qc)
    assert np.allclose(a, u)


def test_tketpass():
    backends = [
        Aer.get_backend("statevector_simulator"),
        Aer.get_backend("qasm_simulator"),
        Aer.get_backend("unitary_simulator"),
    ]
    if IBMQ.stored_account():
        if not IBMQ.active_account():
            IBMQ.load_account()
        provider = IBMQ.providers()[0]
        backends.append(provider.get_backend("ibmq_essex"))
    for back in backends:
        tkpass = TketPass(back)
        qc = get_test_circuit(True)
        pm = PassManager(passes=tkpass)
        output = transpile(qc, pass_manager=pm)


def test_instruction():
    # TKET-446
    qreg = QuantumRegister(3)
    paulis = list(map(Pauli.from_label, ["XXI", "YYI", "ZZZ"]))
    weights = [0.3, 0.5 + 1j * 0.2, -0.4]
    op = WeightedPauliOperator.from_list(paulis, weights)
    evolution_circ = op.evolve(None, 1.2, num_time_slices=1, quantum_registers=qreg)
    tk_circ = qiskit_to_tk(evolution_circ)
    cmds = tk_circ.get_commands()
    assert len(cmds) == 1
    assert cmds[0].op.type == OpType.CircBox


def test_conditions():
    box_c = Circuit(2, 2)
    box_c.Z(0)
    box_c.Y(1, condition_bits=[0, 1], condition_value=1)
    box_c.Measure(0, 0, condition_bits=[0, 1], condition_value=0)
    box = CircBox(box_c)

    u = np.asarray([[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0]])
    ubox = Unitary2qBox(u)

    c = Circuit(2, 2)
    b = c.add_c_register("b", 1)
    c.add_circbox(
        box,
        [Qubit(0), Qubit(1), Bit(0), Bit(1)],
        condition_bits=[b[0]],
        condition_value=1,
    )
    c.add_unitary2qbox(
        ubox, Qubit(0), Qubit(1), condition_bits=[b[0]], condition_value=0
    )

    qc = tk_to_qiskit(c)
    c1 = qiskit_to_tk(qc)
    assert len(c1.get_commands()) == 2
    DecomposeBoxes().apply(c)
    DecomposeBoxes().apply(c1)
    assert c == c1


def test_condition_errors():
    with pytest.raises(Exception) as errorinfo:
        c = Circuit(2, 2)
        c.X(0, condition_bits=[0], condition_value=1)
        tk_to_qiskit(c)
    assert "OpenQASM conditions must be an entire register" in str(errorinfo.value)
    with pytest.raises(Exception) as errorinfo:
        c = Circuit(2, 2)
        b = c.add_c_register("b", 2)
        c.X(Qubit(0), condition_bits=[b[0], Bit(0)], condition_value=1)
        tk_to_qiskit(c)
    assert "OpenQASM conditions can only use a single register" in str(errorinfo.value)
    with pytest.raises(Exception) as errorinfo:
        c = Circuit(2, 2)
        c.X(0, condition_bits=[1, 0], condition_value=1)
        tk_to_qiskit(c)
    assert "OpenQASM conditions must be an entire register in order" in str(
        errorinfo.value
    )


if __name__ == "__main__":
    test_convert()
    test_measures()
    test_boxes()
    test_Unitary2qBox()
    test_tketpass()
    test_symbolic()
    test_instruction()
