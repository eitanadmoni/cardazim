import os
import json
from os import PathLike
from typing import Union
from PIL import Image
from card import Card
from card_driver import CardDriver, FilesystemDriver, SQLDriver

class Saver:
    def __init__(self, database_str: str, images_dir = "./images"):
        self.driver = self.get_driver(database_str)        
        self.images_dir = images_dir
        if not os.path.isdir(images_dir):
            os.makedirs(images_dir)

    def save(self, card: Card):
        metadata, image = parse_card(card)
        image_path = f"{self.images_dir}/{self.generate_identifier(card)}_image.png"
        image.save(image_path, "PNG")
        metadata['image_path'] = image_path
        metadata['identifier'] = self.get_identifier(card)
        self.driver.save_card(metadata)

    def get_identifier(self, card):
        return self.generate_identifier(card)

    def generate_identifier(self, card: Card) -> str:
        return f"{card.name}_{card.creator}"

    def load(self, identifier: str):
        metadata = self.driver.load_card(identifier)
        print(metadata)
        metadata.pop("identifier")
        key_hash = metadata.pop("key_hash")
        card =  Card.create_from_path(metadata["name"], metadata["creator"], metadata["image_path"], metadata["riddle"], metadata["solution"])
        card.image.key_hash = key_hash
        return card

    def get_driver(self, database_str):
        parts = database_str.split('://', 1)
        if parts[0] == 'filesystem':
            if not os.path.isdir(parts[1]):
                os.makedirs(parts[1])
            return FilesystemDriver(parts[1])
        
        if parts[0] == "sql":
            return SQLDriver(parts[1])
            

def parse_card(card):
    card_data = {"name": card.name, "creator": card.creator, "riddle": card.riddle, "solution": card.solution, "key_hash": card.image.key_hash}
    image = card.image.image
    return card_data, image





