# Application de scraping d'informations sur les entreprises

Cette application permet de récupérer des informations sur les entreprises à partir de Google Maps. Elle utilise Selenium pour automatiser la navigation et le scraping des données.

## Installation

1. Clonez ce dépôt sur votre machine :
git clone [https://github.com/roslove44/GoogleMapsScrape.git
](https://github.com/roslove44/GoogleMapsScrape.git)

2. Assurez-vous d'avoir Python 3 installé sur votre machine.

3. Installez les dépendances requises à l'aide de pip :
pip install -r requirements.txt


## Configuration

Avant d'exécuter l'application, vous devez configurer les paramètres de recherche. Les fichiers de configuration se trouvent dans le répertoire `includes/`.

1. `activities.csv` : Ce fichier contient la liste des activités que vous souhaitez rechercher. Chaque activité doit être sur une ligne séparée.

2. `world_map.py` : Ce fichier contient la configuration des pays et des villes pour lesquels vous souhaitez effectuer la recherche. Vous pouvez ajouter ou modifier des pays et leurs villes correspondantes dans le dictionnaire `quartiers`.



L'application commencera à récupérer les informations sur les entreprises en fonction des paramètres de recherche configurés. Les résultats seront enregistrés dans le dossier `result/` avec des fichiers CSV pour chaque recherche effectuée.

## Améliorations possibles

Voici quelques suggestions d'améliorations possibles pour cette application :

- Ajouter une interface utilisateur pour faciliter la configuration des paramètres de recherche.
- Implémenter la parallélisation pour accélérer le processus de scraping.
- Intégrer une base de données pour stocker les résultats de manière persistante.
- Ajouter des fonctionnalités supplémentaires telles que la recherche par catégorie ou la géolocalisation.

N'hésitez pas à contribuer à ce projet en proposant vos propres améliorations ou en soumettant des problèmes rencontrés.

## Licence

Ce projet est sous licence MIT. Veuillez consulter le fichier `LICENSE` pour plus d'informations.

