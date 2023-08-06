# -*- coding: utf-8 -*-

import base64

from .cipher.des3 import DES_3


class AnnaCrypto():
	def __init__(self, DEC_KEY, ENC_KEY, MODE='3DES', SUBMODE='CBC', IVRECIBIDO=None):
		self.DEC_KEY = self.fromBase64String(DEC_KEY)

		self.ENC_KEY = self.fromBase64String(ENC_KEY)

		self.IV_RECIBIDO = IVRECIBIDO
		if IVRECIBIDO is not None:
			self.IV_RECIBIDO = self.fromBase64String(self.IV_RECIBIDO)

		self.MODE = MODE

	def get_manager(self):
		if self.MODE == "3DES":
			return DES_3(ENC_KEY=self.ENC_KEY, DEC_KEY=self.DEC_KEY, IV=self.IV_RECIBIDO)
		return None

	# =====================================================
	def get_dec_key(self):
		return self.DEC_KEY

	def get_iv(self):
		return self.IV_RECIBIDO
	# =====================================================

	def fromBase64String(self, stringData, MODE="utf-8"):
		return base64.b64decode(stringData.encode(MODE))

	def convertString(self, base64_bytes):
		return base64.b64encode(base64_bytes).decode("utf-8")

	def encrypt(self, message, iv_new=None, keyEncrypt=None):
		manager = self.get_manager()
		if keyEncrypt is None:
			keyEncrypt = self.ENC_KEY

		iv = self.IV_RECIBIDO
		if iv_new is not None:
			iv = iv_new

		x = manager.encrypt(plaintext=message, iv_new=iv, keyEncrypt=keyEncrypt)
		return base64.b64encode(x).decode("utf-8")

	def decrypt(self, encrypted_text, iv_new=None):
		manager = self.get_manager()
		encrypted_text_base64_bytes = self.fromBase64String(encrypted_text)
		return manager.decrypt(encrypted_text=encrypted_text_base64_bytes, iv_new=iv_new)

	def gen_iv(self):
		x = DES_3(ENC_KEY=self.ENC_KEY, DEC_KEY=self.DEC_KEY)
		x = x.gen_iv_random()
		return self.convertString(x)
