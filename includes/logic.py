from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
import os
from bs4 import BeautifulSoup
import includes.world_map as world_map

activities = world_map.activities

driver = webdriver.Chrome()


def security_of_null(variable):
    return variable.get_text() if variable else "N/A"


def contains_alphabet(string):
    pattern = re.compile(r'[a-zA-Z]')
    return bool(pattern.search(string))


def celebrity_indice(vote_count, average_note):
    if vote_count != "N/A" and average_note != "N/A":
        average_note = float(average_note.replace(",", "."))
        vote_count = float(vote_count.replace(
            "(", "").replace(")", ""))
        return average_note*vote_count
    else:
        return 0


def get_entreprises_html_section(search_text):
    page_sections = {
        "end": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t > div.m6QErb.tLjsW.eKbjU",
        "entreprises": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd",
        "end_x": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.tLjsW.eKbjU > div > p > span > span",
        "single": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2",
        "another_country": "#omnibox-directions > div > div.JuLCid",
        "region": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf.dS8AEf > div > div > div.CPtD3c"
    }
    driver.get("https://www.google.com/maps/")

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.ENTER)

    driver.implicitly_wait(1)  # Attendre que la page se charge complètement

    # Définir  les variables de sélection
    end_x_locator = (By.CSS_SELECTOR, page_sections["end_x"])
    single_page_locator = (By.CSS_SELECTOR, page_sections["single"])
    another_country_locator = (
        By.CSS_SELECTOR, page_sections["another_country"])
    regions_locator = (By.CSS_SELECTOR, page_sections["region"])
    try:
        # Vérifiez si la page affichée est une page unique d'infos entreprise
        wait = WebDriverWait(driver, 3)
        wait.until(EC.visibility_of_element_located(single_page_locator))
        single_page = driver.find_element(
            By.CSS_SELECTOR, page_sections["single"]
        )
        if (single_page.is_displayed):
            section_html = 0
            return section_html
    except NoSuchElementException:
        try:
            # Vérifiez si la page affichée est une redirection vers un lieu précis
            wait = WebDriverWait(driver, 1)
            wait.until(EC.visibility_of_element_located(
                another_country_locator))
            another_country = driver.find_element(
                By.CSS_SELECTOR, page_sections["another_country"]
            )
            if (another_country.is_displayed):
                section_html = 0
                return section_html
        except NoSuchElementException:
            try:
                # Vérifiez si la page affichée contient une section de planification tarifaire | temporelle | géographique
                wait.until(EC.visibility_of_element_located(
                    regions_locator))
                region = driver.find_element(
                    By.CSS_SELECTOR, page_sections["region"]
                )
                if (region.is_displayed):
                    section_html = 0
                    return section_html
            except NoSuchElementException:
                try:
                    # Vérifiez si la liste d'e/se tient sur une page grâce au end_x_locator
                    wait = WebDriverWait(driver, 3)
                    wait.until(EC.visibility_of_element_located(end_x_locator))
                    section_locator = (
                        By.CSS_SELECTOR, page_sections["entreprises"])
                    section_html = driver.find_element(
                        *section_locator).get_attribute("innerHTML")
                except TimeoutException:
                    # Faire défiler jusqu'à la section "end"
                    actions = ActionChains(driver)
                    while True:
                        try:
                            section = driver.find_element(
                                By.CSS_SELECTOR, page_sections["end"]
                            )
                            if section.is_displayed():
                                break
                        except NoSuchElementException:
                            pass
                        actions.send_keys(Keys.ARROW_DOWN).perform()

                    # Attendre que la section "entreprises" se charge complètement
                    wait = WebDriverWait(driver, 10)
                    section_locator = (
                        By.CSS_SELECTOR, page_sections["entreprises"])
                    section_html = driver.find_element(
                        *section_locator).get_attribute("innerHTML")
            return BeautifulSoup(section_html, 'html.parser').find_all('div', class_=['Nv2PK', 'Q2HXcd', 'THOPZb'])


def get_all_entreprises_infos(soup):
    entreprises = []
    if soup:
        for entreprise_infos in soup:
            name = security_of_null(entreprise_infos.select_one(
                'div.NrDZNb div.qBF1Pd.fontHeadlineSmall'))
            average_note = security_of_null(
                entreprise_infos.select_one('div.bfdHYd span.MW4etd'))
            vote_count = security_of_null(
                entreprise_infos.select_one('div.bfdHYd span.UY7F9'))
            activity = security_of_null(entreprise_infos.select_one(
                'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div:nth-child(1) span:nth-child(1) span'))
            phone_number = security_of_null(entreprise_infos.select_one(
                'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div:nth-child(2) span:nth-child(2) span:nth-child(2)'))
            if phone_number == "N/A":
                phone_number = security_of_null(entreprise_infos.select_one(
                    'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div:nth-child(2) span span'))
                if contains_alphabet(phone_number):
                    phone_number = "N/A"
            href_element = entreprise_infos.select_one(
                'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.Rwjeuc div:nth-child(1) a')
            href = href_element.get('href') if href_element else "N/A"
            if phone_number == "N/A" and href == "N/A":
                phone_number = entreprise_infos.select_one('div a').get('href')
            adresse_element = entreprise_infos.select_one(
                'div.bfdHYd.Ppzolf.OFBs3e div.lI9IFe div.y7PRA div div div.UaQhfb.fontBodyMedium div:nth-child(4) div span:nth-child(2) span:nth-child(2)')
            adresse = adresse_element.get_text() if adresse_element else "N/A"
            ic = celebrity_indice(vote_count, average_note)
            entreprise = {
                'name': name,
                'activity': activity,
                'celebrity_indice': f"{average_note} {vote_count}",
                'ic': ic,
                'phone_number': phone_number,
                'web_site': href,
                'adresse': adresse
            }
            entreprises.append(entreprise)
    return entreprises


def load_data(search_text, entreprises, country_of_search):
    title = search_text.strip().replace(
        "-", "_").replace("/", "_").replace(" ", "_").replace(":", "_").replace("|", "")
    folder = country_of_search.strip().replace(
        "-", "_").replace("/", "_").replace(" ", "_").replace(":", "_").replace("|", "")
    if not os.path.exists(f'result/{folder}'):
        os.makedirs(f'result/{folder}')
    with open(f'result/{folder}/{title}.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['index', 'name', 'activity', 'celebrity_indice', 'ic',
                      'phone_number', 'web_site', 'adresse']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        # On initialise un compteur d'index.
        index = 1

        for entreprise in entreprises:
            entreprise['index'] = index
            writer.writerow(entreprise)
            index += 1
    entreprises = []


def scrape_activities_data(activities: list, country_of_search: str, town: str = None):
    cities = world_map.get_cities(country_of_search)
    if town is not None and isinstance(town, str):
        cities = [town]

    for city in cities:
        for activity in activities:
            search_text = f"{activity} à {city}"
            print(
                f"\033[92m Récupération des infos {activity} à {city} ...\033[0m")
            soup = get_entreprises_html_section(search_text)
            entreprises = get_all_entreprises_infos(soup)
            load_data(search_text, entreprises, country_of_search)
            print(
                f"\033[92m \u2714 ({activity} à {city}): enregistré \033[0m")


def simple_search(search: str, country_of_search: str):
    search_text = f"{search}"
    print(
        f"\033[92m Récupération des infos {search_text}: {country_of_search} ...\033[0m")
    soup = get_entreprises_html_section(search_text)
    entreprises = get_all_entreprises_infos(soup)
    load_data(search_text, entreprises, country_of_search)
    print(
        f"\033[92m \u2714 ({search_text}: {country_of_search}): enregistré \033[0m")
