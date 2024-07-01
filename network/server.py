import argparse
import sys
import threading
from listener import Listener
from crypt_image import CryptImage
from card import Card
from saver import Saver


def client_handler(connection, driver_path):
    serialized_card = connection.receive_message()
    connection.close()
    deserialized_card = Card.deserialize(serialized_card)
    print(f"Received card {deserialized_card.name} by {deserialized_card.creator}.")
    card_manager = Saver(driver_path)
    card_manager.save(deserialized_card)
    print("Saved card to database")


def run_server(ip, port, directory_name):
    with Listener(ip, port) as listener:
        while True:
            connection = listener.accept()
            threading.Thread(target=client_handler, args=(connection, directory_name,)).start()


def get_args():
    parser = argparse.ArgumentParser(description='recv data from client.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data_directory', type=str,
                        help='directory to save cards')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port, args.data_directory)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())

