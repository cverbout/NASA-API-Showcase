from flask import render_template
from flask.views import MethodView
import requests
from dotenv import load_dotenv
import os

class Apod(MethodView):
    def get(self):
        load_dotenv()
        apod_api_key = os.getenv("APOD_API_KEY")
        APOD_URL = f"https://api.nasa.gov/planetary/apod?api_key={apod_api_key}"
        apod = requests.get(APOD_URL).json()
        print(apod)
        APOD_image=apod['url']
        APOD_title=apod['title']
        APOD_author=apod['copyright']
        APOD_text=apod['explanation']
        return render_template('apod.html', APOD_image=APOD_image, APOD_title=APOD_title, APOD_author=APOD_author, APOD_text=APOD_text)
