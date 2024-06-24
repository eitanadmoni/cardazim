import argparse
import sys
import socket
import struct
from connection import Connection
from crypt_image import CryptImage
from card import Card


###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, name, creator, riddle, solution, path):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    with Connection.connect(server_ip, server_port) as connection:
        card = Card.create_from_path(name, creator, path, riddle, solution)
        card.image.encrypt("hash_key")
        serialized_card = card.serialize()
        print(f"Sending card {card.name} by {card.creator}...")
        connection.send_message(serialized_card)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='the data')
    parser.add_argument('creator', type=str,
                        help='the data')
    parser.add_argument('riddle', type=str,
                        help='the data')
    parser.add_argument('solution', type=str,
                        help='the data')
    parser.add_argument('path', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.name, args.creator, args.riddle, args.solution, args.path)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
