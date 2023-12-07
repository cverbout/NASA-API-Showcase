from flask import request, render_template
from flask.views import MethodView
import requests
import random
from dotenv import load_dotenv
import os

class Map(MethodView):
    def get(self):
        """
        Renders map.html page
        """
        load_dotenv()
        google_api_key = os.getenv("GOOGLE_API_KEY")
        URL_events = "https://eonet.gsfc.nasa.gov/api/v2.1/events"
        URL_categories = "https://eonet.gsfc.nasa.gov/api/v2.1/categories"
        limit = request.args.get('limit', default=None)
        days = request.args.get('days', default=None)
        URL_events = urlMaker(URL_events, limit, days)
        map_data = organizeMapData(URL_events)
        category_data=markerInfo(URL_categories)

        return render_template('map.html', map_data=map_data, category_data=category_data, GOOGLE_API_KEY=google_api_key)

def urlMaker(URL_events, limit, days):
    """
    String URL_events
    INT limit
    INT days
    
    Takes in a limit and days and accordingly alters the NASA events URL.
    Returns a string
    """
   
    if limit != None:
        URL_events += "?limit=" + str(limit)
        if days != None:
            URL_events += "&days=" + str(days)
    elif days != None:
            URL_events += "?days=" + str(days)
    return URL_events

def organizeMapData(URL_events):
    """
    String URL_events
    
    Takes in the URL and organized the call from the API into a dictionary
    
    Returns the dictionary
    """
    map_data = {}
    event_data = requests.get(URL_events).json()
    events = event_data["events"]

    for event in events:
        event_title = event["title"]
        event_categories = event["categories"]
        category_id = event_categories[0]["id"]
        category_title = event_categories[0]["title"]

        coordinates_list = []
        event_geometries = event["geometries"]
        for geometry in event_geometries:
            coordinates = {
                "date": geometry["date"],
                "lat": geometry["coordinates"][1],
                "lon": geometry["coordinates"][0]
            }
            coordinates_list.append(coordinates)

        event_info = {
            "coordinates": coordinates_list,
            "category_id": category_id,
            "category_title": category_title
        }
        map_data[event_title] = event_info
    return map_data


def markerInfo(URL_categories):
    """
    String URL_categories
    
    Takes in the NASA API URL for categories
    Creates a dictionary to store and transer the wanted information.
    Adds a color scheme to each category type
    
    Returns dictionary
    """
    categories = requests.get(URL_categories).json()["categories"]

    category_data = {}
    for category in categories:
        category_id = category["id"]
        category_color1 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        category_color2 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        category_color3 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        category_data[category_id] = {
            "title": category["title"],
            "description": category["description"],
            "color1": category_color1,
            "color2": category_color2,
            "color3": category_color3
        }
    return category_data