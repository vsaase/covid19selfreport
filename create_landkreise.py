import geojson
import json
import firebase_admin
import random
from firebase_admin import credentials, firestore
import urllib
from shapely.geometry import shape, Point
from shapely.ops import unary_union

cred = credentials.Certificate("covid19-selfreport-firebase-adminsdk-jfup1-8a45aedc76.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
landkreise = db.collection("Landkreise")

f = open("static/landkreise_simplify200.geojson")
data = json.load(f)
f.close()

laenderpolygons = {}
for i, feature in enumerate(data["features"]):
    name = feature["properties"]["BEZ"] + ' ' + feature["properties"]["GEN"]
    polygon = shape(feature["geometry"])
    if name in laenderpolygons.keys():
        laenderpolygons[name] = {
            "polygon": unary_union([polygon, laenderpolygons[name]["polygon"]]), 
            "geojson_idxs": [i] + laenderpolygons[name]["geojson_idxs"]
        }
    else:
        laenderpolygons[name] = {"polygon": polygon, "geojson_idxs": [i]}

for name in laenderpolygons.keys():
    polygon = laenderpolygons[name]["polygon"]
    point = polygon.centroid
    print(name)
    source = "keine Zahlen vorhanden"
    ncases = 0
    number = 0
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
        "popup": f'<p>{name}<br/>{ncases} Fälle<br/>Quelle: {source}<br/><a href="/landkreis/{urllib.parse.quote(name)}">aktuelle Zahlen eintragen</a></p>'
    }
    print("setting " + name)
    landkreise.document(name + str(dct["number"])).set(dct)

