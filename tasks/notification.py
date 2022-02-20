# coding=utf8
from prefect import Task
from prefect.engine import signals
import requests
from dotenv import dotenv_values
import os

class TelegramNotifications(Task):
	def __init__(self,*args, **kwargs):
		super(TelegramNotifications, self).__init__(*args, **kwargs)
		env_values = dotenv_values("./.env")
		if len(env_values.keys()) > 1:
			self.BOT_TOKEN = env_values['BOT_TOKEN']
			self.GROUP_ID = env_values['GROUP_ID']
		else:
			self.BOT_TOKEN = os.environ['BOT_TOKEN']
			self.GROUP_ID = os.environ['GROUP_ID']


	def run(self,data_dict):
		self.logger.info("Enviando a msg para o telegram")
		try:
			if not data_dict['is_new']:
				raise signals.SKIP("Nenhum cap novo encontrado")

			new_cap = data_dict['new_last_cap']
			manga = data_dict['nome']
			link = data_dict['link']

			message = f"Capitulo {new_cap} de {manga} lançado: {link}"
			url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage?chat_id={self.GROUP_ID}&text={message}"
			response = requests.post(url)

			if response and response.status_code == 400:
				raise signals.FAIL("Erro no request",response.text)

			self.logger.info("Mensagem enviada para o telegram!")

		except Exception as err:
			self.logger.error(f"Erro ao enviar a msg para o telegram: ",err )
			raise signals.FAIL("Error: "+err)



