from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from bs4 import BeautifulSoup
import csv
import os
import includes.geo as geo
from includes.utils import (
    is_valid_domain, is_valid_phone_number,
    security_of_null, celebrity_indice
)
from includes.driver import create_driver

activities = geo.activities


def get_entreprises_html_section(driver, search_text):
    page_sections = {
        "entreprises": "div[role='feed']",
        "single": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2",
        "another_country": "#omnibox-directions > div > div.JuLCid",
        "region": "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf.dS8AEf > div > div > div.CPtD3c"
    }
    driver.get("https://www.google.com/maps/")

    # Accepter la page de consentement cookies Google si elle apparaît
    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//form[contains(@action,'consent')]//button"))
        )
        accept_btn.click()
    except:
        pass

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='q']"))
    )
    search_box = driver.find_element(By.CSS_SELECTOR, "input[name='q']")
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.ENTER)

    driver.implicitly_wait(1)

    single_page_locator = (By.CSS_SELECTOR, page_sections["single"])
    another_country_locator = (By.CSS_SELECTOR, page_sections["another_country"])
    regions_locator = (By.CSS_SELECTOR, page_sections["region"])
    try:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.visibility_of_element_located(single_page_locator))
        single_page = driver.find_element(By.CSS_SELECTOR, page_sections["single"])
        if single_page.is_displayed:
            return 0
    except:
        try:
            wait = WebDriverWait(driver, 1)
            wait.until(EC.visibility_of_element_located(another_country_locator))
            another_country = driver.find_element(By.CSS_SELECTOR, page_sections["another_country"])
            if another_country.is_displayed:
                return 0
        except:
            try:
                wait.until(EC.visibility_of_element_located(regions_locator))
                region = driver.find_element(By.CSS_SELECTOR, page_sections["region"])
                if region.is_displayed:
                    return 0
            except:
                pass

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, page_sections["entreprises"]))
    )
    container = driver.find_element(By.CSS_SELECTOR, page_sections["entreprises"])
    while True:
        at_bottom = driver.execute_script(
            "return arguments[0].scrollHeight - arguments[0].scrollTop <= arguments[0].clientHeight + 5",
            container
        )
        if at_bottom:
            break
        driver.execute_script("arguments[0].scrollBy(0, 500)", container)

    section_html = driver.find_element(By.CSS_SELECTOR, page_sections["entreprises"]).get_attribute("innerHTML")
    return BeautifulSoup(section_html, 'html.parser').find_all('div', class_=['Nv2PK', 'Q2HXcd', 'THOPZb'])


# ✔ tested and working
def get_all_entreprises_infos(soup):
    entreprises = []
    if soup:
        for entreprise_infos in soup:
            name = security_of_null(entreprise_infos.select_one(
                'div.NrDZNb div.qBF1Pd.fontHeadlineSmall'))
            average_note = security_of_null(
                entreprise_infos.select_one('span[role="img"].ZkP5Je span.MW4etd'))
            vote_count = security_of_null(
                entreprise_infos.select_one('span[role="img"].ZkP5Je span.UY7F9'))
            activity = security_of_null(entreprise_infos.select_one(
                'div.W4Efsd div.W4Efsd span:first-child > span'))
            phone_number = security_of_null(entreprise_infos.select_one('.UaQhfb.fontBodyMedium .W4Efsd + .W4Efsd > .W4Efsd + .W4Efsd > span:last-child > span:last-child'))
            if phone_number != "N/A" and not is_valid_phone_number(phone_number):
                phone_number = "N/A"
            href_element = entreprise_infos.select_one('.lI9IFe .Rwjeuc a.lcr4fd.S9kvJb')
            href = href_element.get('href') if href_element else "N/A"
            address = security_of_null(entreprise_infos.select_one(
                'div.W4Efsd div.W4Efsd span:last-child span:last-child'))
            ic = celebrity_indice(vote_count, average_note)
            transition_element = entreprise_infos.select_one('a.hfpxzc')
            transition = transition_element.get('href') if transition_element else "N/A"
            entreprise = {
                'name': name,
                'activity': activity,
                'celebrity_indice': f"{average_note} {vote_count}",
                'ic': ic,
                'phone_number': phone_number,
                'web_site': href,
                'address': address,
                'transition': transition
            }
            entreprises.append(entreprise)
    return entreprises


def href_checker(entreprises):
    for entreprise in tqdm(entreprises, desc="Entreprises"):
        if "https://www.google.com/maps/" in entreprise['transition']:
            html_content = None
            with create_driver(headless=True) as driver:
                try:
                    driver.get(entreprise['transition'])
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div"))
                    )
                    html_content = driver.page_source
                except Exception as e:
                    print(f"Erreur lors de l'extraction de l'URL avec Selenium : {e}")

            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                try:
                    section_html = soup.select_one(
                        'div[role="region"]'
                    )
                    if section_html:
                        section_parse = section_html.find_all(
                            'div', class_=['Io6YTe', 'fontBodyMedium', 'kR99db']
                        )
                        for tag in section_parse:
                            text = tag.get_text()
                            if is_valid_phone_number(text):
                                print(text)
                                entreprise.update({"phone_number": text})
                                print(entreprise["phone_number"])
                            elif is_valid_domain(text):
                                entreprise.update({"web_site": text})
                    else:
                        print("Élément avec le sélecteur donné non trouvé.")
                except Exception as e:
                    print(f"Erreur lors du parsing : {e}")
    return entreprises


def load_data(search_text, entreprises, country_of_search, town):
    title = search_text.strip().replace(
        "-", "_").replace("/", "_").replace(" ", "_").replace(":", "_").replace("|", "")
    folder = country_of_search.strip().replace(
        "-", "_").replace("/", "_").replace(" ", "_").replace(":", "_").replace("|", "")
    if not os.path.exists(f'result/{folder}'):
        os.makedirs(f'result/{folder}')
    with open(f'result/{folder}/{title}.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['index', 'name', 'activity', 'celebrity_indice', 'ic',
                      'phone_number', 'web_site', 'address', 'town', 'transition']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        index = 1
        for entreprise in entreprises:
            entreprise['town'] = town
            entreprise['index'] = index
            writer.writerow(entreprise)
            index += 1


def scrape_activities_data(activities: list, country_of_search: str, town: list = None):
    cities = geo.get_cities(country_of_search)
    if town is not None and isinstance(town, list):
        cities = town

    with create_driver() as driver:
        for city in tqdm(cities, desc='Cities'):
            for activity in tqdm(activities, desc="Activities"):
                location = f"{city} {country_of_search}" if country_of_search else city
                search_text = f"{activity} à {location}"
                print(f"\033[92m Récupération des infos {activity} à {location} ...\033[0m")
                soup = get_entreprises_html_section(driver, search_text)
                entreprises = get_all_entreprises_infos(soup)
                entreprises = href_checker(entreprises)
                load_data(search_text, entreprises, country_of_search, city)
                print(f"\033[92m \u2714 ({activity} à {city}): enregistré \033[0m")


def simple_search(search: str, country_of_search: str, town: str):
    location = f"{town} {country_of_search}" if country_of_search else town
    search_text = f"{search} à {location}"
    print(f"\033[92m Récupération des infos {search_text} ...\033[0m")
    with create_driver() as driver:
        soup = get_entreprises_html_section(driver, search_text)
    entreprises = get_all_entreprises_infos(soup)
    data = href_checker(entreprises)
    load_data(search_text, data, country_of_search, town)
    print(f"\033[92m \u2714 ({search_text}: {country_of_search}): enregistré \033[0m")
