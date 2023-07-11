import pyjson5
# import requests
# from bs4 import BeautifulSoup
# import csv


def get_cities(country):
    if (country in quartiers):
        return list(quartiers[country])
    else:
        print(f"Aucune Correspondance pour {country}")
        exit()


def get_france_cities():
    with open("assets/france.json", "r", encoding='utf-8') as file:
        json_data = file.read()
    data = pyjson5.loads(json_data)
    libelle_acheminement_list = list(
        set([item["Libelle_acheminement"] for item in data]))

    return libelle_acheminement_list


france_cities = get_france_cities()


quartiers = {
    "France": france_cities,
    "Côte d'Ivoire": ["Abidjan"],
    "Bénin": ["Cotonou"]
}


def extract_activities_from_csv():
    activities = []
    with open('activities.csv', mode='r', newline='', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Supprimer les espaces en début et fin de ligne
            activities.append(line)
    return activities


activities = extract_activities_from_csv()

# activities = []
# def extract_soup(url):
#     # Cette fonction extrait le contenu HTML d'une URL donnée.
#     # Elle envoie une requête à l'URL et récupère la réponse.
#     response = requests.get(url)
#     html_response = response.content
#     soup = BeautifulSoup(html_response, 'html.parser').find_all('td')
#     for td in soup:
#         activities.append(td.get_text())


# extract_soup('https://www.debugbar.com/fr/categories-google-my-business/')


# def save_activities_to_csv(activities):
#     with open('assets/activities.csv', mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         for activity in activities:
#             writer.writerow([activity])


# save_activities_to_csv(activities)
