import os
import sys
from InquirerPy import inquirer
from includes.scraper import scrape_activities_data, simple_search, activities
from includes.csv_handler import merge_csv_files

TRANSLATIONS = {
    "fr": {
        "chromedriver_missing": (
            "\n\033[91m✘ chromedriver.exe introuvable à la racine du projet.\033[0m\n"
            "\n"
            "  ChromeDriver est requis pour que le scraper puisse piloter Chrome.\n"
            "  Téléchargez la version correspondant à votre navigateur Chrome :\n"
            "\n"
            "  \033[94mhttps://googlechromelabs.github.io/chrome-for-testing/\033[0m\n"
            "\n"
            "  Comment vérifier votre version de Chrome :\n"
            "    → Ouvrez Chrome > Menu (⋮) > Aide > À propos de Google Chrome\n"
            "\n"
            "  Placez ensuite le fichier chromedriver.exe téléchargé\n"
            "  à la racine du projet, au même niveau que main.py.\n"
        ),
        "menu_title":      "Que voulez-vous faire ?",
        "menu_search":     "  [1] Recherche simple            (simple_search)",
        "menu_scrape":     "  [2] Scraper des activités       (scrape_activities_data)",
        "menu_merge":      "  [3] Fusionner des CSV           (merge_csv_files)",
        "search_query":    "Terme à rechercher (ex: Pâtisserie) : ",
        "search_country":  "Pays (ex: Bénin) : ",
        "search_town":     "Ville (ex: Cotonou) : ",
        "search_neighborhood": "Quartier, optionnel (ex: Ganhi) : ",
        "scrape_country":  "Pays (ex: France) : ",
        "scrape_town":     "Ville(s) séparées par des virgules — laisser vide pour toutes : ",
        "scrape_act":      "Activités séparées par des virgules — laisser vide pour toutes : ",
        "merge_folder":    "Nom du dossier dans result/ (ex: France) : ",
        "merge_output":    "Nom du fichier de sortie sans .csv (ex: resultats_finaux) : ",
        "hint_search":     "Recherche un terme libre sur Google Maps pour une ville donnée\n  et exporte les résultats en CSV.",
        "hint_scrape":     "Scrape une ou plusieurs activités dans toutes les villes d'un pays\n  (ou une ville précise) et exporte les résultats en CSV.",
        "hint_merge":      "Fusionne tous les fichiers CSV d'un dossier result/<pays>/\n  en un seul fichier dans result/<pays>/merge/.",
        "info_limit":      "\n  \033[93mi. Google Maps limite les résultats à ~120 par recherche.\n  Pour de meilleurs résultats, découpez vos recherches par quartier\n  plutôt que par grande ville.\033[0m\n",
    },
    "en": {
        "chromedriver_missing": (
            "\n\033[91m✘ chromedriver.exe not found at the project root.\033[0m\n"
            "\n"
            "  ChromeDriver is required for the scraper to control Chrome.\n"
            "  Download the version matching your current Chrome browser:\n"
            "\n"
            "  \033[94mhttps://googlechromelabs.github.io/chrome-for-testing/\033[0m\n"
            "\n"
            "  How to check your Chrome version:\n"
            "    → Open Chrome > Menu (⋮) > Help > About Google Chrome\n"
            "\n"
            "  Then place the downloaded chromedriver.exe file\n"
            "  at the project root, next to main.py.\n"
        ),
        "menu_title":      "What do you want to do?",
        "menu_search":     "  [1] Simple search               (simple_search)",
        "menu_scrape":     "  [2] Scrape activities            (scrape_activities_data)",
        "menu_merge":      "  [3] Merge CSV files              (merge_csv_files)",
        "search_query":    "Search term (e.g. Bakery): ",
        "search_country":  "Country (e.g. Benin): ",
        "search_town":     "City (e.g. Cotonou): ",
        "search_neighborhood": "Neighborhood, optional (e.g. Ganhi): ",
        "scrape_country":  "Country (e.g. France): ",
        "scrape_town":     "City/cities separated by commas — leave empty for all: ",
        "scrape_act":      "Activities separated by commas — leave empty for all: ",
        "merge_folder":    "Folder name in result/ (e.g. France): ",
        "merge_output":    "Output file name without .csv (e.g. final_results): ",
        "hint_search":     "Searches a keyword on Google Maps for a given city\n  and exports results to CSV.",
        "hint_scrape":     "Scrapes one or more activities across all cities in a country\n  (or a specific city) and exports results to CSV.",
        "hint_merge":      "Merges all CSV files from a result/<country>/ folder\n  into a single file in result/<country>/merge/.",
        "info_limit":      "\n  \033[93mi. Google Maps limits results to ~120 per search.\n  For better results, split your searches by neighborhood\n  rather than by large city.\033[0m\n",
    }
}


def print_hint(fn_name, description):
    line = "─" * 52
    print(f"\n  \033[36m{line}\033[0m")
    print(f"  \033[1;36m  {fn_name}\033[0m")
    print(f"  \033[2m  {description}\033[0m")
    print(f"  \033[36m{line}\033[0m\n")


def get_lang():
    lang = inquirer.select(qmark="", amark=">",
        message="Choisissez votre langue / Choose your language:",
        choices=[
            {"name": "Français", "value": "fr"},
            {"name": "English", "value": "en"},
        ],
    ).execute()
    return lang


def check_chromedriver(t):
    if not os.path.isfile("chromedriver.exe"):
        print(t["chromedriver_missing"])
        sys.exit(1)


def main():
    lang = get_lang()
    t = TRANSLATIONS[lang]

    check_chromedriver(t)
    print(t["info_limit"])

    choice = inquirer.select(qmark="", amark=">",
        message=t["menu_title"],
        choices=[
            {"name": t["menu_search"], "value": "search"},
            {"name": t["menu_scrape"], "value": "scrape"},
            {"name": t["menu_merge"], "value": "merge"},
        ],
    ).execute()

    if choice == "search":
        print_hint("simple_search", t["hint_search"])
        query        = inquirer.text(qmark="", amark=">",message=t["search_query"], validate=lambda x: len(x.strip()) > 0).execute()
        country      = inquirer.text(qmark="", amark=">",message=t["search_country"]).execute()
        town         = inquirer.text(qmark="", amark=">",message=t["search_town"]).execute()
        neighborhood = inquirer.text(qmark="", amark=">",message=t["search_neighborhood"]).execute()
        simple_search(search=query, country_of_search=country or None, town=town or None, neighborhood=neighborhood or None, lang=lang)

    elif choice == "scrape":
        print_hint("scrape_activities_data", t["hint_scrape"])
        country    = inquirer.text(qmark="", amark=">",message=t["scrape_country"]).execute()
        town_input = inquirer.text(qmark="", amark=">",message=t["scrape_town"]).execute()
        act_input  = inquirer.text(qmark="", amark=">",message=t["scrape_act"]).execute()
        town       = [v.strip() for v in town_input.split(",")] if town_input else None
        all_activities = [v.strip() for v in act_input.split(",")] if act_input else activities
        scrape_activities_data(all_activities, country_of_search=country, town=town, lang=lang)

    elif choice == "merge":
        print_hint("merge_csv_files", t["hint_merge"])
        folder = inquirer.text(qmark="", amark=">",message=t["merge_folder"]).execute()
        output = inquirer.text(qmark="", amark=">",message=t["merge_output"]).execute()
        merge_csv_files(folder, output)


if __name__ == "__main__":
    main()
