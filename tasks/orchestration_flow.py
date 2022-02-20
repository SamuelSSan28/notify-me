# coding=utf8
import datetime
from prefect import Flow, unmapped
from getMangasToSee import GetMangasToSee
from scraping import ScrapingSite
from notification import TelegramNotifications
# from saveDB import SaveDB
from datetime import timedelta
from prefect.schedules import IntervalSchedule

schedule = IntervalSchedule(interval=timedelta(hours=12))

flow = Flow("Camara_Bot")
get_mangas_task = GetMangasToSee(name="GetMangasToSee")
telegram_notification = TelegramNotifications(name="TelegramNotifications")
scraping_sites = ScrapingSite(name="ScrapingSite", max_retries=3, retry_delay=datetime.timedelta(minutes=3))
# save_data_sqlite = SaveDB(name="SaveDB") #update DB
# TODO: atualizar os dados do banco

flow.set_dependencies(scraping_sites,
                      upstream_tasks=[get_mangas_task],
                      keyword_tasks={"mangah": get_mangas_task}, mapped=True)

flow.set_dependencies(telegram_notification,
                        upstream_tasks=[scraping_sites],
                        keyword_tasks={"data_dict":scraping_sites},
                                        mapped=True)

if __name__ == '__main__':
    flow.run()
