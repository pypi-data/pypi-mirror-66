import pytest
from pytket.circuit import Circuit
from pytket.backends import StatusEnum
from pytket.backends.aqt import AQTBackend
import os


@pytest.mark.skipif(
    os.getenv("AQT_AUTH") is None,
    reason="requires environment variable AQT_AUTH to be a valid AQT credential",
)
def test_aqt():
    # Run a circuit on the noisy simulator.
    token = os.getenv("AQT_AUTH")
    b = AQTBackend(token, device_name="sim/noise-model-1", label="test 1")
    c = Circuit(4, 4)
    c.H(0)
    c.CX(0, 1)
    c.Rz(0.3, 2)
    c.CSWAP(0, 1, 2)
    c.CRz(0.4, 2, 3)
    c.CY(1, 3)
    c.add_barrier([0, 1])
    c.ZZPhase(0.1, 2, 0)
    c.Tdg(3)
    c.measure_all()
    b.compile_circuit(c)
    n_shots = 10
    b.process_circuits([c], n_shots)
    shots = b.get_shots(c, n_shots, seed=1, timeout=30)
    counts = b.get_counts(c, n_shots)
    assert len(shots) == n_shots
    assert sum(counts.values()) == n_shots


@pytest.mark.skipif(
    os.getenv("AQT_AUTH") is None,
    reason="requires environment variable AQT_AUTH to be a valid AQT credential",
)
def test_bell():
    # On the noiseless simulator, we should always get Bell states here.
    token = os.getenv("AQT_AUTH")
    b = AQTBackend(token, device_name="sim", label="test 2")
    c = Circuit(2, 2)
    c.H(0)
    c.CX(0, 1)
    b.compile_circuit(c)
    n_shots = 10
    b.process_circuits([c], n_shots)
    counts = b.get_counts(c, n_shots, timeout=30)
    assert all(q[0] == q[1] for q in counts)


def test_invalid_cred():
    token = "invalid"
    b = AQTBackend(token, device_name="sim", label="test 3")
    c = Circuit(2, 2).H(0).CX(0, 1)
    b.compile_circuit(c)
    with pytest.raises(RuntimeError) as excinfo:
        b.process_circuits([c], 1)
        assert "Access denied" in str(excinfo.value)


@pytest.mark.skipif(
    os.getenv("AQT_AUTH") is None,
    reason="requires environment variable AQT_AUTH to be a valid AQT credential",
)
def test_invalid_request():
    token = os.getenv("AQT_AUTH")
    b = AQTBackend(token, device_name="sim", label="test 4")
    c = Circuit(2, 2).H(0).CX(0, 1)
    b.compile_circuit(c)
    with pytest.raises(RuntimeError):
        b.process_circuits([c], 1000000)
        assert "1000000" in str(excinfo.value)


@pytest.mark.skipif(
    os.getenv("AQT_AUTH") is None,
    reason="requires environment variable AQT_AUTH to be a valid AQT credential",
)
def test_handles():
    token = os.getenv("AQT_AUTH")
    b = AQTBackend(token, device_name="sim/noise-model-1", label="test 5")
    c = Circuit(2, 2)
    c.H(0)
    c.CX(0, 1)
    b.compile_circuit(c)
    n_shots = 5
    handles = b.process_circuits([c, c], n_shots=n_shots)
    assert len(handles) == 2
    for handle in handles:
        shots = b.get_shots(handle, n_shots=n_shots, timeout=30)
        assert b.circuit_status(handle).status is StatusEnum.COMPLETED
        counts = b.get_counts(handle, n_shots=n_shots)
        assert len(shots) == n_shots
        assert sum(counts.values()) == n_shots


def test_machine_debug():
    b = AQTBackend("invalid", device_name="sim", label="test 6")
    b._MACHINE_DEBUG = True
    c = Circuit(2, 2)
    c.H(0)
    c.CX(0, 1)
    b.compile_circuit(c)
    n_shots = 10
    h = b.process_circuits([c], n_shots)[0]
    counts = b.get_counts(h, n_shots, timeout=30)
    assert counts == {(0, 0): n_shots}
