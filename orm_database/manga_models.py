from peewee import *
import os

# Aqui criamos o banco de dados
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './mangas.db')
db = SqliteDatabase(filename)

class BaseModel(Model):
    """Classe model base"""
    id = IntegerField(primary_key=True, unique=True)
    nome = CharField()
    class Meta:
        database = db

class Site(BaseModel):
    url = CharField()
    last_cap_xpath = CharField()

class Mangas(BaseModel):
    site = ForeignKeyField(Site, backref='site')
    route = CharField()
    ultimo_cap = IntegerField()


if __name__ == '__main__':
    try:
        Site.create_table()
        print("Tabela 'Site' criada com sucesso!")
    except Exception as err:
        print("Erro ao criar a tabela: ", err)

    try:
        Mangas.create_table()
        print("Tabela 'Mangas' criada com sucesso!")
    except Exception as err:
        print("Erro ao criar a tabela: ", err)

