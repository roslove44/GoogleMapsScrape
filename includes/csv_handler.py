import csv
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from includes.utils import is_valid_domain, is_valid_phone_number
from includes.driver import create_driver


def merge_csv_files(folder, output_file_name):
    folder_path = f'result/{folder}'
    output_file = f'result/{folder}/merge/{output_file_name}.csv'
    if not os.path.exists(f'result/{folder}/merge'):
        os.makedirs(f'result/{folder}/merge')

    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        print("Aucun fichier CSV trouvé dans le dossier spécifié.")
        return

    first_file = os.path.join(folder_path, csv_files[0])
    with open(first_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        index = 1
        for csv_file in tqdm(csv_files, desc="Traitement"):
            file_path = os.path.join(folder_path, csv_file)
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['index'] = index
                    writer.writerow(row)
                    index += 1

    print(f"Données fusionnées avec succès dans le fichier {output_file}.")


def transform_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        entreprises = list(reader)

    for entreprise in entreprises:
        transition_value = entreprise.get('transition', '')
        if "https://www.google.com/maps/" in transition_value:
            html_content = None
            with create_driver(headless=True) as driver:
                try:
                    driver.get(transition_value)
                    WebDriverWait(driver, 10).until(
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
                            elif is_valid_domain(text):
                                print(text)
                                entreprise.update({"web_site": text})
                    else:
                        print("Élément avec le sélecteur donné non trouvé.")
                except Exception as e:
                    print(f"Erreur lors du parsing : {e}")

    with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = entreprises[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entreprises)
