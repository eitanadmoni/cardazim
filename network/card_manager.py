import os
import json
from os import PathLike
from typing import Union
from PIL import Image
from card import Card

class CardManager:
    def __init__(self):
        self.card_to_id = {}

    def save(self, card: Card, dir_path: Union[str, PathLike] = '.'):
        new_dir_path = f"{dir_path}/{self.get_identifier(card)}"
        os.makedirs(new_dir_path)
        image_path = os.path.join(new_dir_path, "image.jpg")
        card.image.image.save(image_path, "JPEG")
        card_data = {"name": card.name, "creator": card.creator, "riddle": card.riddle, "solution": card.solution, "image_path": image_path}
        json_object = json.dumps(card_data, indent=4)
        json_path = os.path.join(new_dir_path, "metadata.json")
        with open(json_path, "w") as json_file:
            json_file.write(json_object)

    def get_identifier(self, card: Card):
        return self.generate_identifier(card)

    def generate_identifier(self, card: Card) -> str:
        self.card_to_id[(card.name, card.creator)] = (card.name, card.creator)
        return card.name + card.creator

