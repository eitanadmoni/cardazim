import argparse
import sys
import socket
import functools
import threading


def recv_from_client(conn):
    """
    Receive data from client and print it
    :param conn: socket to connect wih client
    """
    data = conn.recv(4)
    length = int.from_bytes(data, "little")
    buff = []
    while True:
        data = conn.recv(1024)
        buff += data.decode('utf-8')
        if not data:
            break
    message = functools.reduce(lambda x, y: x+y, buff)
    print("Received data: " + message)
    conn.close()


def run_server(ip, port):
    """
    listen for connections and give each cliend a thread
    :param ip: ip of server
    :param port: port to listen at
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=recv_from_client, args=(conn,)).start()
            recv_from_client(s.accept()[0])






def get_args():
    parser = argparse.ArgumentParser(description='recv data from client.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
