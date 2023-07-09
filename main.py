from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
import os
from bs4 import BeautifulSoup
import world_map

page_sections = {
    "end": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t > div.m6QErb.tLjsW.eKbjU",
    "entreprises": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd"
}
entreprises = []

cities = world_map.get_cities("Côte d'Ivoire")[0]

search_text = f"entreprises à {cities}"

driver = webdriver.Chrome()


def security_of_null(variable):
    return variable.get_text() if variable else "N/A"


def contains_alphabet(string):
    pattern = re.compile(r'[a-zA-Z]')
    return bool(pattern.search(string))


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

    return BeautifulSoup(section_html, 'html.parser').find_all('div', class_=['Nv2PK', 'Q2HXcd', 'THOPZb'])


def get_all_entreprises_infos(soup):
    for entreprise_infos in soup:
        name = entreprise_infos.get('aria-label')

        average_note = security_of_null(entreprise_infos.find(
            'div', class_='bfdHYd').find('span', class_='MW4etd'))

        vote_count = security_of_null(entreprise_infos.find(
            'div', class_='bfdHYd').find('span', class_='UY7F9'))

        activity = security_of_null(entreprise_infos.select_one(
            'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div:nth-child(1) span:nth-child(1) span'))

        phone_number = security_of_null(entreprise_infos.select_one(
            'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div:nth-child(2) span:nth-child(2) span:nth-child(2)'))
        if (phone_number == "N/A"):
            phone_number = security_of_null(entreprise_infos.select_one(
                'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div:nth-child(2) span span'))
            if (contains_alphabet(phone_number)):
                phone_number = "N/A"

        href_element = entreprise_infos.select_one(
            'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.Rwjeuc div:nth-child(1) a')
        if href_element:
            href = href_element.get('href')
        else:
            href = "N/A"

    # google maps masque phone number et href pour certaines categories
    # il faudra donc aller sur la page de l'entreprise pour récupérer les infos
        if (phone_number == "N/A" and href == "N/A"):
            phone_number = entreprise_infos.select_one('div a').get('href')
        adresse_element = entreprise_infos.select_one(
            'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div span:nth-child(2) span:nth-child(2)')
        if adresse_element:
            adresse = adresse_element.get_text()
        else:
            adresse = "N/A"

        entreprise = {
            'name': name,
            'activity': activity,
            'celebrity_indice': f"{average_note} {vote_count}",
            'phone_number': phone_number,
            'web_site': href,
            'adresse': adresse
        }
        entreprises.append(entreprise)


def load_data(entreprises):
    title = search_text.strip().replace(
        "-", "_").replace("/", "_").replace(" ", "_").replace(":", "_").replace("|", "")

    # On ouvre le fichier CSV en mode écriture et on spécifie l'encodage.
    with open(f'{title}.csv', mode='w', newline='', encoding='utf-8') as file:
        # On spécifie les noms des colonnes dans le fichier CSV.
        fieldnames = ['index', 'name', 'activity', 'celebrity_indice',
                      'phone_number', 'web_site', 'adresse']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # On écrit l'en-tête du fichier CSV avec les noms des colonnes.
        writer.writeheader()

        # On initialise un compteur d'index.
        index = 1

        # Pour chaque produit extrait, on ajoute un index, puis on écrit les données du produit dans une ligne du fichier CSV.
        for entreprise in entreprises:
            entreprise['index'] = index
            writer.writerow(entreprise)
            index += 1


soup = get_entreprises_html_section(search_text)
get_all_entreprises_infos(soup)

load_data(entreprises)
