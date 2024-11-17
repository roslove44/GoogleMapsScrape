from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import tldextract
import re


def extract_html_content_with_selenium(url):
    """
    Cette fonction utilise Selenium pour récupérer le contenu HTML d'une page web dynamique.
    """
    # Configuration de Selenium
    chrome_options = Options()
    # Mode headless pour exécuter sans interface graphique
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Charger l'URL
        driver.get(url)

        # Attendre que l'élément cible soit chargé (10 secondes max)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div"))
        )

        # Récupérer le contenu HTML
        html_content = driver.page_source
        return html_content

    except Exception as e:
        print(f"Erreur lors de l'extraction de l'URL avec Selenium : {e}")
        return None
    finally:
        driver.quit()


def is_valid_domain(domain):
    extracted = tldextract.extract(domain)
    return bool(extracted.domain and extracted.suffix)


def is_valid_phone_number(phone_number):
    # Modèle de numéro de téléphone avec des chiffres, des espaces et éventuellement le symbole "+"
    pattern = r'^\+?[\d\s]+$'
    return bool(re.match(pattern, phone_number))


url = "https://www.google.com/maps/place/SPHERE+Restaurant+Paris/@48.87427,2.3143638,17z/data=!3m2!4b1!5s0x47e66fc976f71e0f:0x9acef3ed0845fd65!4m6!3m5!1s0x47e66f4c47058947:0xe1de61d4b89d1efb!8m2!3d48.8742665!4d2.3169387!16s%2Fg%2F11t77k7nft?entry=ttu&g_ep=EgoyMDI0MTExMy4xIKXMDSoASAFQAw%3D%3D"

# Récupérer le contenu HTML avec Selenium
html_content = extract_html_content_with_selenium(url)

if html_content:
    # Parse le HTML avec BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Sélection d'un élément CSS
    try:
        section_html = soup.select_one(
            '#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div'
        )
        if section_html:
            section_parse = section_html.find_all(
                'div', class_=['Io6YTe', 'fontBodyMedium', 'kR99db']
            )
            for tag in section_parse:
                text = tag.get_text()
                if is_valid_phone_number(text):
                    print(text)
                elif is_valid_domain(text):
                    print(text)
        else:
            print("Élément avec le sélecteur donné non trouvé.")
    except Exception as e:
        print(f"Erreur lors du parsing : {e}")
