from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
from bs4 import BeautifulSoup

search_text = "bibliothèque Calavi"
page_sections = {
    "end": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t > div.m6QErb.tLjsW.eKbjU",
    "entreprises": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd"
}

driver = webdriver.Chrome()


def get_entreprises_html_section(search_text):
    driver.get("https://www.google.com/maps/")

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.ENTER)

    driver.implicitly_wait(1)  # Attendre que la page se charge complètement

    # Scroller jusqu'à la section spécifique
    actions = ActionChains(driver)
    while True:
        try:
            section = driver.find_element(
                By.CSS_SELECTOR, page_sections["end"]
            )
            if section.is_displayed():
                break
        except:
            pass
        actions.send_keys(Keys.ARROW_DOWN).perform()

    # Attendre que la section se charge complètement
    wait = WebDriverWait(driver, 10)

    section_locator = (By.CSS_SELECTOR, page_sections["end"])

    section = wait.until(EC.visibility_of_element_located(section_locator))
    section_html = driver.find_element(
        By.CSS_SELECTOR, page_sections["entreprises"]
    ).get_attribute("innerHTML")

    return section_html


entreprises_html_section = get_entreprises_html_section(search_text)
soup = BeautifulSoup(entreprises_html_section, 'html.parser')
print(len(soup.find_all('div', class_='qBF1Pd')))
