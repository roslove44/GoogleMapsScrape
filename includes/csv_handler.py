import csv
import os
from tqdm import tqdm
from includes.i18n import t


def merge_csv_files(folder, output_file_name):
    folder_path = f'result/{folder}'
    output_file = f'result/{folder}/merge/{output_file_name}.csv'
    if not os.path.exists(f'result/{folder}/merge'):
        os.makedirs(f'result/{folder}/merge')

    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        print(t("no_csv_found"))
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

    print(t("merge_success", file=output_file))


def _sanitize_name(text):
    for char in "-/ :|":
        text = text.replace(char, "_")
    return text.strip()


def load_data(search_text, entreprises, country_of_search, town):
    title = _sanitize_name(search_text)
    folder = _sanitize_name(country_of_search)
    os.makedirs(f'result/{folder}', exist_ok=True)
    with open(f'result/{folder}/{title}.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['index', 'name', 'activity', 'celebrity_indice', 'ic', 'phone_number', 'web_site', 'address', 'town', 'transition']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for index, entreprise in enumerate(entreprises, start=1):
            row = {**entreprise, 'town': town, 'index': index}
            writer.writerow(row)
