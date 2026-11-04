
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate

def qft_rot(k, inverse=False, cutoff=None):
    qc = QuantumCircuit(k, name="QFT" if not inverse else "IQFT")
    if not inverse:
        for j in range(k-1, -1, -1):
            qc.h(j)
            for m in range(j):
                ang = math.pi / 2**(j-m)
                if cutoff is not None and abs(ang) < 2*math.pi/2**cutoff: continue
                qc.cp(ang, m, j)
    else:
        for j in range(k):
            for m in range(j):
                ang = -math.pi / 2**(j-m)
                if cutoff is not None and abs(ang) < 2*math.pi/2**cutoff: continue
                qc.cp(ang, m, j)
            qc.h(j)
    return qc

def qft_add_const(k, x, cutoff=None):
    qc = QuantumCircuit(k, name=f"ADD{x}")
    qc.compose(qft_rot(k, cutoff=cutoff), inplace=True); qc.barrier()
    for j in range(k):
        ang = (2*math.pi * x / 2**(j+1)) % (2*math.pi)
        if cutoff is not None and min(ang, 2*math.pi-ang) < 2*math.pi/2**cutoff: continue
        if abs(ang) > 1e-15: qc.p(ang, j)
    qc.barrier()
    qc.compose(qft_rot(k, inverse=True, cutoff=cutoff), inplace=True)
    return qc

def qft_sub_controlled(k, kB, cutoff=None):
    qc = QuantumCircuit(2*k, name="CSUB")
    qc.compose(qft_rot(kB, cutoff=cutoff), qubits=range(k, 2*k), inplace=True); qc.barrier()
    for t in range(k):
        for j in range(kB):
            ang = (-2*math.pi * (2**t) / 2**(j+1)) % (2*math.pi)
            if cutoff is not None and min(ang, 2*math.pi-ang) < 2*math.pi/2**cutoff: continue
            if abs(ang) > 1e-15: qc.cp(ang, t, k+j)
    qc.barrier()
    qc.compose(qft_rot(kB, inverse=True, cutoff=cutoff), qubits=range(k, 2*k), inplace=True)
    return qc

def zpow(k, x2):
    n = 2**k
    qc = QuantumCircuit(k, name=f"Z{x2}")
    for j in range(k):
        ang = (2*math.pi * x2 * (2**j) / n) % (2*math.pi)
        if abs(ang) > 1e-15: qc.p(ang, j)
    return qc

def build_protocol(k, x1, x2, cutoff=None):
    qc = QuantumCircuit(2*k, 2*k, name=f"QRACv3_d{2**k}_x{x1}_{x2}")
    for j in range(k):
        qc.h(j); qc.cx(j, k+j)
    qc.barrier()
    qc.compose(zpow(k, x2), qubits=range(k), inplace=True)
    qc.barrier()
    qc.compose(qft_add_const(k, x1, cutoff), qubits=range(k), inplace=True)
    qc.barrier()
    qc.compose(qft_sub_controlled(k, k, cutoff), inplace=True)
    qc.barrier()
    qc.append(QFTGate(k).inverse(), range(k))
    qc.measure(range(2*k), range(2*k))
    return qc

def build_cal(k):
    cal0 = QuantumCircuit(2*k, 2*k, name="CAL0"); cal0.measure(range(2*k), range(2*k))
    cal1 = QuantumCircuit(2*k, 2*k, name="CAL1"); cal1.x(range(2*k)); cal1.measure(range(2*k), range(2*k))
    return cal0, cal1
