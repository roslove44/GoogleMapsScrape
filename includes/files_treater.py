import csv
import os
from tqdm import tqdm


def merge_csv_files(folder, output_file_name):
    folder_path = f'result/{folder}'
    output_file = f'result/{folder}/merge/{output_file_name}.csv'
    if not os.path.exists(f'result/{folder}/merge'):
        os.makedirs(f'result/{folder}/merge')
    # Obtenez la liste de tous les fichiers CSV dans le dossier spécifié
    csv_files = [file for file in os.listdir(
        folder_path) if file.endswith('.csv')]

    # Vérifiez s'il y a des fichiers à fusionner
    if not csv_files:
        print("Aucun fichier CSV trouvé dans le dossier spécifié.")
        return

    # Lire le premier fichier pour obtenir les en-têtes des colonnes
    first_file = os.path.join(folder_path, csv_files[0])
    with open(first_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

    # Fusionner les données des fichiers CSV dans un fichier unique
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        index = 1  # Nouvelle valeur de l'index
        for csv_file in tqdm(csv_files, desc="Traitement"):
            file_path = os.path.join(folder_path, csv_file)
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Modifier la valeur de l'index pour chaque ligne
                for row in reader:
                    row['index'] = index
                    writer.writerow(row)
                    index += 1

    print(f"Données fusionnées avec succès dans le fichier {output_file}.")
