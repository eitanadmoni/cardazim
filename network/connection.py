import socket
import functools
import struct


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
        data = self.conn.recv(4)
        length = int.from_bytes(data, "little")
        buff = []
        while True:
            data = self.conn.recv(1024)
            buff += data.decode('utf-8')
            if not data:
                break
            length -= len(data)
        if length != 0:
            raise Exception("Connection close before all message arrive")
        message = functools.reduce(lambda x, y: x + y, buff)
        print("Received data: " + message)

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


