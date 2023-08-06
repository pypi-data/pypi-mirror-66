import pytest

from socket_says.socket_says import SocketSays


@pytest.fixture()
def test_socket():
    simon = SocketSays('127.0.0.1', 7357)
    yield simon


def test_says(test_socket: SocketSays, capsys):
    errors = None
    try:
        test_socket.says("""Test
        test
        test """)
    except ConnectionRefusedError:
        errors = True
    assert errors is None
    # captured_err = capsys.readouterr()
    # assert captured_err.out == ''


def test_change_address(test_socket: SocketSays):
    assert str(test_socket.address) == '127.0.0.1'
    test_socket.address = '10.10.2.20'
    assert str(test_socket.address) == '10.10.2.20'


def test_change_port(test_socket: SocketSays):
    assert test_socket.port == 7357
    test_socket.port = 80
    assert test_socket.port == 80


@pytest.mark.xfail
def test_bad_changes(test_socket: SocketSays):
    test_socket.address = "192,43:etc"
    test_socket.port = "gatsby"
