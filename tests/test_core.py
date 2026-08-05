from src.main import calculate_uptime, check_target_availability, load_json_file


def test_calculate_uptime_all_online():
    history = [{"is_online": True}, {"is_online": True}]
    assert calculate_uptime(history) == 100.0


def test_calculate_uptime_partial():
    history = [{"is_online": True}, {"is_online": False}]
    assert calculate_uptime(history) == 50.0


def test_calculate_uptime_empty_history():
    assert calculate_uptime([]) == 0.0


def test_load_json_file_non_existent(tmp_path):
    fake_file = tmp_path / "non_existent.json"
    result = load_json_file(str(fake_file), dict)
    assert result == {}


def test_check_target_availability_failure():
    is_online, latency = check_target_availability("127.0.0.1", 1, timeout=0.1)
    assert is_online is False
    assert latency == 0.0
