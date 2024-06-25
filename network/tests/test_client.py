import struct
import pytest
import socket
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import send_data
from card import Card

NUM = 4

class MockSocket:
    sent_data = []
    addr = None

    def __init__(self, *args, **kwargs):
        pass

    def connect(self, addr):
        MockSocket.addr = addr

    def sendall(self, data: bytes):
        MockSocket.sent_data.append(data)

    def recv(self, num: int):
        return struct.pack('I', NUM)

    def close(self):
        pass

@pytest.fixture
def mock_socket(monkeypatch):
    mock = MockSocket
    monkeypatch.setattr(socket, 'socket', lambda *args, **kwargs: mock())

def test_run_client(mock_socket):
    send_data("127.0.0.1", "8000", "card", "Eitan", "rrr", "sss", "italy.png")
    assert MockSocket.addr == ("127.0.0.1", '8000')
    card = Card.create_from_path("card", "Eitan", "italy.png",  "rrr", "sss")
    card.image.encrypt(card.solution)
    assert card.serialize() != MockSocket.sent_data[0]
    print(MockSocket.addr)
    print(MockSocket.sent_data)

if __name__ == "__main__":
    pytest.main()
