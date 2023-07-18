import pyjson5
import os

# Récupère la liste des villes pour un pays donné
# Si le pays n'est pas trouvé dans le dictionnaire, affiche un message d'erreur et quitte le programme


def get_cities(country):
    if (country in quartiers):
        return list(quartiers[country])
    else:
        print(
            '\033[93m' +
            f"\u2718 Aucune Correspondance pour {country}. \n  Ajoutez le dans dictionnaire world_map.quartiers "
            + '\033[0m')
        exit()


# Récupère la liste des villes pour la France à partir d'un fichier JSON plus de 3000 villes impossible de tout stocker dans une liste en dur
def get_france_cities():
    file_path = os.path.join(os.path.dirname(
        __file__), '../assets/france.json')
    with open(file_path, "r", encoding='utf-8') as file:
        json_data = file.read()
    data = pyjson5.loads(json_data)
    libelle_acheminement_list = list(
        set([item["Libelle_acheminement"] for item in data]))

    return libelle_acheminement_list


france_cities = get_france_cities()

# Dictionnaire des villes pour chaque pays : flemme de renommer
quartiers = {
    "France": france_cities,
    "Côte d'Ivoire": ["Abidjan"],
    "Bénin": ["Cotonou"]
}

# Extraction des activités à partir d'un fichier CSV


def extract_activities_from_csv():
    file_path = os.path.join(os.path.dirname(
        __file__), '../assets/activities.csv')
    activities = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Supprimer les espaces en début et fin de ligne
            activities.append(line)
    return activities


# Liste des activités extraites du fichier CSV
activities = extract_activities_from_csv()
