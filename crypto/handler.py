import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from PIL import Image


class CryptoHandler:
    def __init__(self):
        self.salt = b'anthropic_salt_2024'
        self.max_file_size = 5 * 1024 * 1024
        self.supported_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']

    def validate_file_size(self, file_path: str) -> bool:
        return os.path.getsize(file_path) <= self.max_file_size

    def generate_key(self, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_file(self, file_path: str, password: str, progress_callback=None) -> tuple[bytes, bool]:
        try:
            if not file_path or not os.path.exists(file_path):
                return "No file path provided", False

            ext = os.path.splitext(file_path)[1].lower()
            if ext not in self.supported_extensions:
                return f"Unsupported file type: {ext}", False

            if not self.validate_file_size(file_path):
                return "File exceeds size limit", False

            return self._encrypt_data(file_path, password, progress_callback)
        except Exception as e:
            return f"Encryption error: {str(e)}", False

    def _encrypt_data(self, file_path: str, password: str, progress_callback=None) -> tuple[bytes, bool]:
        key = self.generate_key(password)
        fernet = Fernet(key)

        with open(file_path, 'rb') as file:
            file_data = file.read()
            total_chunks = len(file_data) // 1024 + (1 if len(file_data) % 1024 else 0)

            for i in range(total_chunks):
                if progress_callback:
                    progress_callback((i + 1) / total_chunks)

        encrypted_data = fernet.encrypt(file_data)
        return encrypted_data, True

    def decrypt_file(self, encrypted_data: bytes, password: str, original_ext: str, progress_callback=None) -> tuple[
            bytes, bool]:
        try:
            if original_ext.lower() not in self.supported_extensions:
                return f"Unsupported file type: {original_ext}", False

            return self._decrypt_data(encrypted_data, password, progress_callback)
        except Exception as e:
            return f"Decryption error: {str(e)}", False

    def _decrypt_data(self, encrypted_data: bytes, password: str, progress_callback=None) -> tuple[bytes, bool]:
        try:
            key = self.generate_key(password)
            fernet = Fernet(key)

            total_chunks = len(encrypted_data) // 1024 + (1 if len(encrypted_data) % 1024 else 0)
            for i in range(total_chunks):
                if progress_callback:
                    progress_callback((i + 1) / total_chunks)

            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data, True
        except InvalidToken:
            return "Invalid decryption key", False
        except Exception as e:
            return str(e), False

    def data_to_image(self, data: bytes) -> Image.Image:
        binary = ''.join(format(byte, '08b') for byte in data)
        width = 1024
        height = (len(binary) + width - 1) // width
        img = Image.new('RGB', (width, height), color='white')
        pixels = img.load()

        for i in range(len(binary)):
            x = i % width
            y = i // width
            if y < height:
                pixels[x, y] = (0, 0, 0) if binary[i] == '1' else (255, 255, 255)

        return img

    def image_to_data(self, img: Image.Image) -> bytes:
        width, height = img.size
        pixels = img.load()
        binary = ''

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary += '1' if r < 128 else '0'

        byte_data = bytearray()
        for i in range(0, len(binary), 8):
            byte = binary[i:i + 8]
            if len(byte) == 8:
                byte_data.append(int(byte, 2))

        return bytes(byte_data)
