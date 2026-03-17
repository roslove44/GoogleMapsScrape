_lang = "fr"

MESSAGES = {
    "fr": {
        # scraper
        "fetching_info":        "\033[92m Récupération des infos {search_text} ...\033[0m",
        "no_result":            "\033[93m ⚠ ({search_text}): aucun résultat\033[0m",
        "saved":                "\033[92m ✔ ({search_text}): enregistré \033[0m",
        "selenium_error":       "Erreur lors de l'extraction de l'URL avec Selenium : {error}",
        "insufficient_regions": "Sections région insuffisantes.",
        # csv_handler
        "no_csv_found":         "Aucun fichier CSV trouvé dans le dossier spécifié.",
        "merge_success":        "Données fusionnées avec succès dans le fichier {file}.",
        # geo
        "no_country_match":     "\033[93m\u2718 Aucune Correspondance pour {country}.\n  Ajoutez le dans dictionnaire geo.quartiers \033[0m",
        # main
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
        "menu_title":           "Que voulez-vous faire ?",
        "menu_search":          "  [1] Recherche simple            (simple_search)",
        "menu_scrape":          "  [2] Scraper des activités       (scrape_activities_data)",
        "menu_merge":           "  [3] Fusionner des CSV           (merge_csv_files)",
        "search_query":         "Terme à rechercher (ex: Pâtisserie) : ",
        "search_country":       "Pays (ex: Bénin) : ",
        "search_town":          "Ville (ex: Cotonou) : ",
        "search_neighborhood":  "Quartier, optionnel (ex: Ganhi) : ",
        "scrape_country":       "Pays : ",
        "scrape_town_choice":   "Villes : ",
        "scrape_town_all":      "Toutes les villes du pays ({count})",
        "scrape_town_custom":   "Saisir manuellement",
        "scrape_town_input":    "Ville(s) séparées par des virgules : ",
        "scrape_act_choice":    "Activités : ",
        "scrape_act_all":       "Toutes les activités ({count})",
        "scrape_act_custom":    "Saisir manuellement",
        "scrape_act_input":     "Activités séparées par des virgules : ",
        "merge_folder":         "Nom du dossier dans result/ (ex: France) : ",
        "merge_output":         "Nom du fichier de sortie sans .csv (ex: resultats_finaux) : ",
        "hint_search":          "Recherche un terme libre sur Google Maps pour une ville donnée\n  et exporte les résultats en CSV.",
        "hint_scrape":          "Scrape une ou plusieurs activités dans toutes les villes d'un pays\n  (ou une ville précise) et exporte les résultats en CSV.",
        "hint_merge":           "Fusionne tous les fichiers CSV d'un dossier result/<pays>/\n  en un seul fichier dans result/<pays>/merge/.",
        "info_limit":           "\n  \033[93mi. Google Maps limite les résultats à ~120 par recherche.\n  Pour de meilleurs résultats, découpez vos recherches par quartier\n  plutôt que par grande ville.\033[0m\n",
    },
    "en": {
        # scraper
        "fetching_info":        "\033[92m Fetching info {search_text} ...\033[0m",
        "no_result":            "\033[93m ⚠ ({search_text}): no results\033[0m",
        "saved":                "\033[92m ✔ ({search_text}): saved \033[0m",
        "selenium_error":       "Error extracting URL with Selenium: {error}",
        "insufficient_regions": "Insufficient region sections.",
        # csv_handler
        "no_csv_found":         "No CSV files found in the specified folder.",
        "merge_success":        "Data successfully merged into {file}.",
        # geo
        "no_country_match":     "\033[93m\u2718 No match for {country}.\n  Add it to the geo.quartiers dictionary \033[0m",
        # main
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
        "menu_title":           "What do you want to do?",
        "menu_search":          "  [1] Simple search               (simple_search)",
        "menu_scrape":          "  [2] Scrape activities            (scrape_activities_data)",
        "menu_merge":           "  [3] Merge CSV files              (merge_csv_files)",
        "search_query":         "Search term (e.g. Bakery): ",
        "search_country":       "Country (e.g. Benin): ",
        "search_town":          "City (e.g. Cotonou): ",
        "search_neighborhood":  "Neighborhood, optional (e.g. Ganhi): ",
        "scrape_country":       "Country: ",
        "scrape_town_choice":   "Cities: ",
        "scrape_town_all":      "All cities in the country ({count})",
        "scrape_town_custom":   "Enter manually",
        "scrape_town_input":    "City/cities separated by commas: ",
        "scrape_act_choice":    "Activities: ",
        "scrape_act_all":       "All activities ({count})",
        "scrape_act_custom":    "Enter manually",
        "scrape_act_input":     "Activities separated by commas: ",
        "merge_folder":         "Folder name in result/ (e.g. France): ",
        "merge_output":         "Output file name without .csv (e.g. final_results): ",
        "hint_search":          "Searches a keyword on Google Maps for a given city\n  and exports results to CSV.",
        "hint_scrape":          "Scrapes one or more activities across all cities in a country\n  (or a specific city) and exports results to CSV.",
        "hint_merge":           "Merges all CSV files from a result/<country>/ folder\n  into a single file in result/<country>/merge/.",
        "info_limit":           "\n  \033[93mi. Google Maps limits results to ~120 per search.\n  For better results, split your searches by neighborhood\n  rather than by large city.\033[0m\n",
    }
}


def set_lang(lang):
    global _lang
    _lang = lang


def t(key, **kwargs):
    message = MESSAGES.get(_lang, MESSAGES["fr"]).get(key, key)
    return message.format(**kwargs) if kwargs else message
