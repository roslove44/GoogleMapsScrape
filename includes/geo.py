import pyjson5
import os


def get_cities(country):
    if country in quartiers:
        return list(quartiers[country])
    else:
        print(
            '\033[93m' +
            f"\u2718 Aucune Correspondance pour {country}. \n  Ajoutez le dans dictionnaire geo.quartiers "
            + '\033[0m')
        raise SystemExit(1)


def get_france_cities():
    file_path = os.path.join(os.path.dirname(__file__), '../assets/france.json')
    with open(file_path, "r", encoding='utf-8') as file:
        json_data = file.read()
    data = pyjson5.loads(json_data)
    libelle_acheminement_list = list(
        set([item["Libelle_acheminement"] for item in data]))
    return libelle_acheminement_list


france_cities = get_france_cities()

quartiers = {
    "France": france_cities,
    "Côte d'Ivoire": ["Abidjan"],
    "Bénin": ["Cotonou", "Abomey-Calavi", "Porto-Novo"],
    "Martinique": ["Fort-de-France"]
}


def extract_activities_from_csv():
    file_path = os.path.join(os.path.dirname(__file__), '../assets/activities.csv')
    activities = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            activities.append(line)
    return activities


activities = extract_activities_from_csv()
