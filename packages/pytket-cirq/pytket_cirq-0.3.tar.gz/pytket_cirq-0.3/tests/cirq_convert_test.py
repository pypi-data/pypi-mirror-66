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

from pytket.cirq import cirq_to_tk, tk_to_cirq, process_device
from pytket.routing import SquareGrid

import cirq
import pytest
import numpy as np
from sympy import pi

from cirq.value import Duration
from cirq.google import XmonDevice, Foxtail
from cirq.circuits import InsertStrategy


def get_circuit():
    PI = float(pi.evalf())
    qubits = [cirq.LineQubit(i) for i in range(9)]

    g = cirq.CZPowGate(exponent=0.1)
    circ = cirq.Circuit.from_ops(
        cirq.H(qubits[0]),
        cirq.X(qubits[1]),
        cirq.Y(qubits[2]),
        cirq.Z(qubits[3]),
        cirq.T(qubits[3]),
        cirq.S(qubits[4]),
        cirq.CNOT(qubits[1], qubits[4]),
        # cirq.SWAP(qubits[1], qubits[6]),
        cirq.CNOT(qubits[6], qubits[8]),
        cirq.Rx(rads=0.1 * PI)(qubits[5]),
        cirq.Ry(rads=0.1 * PI)(qubits[6]),
        cirq.Rz(rads=0.1 * PI)(qubits[7]),
        g(qubits[2], qubits[3]),
        cirq.CZ(qubits[2], qubits[3]),
        cirq.ISWAP(qubits[4], qubits[5]),
        cirq.measure_each(*qubits[3:-2]),
    )
    return circ


def get_match_circuit():
    qubits = [cirq.LineQubit(i) for i in range(9)]

    g = cirq.CZPowGate(exponent=0.1)
    zz = cirq.ZZPowGate(exponent=0.3)
    px = cirq.PhasedXPowGate(phase_exponent=0.6, exponent=0.2)
    circ = cirq.Circuit.from_ops(
        (
            cirq.H(qubits[0]),
            cirq.X(qubits[1]),
            cirq.Y(qubits[2]),
            cirq.Z(qubits[3]),
            cirq.S(qubits[4]),
            cirq.CNOT(qubits[1], qubits[4]),
            cirq.T(qubits[3]),
            cirq.CNOT(qubits[6], qubits[8]),
            # cirq.Rx(rads=0.1*PI)(qubits[5]),
            # cirq.Ry(rads=0.1*PI)(qubits[6]),
            # cirq.Rz(rads=0.1*PI)(qubits[7]),
            # (cirq.X**0.1)(qubits[5]),
            # (cirq.Y**0.1)(qubits[6]),
            # (cirq.Z**0.1)(qubits[7]),
            cirq.XPowGate(exponent=0.1)(qubits[5]),
            cirq.YPowGate(exponent=0.1)(qubits[6]),
            cirq.ZPowGate(exponent=0.1)(qubits[7]),
            g(qubits[2], qubits[3]),
            zz(qubits[3], qubits[4]),
            px(qubits[6]),
            cirq.measure_each(*qubits[3:-2]),
        ),
        strategy=InsertStrategy.EARLIEST,
    )
    return circ


def test_conversions():

    arc = SquareGrid(3, 3)
    qubits = [cirq.LineQubit(i) for i in range(9)]
    device = XmonDevice(
        Duration(nanos=0), Duration(nanos=0), Duration(nanos=0), qubits=qubits
    )
    circ = get_match_circuit()
    coms = cirq_to_tk(circ)
    print(str(circ))
    print(str(tk_to_cirq(coms)))
    assert str(circ) == str(tk_to_cirq(coms))
    tk_to_cirq(cirq_to_tk(get_circuit()))


def test_device():
    fox = Foxtail
    dev = process_device(fox)
    arc = dev.architecture
    # print(str(arc))
    assert str(arc) == "<tket::Architecture, nodes=22>"


if __name__ == "__main__":
    test_conversions()
    test_device()
