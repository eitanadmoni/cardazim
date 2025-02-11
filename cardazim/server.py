import argparse
import sys
import socket
import struct

def run_server(ip, port):
    """Function to run the server, receive data from clients, and print it."""
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(5)
        
        # Bind the server to the provided IP and port
        server_socket.bind((ip, port))
    
        # Listen for incoming connections
        server_socket.listen(5)
        
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            
            # Receive the data sent by the client
            data = client_socket.recv(1024)
            
            if data:
                # Decode and print the received data
                data = data[4:]
                print(f"Received data: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure the server socket is closed properly
        server_socket.close()

def get_args() -> argparse.Namespace:
    """
    Parse the command line arguments required to run the server.

    :returns: The parsed arguments, as an 'argparse.Namespace' object. Example for usage: 'get_args().server_ip'
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description='Run a server that listens for data.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main() -> None:
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()


    try:
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
