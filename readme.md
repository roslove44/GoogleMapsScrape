# Application de scraping d'informations sur les entreprises

Cette application permet de récupérer des informations sur les entreprises à partir de Google Maps. Elle utilise Selenium pour automatiser la navigation et le scraping des données.

## Installation

1. Clonez ce dépôt sur votre machine :

```bash
git clone link
```

````

2. Assurez-vous d'avoir Python 3 installé sur votre machine.

3. Installez les dépendances requises à l'aide de pip :

```bash
pip install -r requirements.txt
```

## Configuration

Avant d'exécuter l'application, vous devez configurer les paramètres de recherche. Les fichiers de configuration se trouvent dans le répertoire `config/`.

1. `activities.csv` : Ce fichier contient la liste des activités à rechercher. Vous pouvez modifier cette liste en ajoutant ou en supprimant des activités.

2. `world_map.py` : Ce fichier contient les données de configuration pour les pays et les villes à rechercher. Vous pouvez ajouter de nouveaux pays et villes en les définissant dans ce fichier.

## Utilisation

L'application fournit deux méthodes de recherche :

1. Recherche par activité et pays :

```bash
python main.py scrape_activities_data()
```


2. Recherche simple par terme et pays :

```bash
python main.py simple_search()
```


Les résultats de la recherche seront enregistrés dans le répertoire `result/{country_of_search}/` sous forme de fichiers CSV.

## Contribution

Les contributions sont les bienvenues ! Si vous souhaitez améliorer cette application, n'hésitez pas à créer une pull request.

## Licence

Ce projet est sous licence MIT. Veuillez consulter le fichier `LICENSE` pour plus d'informations.

```

Ce modèle de fichier README.md fournit une structure de base pour présenter l'application, expliquer l'installation et l'utilisation, ainsi que mentionner les contributions et la licence. Vous pouvez personnaliser le contenu en fonction de vos besoins spécifiques et ajouter des sections supplémentaires si nécessaire.
```
````
