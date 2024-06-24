from PIL import Image
from Crypto.Cipher import AES
from io import BytesIO
import hashlib


class CryptImage:
    def __init__(self, image, key_hash):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path):
        im = Image.open(path)
        key = None
        return cls(im, key)

    def image_to_binary(self):
        byte_io = BytesIO()
        self.image.save(byte_io, format=self.image.format)
        image_binary_data = byte_io.getvalue()
        byte_io.close()
        return image_binary_data

    def encrypt(self, key: str) -> None:
        self.key_hash = hashlib.sha256(hashlib.sha256(key.encode('utf-8')).digest()).digest()
        image_binary_data = self.image.tobytes()
        cipher = AES.new(hashlib.sha256(key.encode('utf-8')).digest(), AES.MODE_EAX, nonce=b'arazim')
        encrypted_binary_image = cipher.encrypt(image_binary_data)
        self.image = Image.frombytes(self.image.mode, self.image.size, encrypted_binary_image)

    def decrypt(self, key: str) -> bool:
        if self.key_hash != hashlib.sha256(hashlib.sha256(key.encode('utf-8')).digest()).digest():
            return False
        else:
            image_binary_data = self.image.tobytes()

            cipher = AES.new(hashlib.sha256(key.encode('utf-8')).digest(), AES.MODE_EAX, nonce=b'arazim')
            decrypted_binary_image = cipher.decrypt(image_binary_data)
            self.image = Image.frombytes(self.image.mode, self.image.size, decrypted_binary_image)
            return True







