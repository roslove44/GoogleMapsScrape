import os
import sys
from InquirerPy import inquirer
from includes.scraper import scrape_activities_data, simple_search, activities
from includes.csv_handler import merge_csv_files
from includes.i18n import set_lang, t


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


def check_chromedriver():
    if not os.path.isfile("chromedriver.exe"):
        print(t("chromedriver_missing"))
        sys.exit(1)


def main():
    lang = get_lang()
    set_lang(lang)

    check_chromedriver()
    print(t("info_limit"))

    choice = inquirer.select(qmark="", amark=">",
        message=t("menu_title"),
        choices=[
            {"name": t("menu_search"), "value": "search"},
            {"name": t("menu_scrape"), "value": "scrape"},
            {"name": t("menu_merge"), "value": "merge"},
        ],
    ).execute()

    if choice == "search":
        print_hint("simple_search", t("hint_search"))
        query        = inquirer.text(qmark="", amark=">", message=t("search_query"), validate=lambda x: len(x.strip()) > 0).execute()
        country      = inquirer.text(qmark="", amark=">", message=t("search_country")).execute()
        town         = inquirer.text(qmark="", amark=">", message=t("search_town")).execute()
        neighborhood = inquirer.text(qmark="", amark=">", message=t("search_neighborhood")).execute()
        simple_search(search=query, country_of_search=country or None, town=town or None, neighborhood=neighborhood or None, lang=lang)

    elif choice == "scrape":
        print_hint("scrape_activities_data", t("hint_scrape"))
        country    = inquirer.text(qmark="", amark=">", message=t("scrape_country")).execute()
        town_input = inquirer.text(qmark="", amark=">", message=t("scrape_town")).execute()
        act_input  = inquirer.text(qmark="", amark=">", message=t("scrape_act")).execute()
        town       = [v.strip() for v in town_input.split(",")] if town_input else None
        all_activities = [v.strip() for v in act_input.split(",")] if act_input else activities
        scrape_activities_data(all_activities, country_of_search=country, town=town, lang=lang)

    elif choice == "merge":
        print_hint("merge_csv_files", t("hint_merge"))
        folder = inquirer.text(qmark="", amark=">", message=t("merge_folder")).execute()
        output = inquirer.text(qmark="", amark=">", message=t("merge_output")).execute()
        merge_csv_files(folder, output)


if __name__ == "__main__":
    main()
