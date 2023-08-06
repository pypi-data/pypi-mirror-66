# -*- coding: utf-8 -*-
import json


class AnnaResponse():
	def __init__(self):
		# OBLIGATORIO
		self.container_ob = {
			'ClientStatus': '',  # OK, ERRO - OBLIGATORIO
		}

		# CONDICIONAL: Permitido si ClientStatus = ERRO
		self.container_cond = {
			'ClientMessage': "",
		}

		# OPCIONAL
		self.container_op = {
			'Containers': []
		}

	def gen_container(self, type_container, data):
		if type_container == "MSG":
			MyVar1 = '{"ClientStatus":"OK",'
			MyVar1 += '"ClientMessage":"",'
			MyVar1 += '"DevCallback":"",'
			MyVar1 += '"Containers":[{"Type":"MSG",'
			MyVar1 += '               "Phrase": "%s",' % (data)
			MyVar1 += '               "Alias":"P200",'
			MyVar1 += '               "Subject":"",' 
			MyVar1 += '               "Topic":"",'
			MyVar1 += '               "Scope":"",'
			MyVar1 += '               "AnswerType":"N",'
			MyVar1 += '               "AnswerTypeComment":"",'
			MyVar1 += '               "MediaURL":"",'
			MyVar1 += '               "ShowMsgHeader":"N",'
			MyVar1 += '               "WaitNext":0,'
			MyVar1 += '               "Enumeration":"",'
			MyVar1 += '               "JumpType":"",'
			MyVar1 += '               "JumpTo":"",'
			MyVar1 += '               "ResumeType":"CONTAINER",'
			MyVar1 += '               "ResumeTo":"",'
			MyVar1 += '               "WsEncodeUrl":"N",'
			MyVar1 += '               "WsUrl":"",'
			MyVar1 += '               "WsCallBackUrl":"",'
			MyVar1 += '               "WsCallBackMsg":"",'
			MyVar1 += '               "IgnoreServices":"N",'
			MyVar1 += '               "ExternalData":"",'
			MyVar1 += '               "RespostaDefault":"",'
			MyVar1 += '               "GroupAlias":"",'
			MyVar1 += '               "IsSensitive":"N"}]'
			MyVar1 += '}'

		return MyVar1
