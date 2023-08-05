import numpy as np
import pytest
from pytket.circuit import Circuit, Qubit, Bit
from pytket.backends.honeywell import HoneywellBackend
from pytket.backends.honeywell.honeywell import _DEBUG_HANDLE_PREFIX, _convert_result
from pytket.backends.status import StatusEnum
import os


def test_honeywell():
    # Run a circuit on the noisy simulator.
    token = os.getenv("HQS_AUTH")
    backend = HoneywellBackend(token, device_name="HQS-LT-1.0-APIVAL", label="test 1")
    if token is None:
        backend._MACHINE_DEBUG = True
    c = Circuit(4, 4)
    c.H(0)
    c.CX(0, 1)
    c.Rz(0.3, 2)
    c.CSWAP(0, 1, 2)
    c.CRz(0.4, 2, 3)
    c.CY(1, 3)
    c.ZZPhase(0.1, 2, 0)
    c.Tdg(3)
    c.measure_all()
    backend.compile_circuit(c)
    n_shots = 4
    handle = backend.process_circuits([c], n_shots)[0]
    if token:
        assert isinstance(handle[0], str)
    else:
        assert handle[0].startswith(_DEBUG_HANDLE_PREFIX)

    correct_shots = np.zeros((4, 4))
    correct_counts = {(0, 0, 0, 0): 4}
    shots = backend.get_shots(handle, timeout=49)
    counts = backend.get_counts(handle)
    assert backend.circuit_status(handle).status is StatusEnum.COMPLETED
    assert np.all(shots == correct_shots)
    assert counts == correct_counts
    newshots = backend.get_shots(c, 4, timeout=49)
    assert np.all(newshots == correct_shots)
    newcounts = backend.get_counts(c, 4)
    assert newcounts == correct_counts


@pytest.mark.skipif(
    os.getenv("HQS_AUTH") is None,
    reason="requires environment variable HQS_AUTH to be a valid Honeywell credential",
)
def test_bell():
    # On the noiseless simulator, we should always get Bell states here.
    token = os.getenv("HQS_AUTH")
    b = HoneywellBackend(token, device_name="HQS-LT-1.0-APIVAL", label="test 2")
    c = Circuit(2, 2)
    c.H(0)
    c.CX(0, 1)
    b.compile_circuit(c)
    n_shots = 10
    handle = b.process_circuits([c], n_shots)[0]
    counts = b.get_shots(handle)
    print(counts)
    assert all(q[0] == q[1] for q in counts)


@pytest.mark.skipif(
    os.getenv("HQS_AUTH") is None,
    reason="requires environment variable HQS_AUTH to be a valid Honeywell credential",
)
def test_multireg():
    token = os.getenv("HQS_AUTH")
    b = HoneywellBackend(token, device_name="HQS-LT-1.0-APIVAL", label="test 2")
    c = Circuit()
    q1 = Qubit("q1", 0)
    q2 = Qubit("q2", 0)
    c1 = Bit("c1", 0)
    c2 = Bit("c2", 0)
    for q in (q1, q2):
        c.add_qubit(q)
    for cb in (c1, c2):
        c.add_bit(cb)
    c.H(q1)
    c.CX(q1, q2)
    c.Measure(q1, c1)
    c.Measure(q2, c2)
    b.compile_circuit(c)

    n_shots = 10
    handle = b.process_circuits([c], n_shots)[0]
    shots = b.get_shots(handle)
    assert np.array_equal(shots, np.zeros((10, 2)))


if __name__ == "__main__":
    test_honeywell()
