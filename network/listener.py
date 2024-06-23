import socket
from connection import Connection


class Listener:
    def __init__(self, host, port, backlog=1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __repr__(self):
        print(f"Listener(port={self.port}, host={self.host}, backlog={self.backlog}")

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(self.backlog)

    def stop(self):
        self.s.close()

    def accept(self):
        conn, addr = self.s.accept()
        return Connection(conn)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.stop()
