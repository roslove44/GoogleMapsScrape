from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import tldextract
import re
import csv


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


def transform_csv(file_path):
    # Lire le fichier CSV d'entrée
    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        entreprises = list(reader)

    # Effectuer des transformations sur chaque ligne
    for entreprise in entreprises:
        transition_value = entreprise.get('transition', '')

        # Exemple d'action personnalisée basée sur la valeur de 'transition'
        if "https://www.google.com/maps/" in transition_value:
            # Remplacez par la nouvelle valeur
            html_content = extract_html_content_with_selenium(transition_value)
            if html_content:
                # Parse le HTML avec BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

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
                                entreprise.update({"phone_number": text})
                                print(entreprise["phone_number"])
                            elif is_valid_domain(text):
                                print(text)
                                entreprise.update({"web_site": text})
                    else:
                        print("Élément avec le sélecteur donné non trouvé.")
                except Exception as e:
                    print(f"Erreur lors du parsing : {e}")

    # Écrire les données mises à jour dans le fichier CSV (ou un nouveau fichier)
    with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = entreprises[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(entreprises)


# Exemple d'utilisation
# Remplacez par votre chemin réel
file_path = ''
transform_csv(file_path)
