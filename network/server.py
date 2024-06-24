import argparse
import sys
import threading
from listener import Listener
from crypt_image import CryptImage
from card import Card


def client_handler(connection):
    serialized_card = connection.receive_message()
    connection.close()
    deserialized_card = Card.deserialize(serialized_card)
    print(f"Received card {deserialized_card.name} by {deserialized_card.creator}")


def run_server(ip, port):
    with Listener(ip, port) as listener:
        while True:
            connection = listener.accept()
            threading.Thread(target=client_handler, args=(connection,)).start()


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
