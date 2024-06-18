import argparse
import sys
import socket
import struct

def run_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            print("Received data: ",  end ="")
            data = conn.recv(4)
            while True:
                data = conn.recv(1024)
                message = data.decode('utf-8')
                if not data:
                    break
                print(message,  end ="")
            print()
            conn.close()






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
