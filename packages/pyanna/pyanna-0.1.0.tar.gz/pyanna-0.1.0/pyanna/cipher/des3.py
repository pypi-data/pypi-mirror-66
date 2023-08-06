# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Cipher import DES3
from pyDes import *


class DES_3():
	def __init__(self, ENC_KEY, DEC_KEY, MODE="CBC", IV=None):
		self.DEC_KEY = DEC_KEY
		self.ENC_KEY = ENC_KEY

		self.IV_base64_bytes = IV
		if IV is None:
			self.IV_base64_bytes = self.gen_iv_random()

	def gen_iv_random(self):
		return Random.new().read(DES3.block_size)

	def decrypt(self, encrypted_text, iv_new=None):
		iv = self.IV_base64_bytes
		if iv_new is not None:
			iv = iv_new
		cipher = triple_des(self.DEC_KEY, CBC, iv, pad=None, padmode=PAD_PKCS5)
		decrypted_text = cipher.decrypt(encrypted_text)
		decrypted_text = decrypted_text.decode("utf-8") 
		return decrypted_text

	def encrypt(self, plaintext, iv_new=None, keyEncrypt=None):
		iv = self.IV_base64_bytes
		if iv_new is not None:
			iv = iv_new
		if keyEncrypt is None:
			keyEncrypt = self.ENC_KEY
		cipher = triple_des(keyEncrypt, CBC, iv, pad=None, padmode=PAD_PKCS5)
		x = cipher.encrypt(plaintext)
		return x
