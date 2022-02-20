# coding=utf8
from prefect import Task
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
from prefect.engine import signals

class ScrapingSite(Task):

    def run(self,mangah):
        try:
            self.logger.info("Iniciando o scraping no site: "+mangah['url'])
            url= mangah['url']+mangah['route']
            last_cap= mangah['ultimo_cap']
            last_cap_xpath = mangah['last_cap_xpath']
            new_last_cap,link = self.scrapingPage(url,last_cap_xpath)
            mangah['new_last_cap'] = new_last_cap
            mangah['link'] = link
            mangah['is_new'] = int(new_last_cap) != last_cap
            return mangah
        except Exception as err:
            self.logger.error(f"Erro no scraping {err}")
            raise signals.FAIL("Error: " + err)

    def scrapingPage(self, url,last_cap_xpath):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        except Exception as err:
            driver = webdriver.Chrome('./chromedriver.exe', options=options)

        driver.set_page_load_timeout(10000)

        driver.get(url)
        element = driver.find_element_by_xpath(last_cap_xpath)

        text = element.text
        link = element.get_attribute('href')
        new_last_cap = re.sub('\D', '', text)

        return new_last_cap,link