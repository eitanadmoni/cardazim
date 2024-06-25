import socket
import functools
import struct

KB = 1024
METADATA_LENGTH = 4


class Connection:
    def __init__(self, connection: socket.socket):
        self.conn = connection

    def __repr__(self):
        source_ip, source_port = self.conn.getsockname()
        dest_ip, dest_port = self.conn.getpeername()
        print(f"<Connection from {source_ip}:{source_port} to {dest_ip}:{dest_port}")

    def send_message(self, message: bytes):
        n = len(message)
        format = f'<I{n}s'
        data = struct.pack(format, n, message)
        self.conn.sendall(data)

    def receive_message(self):
        message_length = int.from_bytes(self.conn.recv(METADATA_LENGTH), "little")
        message_from_client = b''
        while True:
            data = self.conn.recv(KB)
            if not data:
                break
            message_from_client += data
        if message_length != len(message_from_client):
            raise Exception("Connection close before all message arrive")
        return message_from_client

    @classmethod
    def connect(cls, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return cls(s)

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
            return self.close()
