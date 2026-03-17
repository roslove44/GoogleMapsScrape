from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import includes.geo as geo
from includes.csv_handler import load_data
from includes.utils import (
    is_valid_domain, is_valid_phone_number,
    get_text_or_na, celebrity_indice
)
from includes.driver import create_driver
from includes.i18n import t

activities = geo.activities


# ✔ tested and working
def parse_single_entreprise(soup, transition_url):
    """Parse la fiche d'une entreprise unique."""
    name = get_text_or_na(soup.select_one('h1.DUwDvf.lfPIob'))
    average_note = get_text_or_na(soup.select_one('div.F7nice span[aria-hidden="true"]'))
    vote_count_els = soup.select('div.F7nice span span[role="img"]')
    vote_count_el = vote_count_els[1] if len(vote_count_els) >= 2 else None
    vote_count = vote_count_el.get_text(strip=True) if vote_count_el else "N/A"
    activity = get_text_or_na(soup.select_one('button.DkEaL'))
    ic = celebrity_indice(vote_count, average_note)

    address = "N/A"
    phone_number = "N/A"
    web_site = "N/A"

    sections = soup.select('div.m6QErb.XiKgde[role="region"]')
    if len(sections) >= 2:
        details = sections[1].find_all('div', class_=['Io6YTe', 'fontBodyMedium', 'kR99db'])
        if details:
            address = get_text_or_na(details[0])
        for tag in details[1:]:
            text = tag.get_text(strip=True)
            if phone_number == "N/A" and is_valid_phone_number(text):
                phone_number = text
            elif web_site == "N/A" and is_valid_domain(text):
                web_site = text

    return [{
        'name': name,
        'activity': activity,
        'celebrity_indice': f"{average_note} {vote_count}",
        'ic': ic,
        'phone_number': phone_number,
        'web_site': web_site,
        'address': address,
        'transition': transition_url
    }]


def get_entreprises_html_section(driver, search_text, lang="fr"):
    from selenium.common.exceptions import TimeoutException

    FEED_SELECTOR = "div[role='feed']"
    REGION_SELECTOR = 'div.m6QErb.XiKgde[role="region"]'
    OMNIBOX_SELECTOR = "#omnibox-directions, #directions-searchbox-0, #directions-searchbox-1"
    END_OF_LIST_SELECTOR = "div.m6QErb.tLjsW.eKbjU"

    driver.get(f"https://www.google.com/maps/?hl={lang}")

    # Accepter la page de consentement cookies Google si elle apparaît
    try:
        accept_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//form[contains(@action,'consent')]//button"))
        )
        accept_btn.click()
    except TimeoutException:
        pass

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='q']"))
    )
    search_box = driver.find_element(By.CSS_SELECTOR, "input[name='q']")
    search_box.send_keys(search_text)
    search_box.send_keys(Keys.ENTER)

    # Attendre qu'un indicateur de résultat apparaisse
    try:
        WebDriverWait(driver, 10).until(
            lambda d: (
                d.find_elements(By.CSS_SELECTOR, FEED_SELECTOR) or
                d.find_elements(By.CSS_SELECTOR, REGION_SELECTOR) or
                d.find_elements(By.CSS_SELECTOR, OMNIBOX_SELECTOR)
            )
        )
    except TimeoutException:
        return None

    # Cas entreprises : liste avec scroll infini
    if driver.find_elements(By.CSS_SELECTOR, FEED_SELECTOR):
        container = driver.find_element(By.CSS_SELECTOR, FEED_SELECTOR)
        while not driver.find_elements(By.CSS_SELECTOR, END_OF_LIST_SELECTOR):
            driver.execute_script("arguments[0].scrollBy(0, 400)", container)
            time.sleep(1)

        section_html = container.get_attribute("innerHTML")
        cards = BeautifulSoup(section_html, 'html.parser').find_all('div', class_=['Nv2PK', 'Q2HXcd', 'THOPZb'])
        return ("entreprises", cards)

    # Cas another_country : skip
    if driver.find_elements(By.CSS_SELECTOR, OMNIBOX_SELECTOR):
        return None

    # Cas single (2+ regions) ou region (1 seule → skip)
    try:
        WebDriverWait(driver, 3).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, REGION_SELECTOR)) >= 2
        )
    except TimeoutException:
        return None

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return ("single", parse_single_entreprise(soup, driver.current_url))


# ✔ tested and working
def get_all_entreprises_infos(soup):
    entreprises = []
    if soup:
        for entreprise_infos in soup:
            name = get_text_or_na(entreprise_infos.select_one(
                'div.NrDZNb div.qBF1Pd.fontHeadlineSmall'))
            average_note = get_text_or_na(
                entreprise_infos.select_one('span[role="img"].ZkP5Je span.MW4etd'))
            vote_count = get_text_or_na(
                entreprise_infos.select_one('span[role="img"].ZkP5Je span.UY7F9'))
            activity = get_text_or_na(entreprise_infos.select_one(
                'div.W4Efsd div.W4Efsd span:first-child > span'))
            phone_number = get_text_or_na(entreprise_infos.select_one('.UaQhfb.fontBodyMedium .W4Efsd + .W4Efsd > .W4Efsd + .W4Efsd > span:last-child > span:last-child'))
            if phone_number != "N/A" and not is_valid_phone_number(phone_number):
                phone_number = "N/A"
            href_element = entreprise_infos.select_one('.lI9IFe .Rwjeuc a.lcr4fd.S9kvJb')
            href = href_element.get('href') if href_element else "N/A"
            address = get_text_or_na(entreprise_infos.select_one(
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


# ✔ tested and working
def href_checker(entreprises):
    from selenium.common.exceptions import TimeoutException, WebDriverException

    with create_driver(headless=True) as driver:
        for entreprise in tqdm(entreprises, desc="Entreprises"):
            if "https://www.google.com/maps/" not in entreprise['transition']:
                continue
            if entreprise['phone_number'] != "N/A" and entreprise['web_site'] != "N/A":
                continue

            try:
                driver.get(entreprise['transition'])
                WebDriverWait(driver, 5).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, 'div.m6QErb.XiKgde[role="region"]')) >= 2
                )
            except (TimeoutException, WebDriverException) as e:
                print(t("selenium_error", error=e))
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            sections = soup.select('div.m6QErb.XiKgde[role="region"]')
            if len(sections) < 2:
                print(t("insufficient_regions"))
                continue

            for tag in sections[1].find_all('div', class_=['Io6YTe', 'fontBodyMedium', 'kR99db']):
                text = tag.get_text(strip=True)
                if entreprise['phone_number'] == "N/A" and is_valid_phone_number(text):
                    entreprise['phone_number'] = text
                elif entreprise['web_site'] == "N/A" and is_valid_domain(text):
                    entreprise['web_site'] = text
    return entreprises


def scrape_activities_data(activities: list, country_of_search: str, town: list = None, lang: str = "fr"):
    cities = geo.get_cities(country_of_search)
    if town is not None and isinstance(town, list):
        cities = town

    with create_driver() as driver:
        for city in tqdm(cities, desc='Cities'):
            for activity in tqdm(activities, desc="Activities"):
                location = f"{city} {country_of_search}" if country_of_search else city
                search_text = f"{activity} à {location}"
                print(t("fetching_info", search_text=f"{activity} à {location}"))
                result = get_entreprises_html_section(driver, search_text, lang=lang)
                if result is None:
                    print(t("no_result", search_text=f"{activity} à {city}"))
                    continue
                page_type, data = result
                if page_type == "entreprises":
                    entreprises = get_all_entreprises_infos(data)
                    entreprises = href_checker(entreprises)
                else:
                    entreprises = data
                load_data(search_text, entreprises, country_of_search, city)
                print(t("saved", search_text=f"{activity} à {city}"))


# ✔ tested and working
def simple_search(search: str, country_of_search: str = None, town: str = None, neighborhood: str = None, lang: str = "fr"):
    location = " ".join(p for p in [neighborhood, town, country_of_search] if p)
    search_text = f"{search} à {location}" if location else search
    print(t("fetching_info", search_text=search_text))
    with create_driver() as driver:
        result = get_entreprises_html_section(driver, search_text, lang=lang)
    if result is None:
        print(t("no_result", search_text=search_text))
        return
    page_type, data = result
    if page_type == "entreprises":
        entreprises = get_all_entreprises_infos(data)
        entreprises = href_checker(entreprises)
    else:
        entreprises = data
    load_data(search_text, entreprises, country_of_search or "", town or "")
    print(t("saved", search_text=search_text))
