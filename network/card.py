from crypt_image import CryptImage
from PIL import Image
from io import BytesIO
import struct

METADATA_LENGTH = 4

class Card:
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        print(f"<Card name ={self.name}, creator={self.creator}")

    def __str__(self):
        if self.solution:
            return f"Card {self.name} by {self.creator}\n  riddle: {self.riddle}\n  solution: {self.solution}"
        else:
            return f"Card {self.name} by {self.creator}\n  riddle: {self.riddle}\n  solution: unsolved"

    @classmethod
    def create_from_path(cls, name: str, creator: str, path, riddle: str, solution: str):
        image = CryptImage.create_from_path(path)
        return cls(name, creator, image, riddle, solution)

    def serialize(self) -> bytes:
        print(self.image.image.mode)
        name_length = len(self.name.encode('utf-8'))
        creator_length = len(self.creator.encode('utf-8'))
        riddle_length = len(self.riddle.encode('utf-8'))
        image_width, image_height = self.image.image.size
        format = f'<I{name_length}sI{creator_length}sII{len(self.image.image.tobytes())}s32sI{riddle_length}s'
        packed_data = struct.pack(format, name_length, self.name.encode('utf-8'), creator_length, self.creator.encode('utf-8'), image_width, image_height, self.image.image.tobytes(), self.image.key_hash, riddle_length, self.riddle.encode('utf-8'))
        return packed_data

    @classmethod
    def deserialize(cls, data):
        offset = METADATA_LENGTH
        name_length = int.from_bytes(data[:METADATA_LENGTH], 'little')
        name = (data[offset:offset+name_length]).decode('utf-8')
        offset += name_length
        creator_length = int.from_bytes(data[offset: offset + METADATA_LENGTH], 'little')
        offset += METADATA_LENGTH
        creator = (data[offset: offset + creator_length]).decode('utf-8')
        offset += creator_length
        image_width = int.from_bytes(data[offset:offset + METADATA_LENGTH], 'little')
        offset += METADATA_LENGTH
        image_height = int.from_bytes(data[offset: offset + METADATA_LENGTH], 'little')
        offset += METADATA_LENGTH
        image_bytes = data[offset: offset + (image_width*image_height*3)]
        offset += (image_width*image_height*3)
        key_hash = data[offset:offset + 32]
        offset += 32
        riddle_length = int.from_bytes(data[offset: offset + METADATA_LENGTH], 'little')
        offset += METADATA_LENGTH
        riddle = (data[offset: offset + riddle_length]).decode('utf-8')
        image = Image.frombytes('RGB', (image_width, image_height), image_bytes)
        crypt_image = CryptImage(image, key_hash)
        return cls(name, creator, crypt_image, riddle, None)
