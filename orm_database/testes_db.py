from models import Site,Mangas
from peewee import JOIN

def populate_test_data():

    data = (
        ('manga livre', 'https://mangalivre.net/', '//*[@id="chapter-list"]/div[3]/ul/li[1]/a', (
                                  ["The Beginning After The End - TurtleMe", "manga/the-beginning-after-the-end/7403 = CharField()", 131],
                                  ["The God of Highschool - Yong-Je Park", "manga/the-god-of-highschool/428", 527],
                                  ["Jujutsu Kaisen - Gege, Akutami ", "manga/jujutsu-kaisen/7178", 170])),
        )

    for nome,url,xpath,mangas in data:
        site = Site.create(nome=nome,last_cap_xpath=xpath,url=url)
        for nome,route,ultimo_cap in mangas:
            Mangas.create(nome=nome, route=route,ultimo_cap=ultimo_cap,site=site)

def select_mangas():
    mangas = []
    result = Mangas.select(Mangas,Site).join(Site, JOIN.INNER).order_by(Mangas.nome).dicts()
    for row in result:
        print(row)
        mangas.append(row)
    return  mangas

#populate_test_data()

select_mangas()
