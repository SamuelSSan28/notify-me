# coding=utf8
from prefect import Task
from prefect.engine import signals
from peewee import JOIN
from manga_models import Mangas,Site

class GetMangasToSee(Task):

	def run(self):
		self.logger.info("Iniciando metodo para buscar os mangas cadastrados no banco")
		try:
			mangas = self.getMangas()
			self.logger.info(f"Busca no banco realizada com sucesso - {len(mangas)} encontrados")
			return mangas

		except Exception as err:
			self.logger.error(f"Erro ao buscar o processo: ",err )
			raise signals.FAIL("Error: "+err)


	def getMangas(self):
		mangas = []
		result =Mangas.select(Mangas,Site).join(Site, JOIN.INNER).order_by(Mangas.nome).dicts()
		for row in result:
			mangas.append(row)
		return mangas
