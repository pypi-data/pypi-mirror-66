
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import mvm_control as ctrl


def create_mock_serial():
    serial = Mock()
    serial.write.return_value = True
    serial.read_until.return_value = b"valore=OK"
    return serial


def test_parse_response():
    serial = Mock()
    serial.read_until.return_value = b"valore=OK\r\n"
    assert ctrl._parse_response(serial) == "OK"

    serial.read_until.return_value = b"valore=0\r\n"
    assert ctrl._parse_response(serial) == "0"

    serial.read_until.return_value = b"valare=OK\r\n"
    assert ctrl._parse_response(serial) is False


def test_set_mvm_param():
    serial = create_mock_serial()
    assert ctrl.set_mvm_param(serial, "mode", "1") is True
