from includes.logic import scrape_activities_data as scrape_activities_data
from includes.logic import simple_search as simple_search
from includes.logic import activities   # list [] of all g_maps activities
from includes.files_treater import merge_csv_files


# Listes des activités disponibles
# Vous pouvez ajouter ou supprimer des activités selon vos besoins
# all_activities = activities
all_activities = ['Cabinet']

# Appels aux fonctions pour réaliser les opérations spécifiques
# Commentez ou décommentez les fonctions en fonction de vos objectifs

# Exemple 1: Scraper les données pour toutes les activités dans une région spécifique
# Remplir d'abord les données du dictionnaire quartiers in includes/world_map.py

# scrape_activities_data(
#     all_activities, country_of_search='Martinique', town='Fort-de-France')
# Possible de spécifier le paramètre town dans la fonction pour faire la recherche que dans une ville du pays

# Exemple 2: Effectuer une recherche simple pour une requête spécifique
simple_search(search="Restaurant",
              country_of_search='France', town='Lyon')

# Fusionner tous les fichiers CSV dans un seul fichier
# merge_csv_files('Benin', 'agence_voyage_tourisme')

# L'interface utilisateur sera développée ultérieurement avec Symfony
# Le projet est en cours de développement et est prévu pour x dates
