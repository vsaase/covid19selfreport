
import json
import firebase_admin
import random
from firebase_admin import credentials, firestore
import urllib
from shapely.geometry import shape, Point
from shapely.ops import unary_union
import requests
from datetime import datetime


#cred = credentials.Certificate("covid19-selfreport-firebase-adminsdk-jfup1-8a45aedc76.json")

cred = credentials.Certificate("covid19test-218a3-firebase-adminsdk-o6s3e-40e98ea53d.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
landkreise = db.collection("Landkreise")

url = 'https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.geojson'
link_to_page = 'https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0/data'

r = requests.get(url, allow_redirects=True)
last_fetch = datetime.now()
open('static/landkreise_simplify200.geojson', 'wb').write(r.content)

data = r.json()

for i, feature in enumerate(data["features"]):
    name = feature["properties"]["BEZ"] + ' ' + feature["properties"]["GEN"]
    polygon = shape(feature["geometry"])
    point = polygon.centroid
    print(name)
    source = "keine Zahlen vorhanden"
    ncases = feature["properties"]['cases']
    number = feature["properties"]['deaths']
    red_cases = 1000
    hue = 60-60*ncases/red_cases if ncases < red_cases else 0
    color = f'hsl({hue},100%,50%)'
    style = "opacity:1;weight:1;fillOpacity:0.8;color:" + color

    dct = {
        "number": number,
        "source": source,
        "name": name,
        "latitude": point.y,
        "longitude": point.x,
        "ncases": ncases,
        "test": "Positiv",
        "overwritten": False,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "popup": f'<p>{ncases} positiv getestet in {name}<br/>{number} Todesfälle<br/>'
                 f'Letzter Abruf von <a href="{link_to_page}">{link_to_page}</a> um {last_fetch.strftime("%d.%m.%Y %H:%M:%S")}"</p>',
        "style:": style
    }
    print("setting " + name)
    landkreise.document(name + str(dct["number"])).set(dct)

