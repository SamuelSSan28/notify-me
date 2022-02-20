# coding=utf8
from prefect import Task
from models import Projetos
from prefect.engine import signals

class SaveDB(Task):

    def run(self,new_projects):
        self.logger.info("Salvando os processos no banco")
        try:
            self.logger.info(f"{new_projects}")
            if new_projects and len(new_projects) == 0:
                raise signals.SKIP("Nenhum projeto encontrado")

            self.saveDB(new_projects)
            self.logger.info(f"Projetos salvos no banco com sucesso")
        except Exception as err:
            self.logger.error(f"Erro ao salvar os projetos no banco {err}")

    def saveDB(self,new_projects):
        for new_project in new_projects:
            dados = {"processo" : new_project["processo"],
                     "protocolo" : new_project["protocolo"],
                     "data" : new_project["data"],
                     "titulo" : new_project["resumo"],
                     "situacao" : new_project["situacao"],
                     "vereador" : new_project["autor"],
                     "tipo" : new_project["tipo"] }
            Projetos.insert(dados).execute()

