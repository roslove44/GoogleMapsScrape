import pyjson5


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
}
