from includes.logic import scrape_activities_data as scrape_activities_data
from includes.logic import simple_search as simple_search
from includes.logic import activities

simple_search('salle de cinéma cotonou', "Bénin")
activities = activities[17:]
# scrape_activities_data(activities, "Bénin")
