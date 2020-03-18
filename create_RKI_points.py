import geojson
import json
import firebase_admin
import random
from firebase_admin import credentials, firestore

from shapely.geometry import shape, Point
from shapely.ops import unary_union
from rki_cases_17032020 import cases

cred = credentials.Certificate("covid19-selfreport-firebase-adminsdk-jfup1-8a45aedc76.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
rki_simulation = db.collection("RKI_Laender")

f = open("bundeslaender_simplify200.geojson")
data = json.load(f)
f.close()


lat_bounds = [47.27012360470944, 55.099168977100774]
long_bounds = [5.866755374775609, 15.04181565646822]

laender = cases.keys()
laenderpolygons = {}
for feature in data["features"]:
    name = feature["properties"]["GEN"]
    if "Bodensee" in name:
        continue
    polygon = shape(feature["geometry"])
    if name in laenderpolygons.keys():
        laenderpolygons[name] = unary_union([polygon, laenderpolygons[name]])
    else:
        laenderpolygons[name] = polygon

for name in laenderpolygons.keys():
    polygon = laenderpolygons[name]
    point = polygon.centroid
    print(name)
    rki_simulation.document(name).set({
        "source": "RKI",
        "latitude": point.y,
        "longitude": point.x,
        "ncases": cases[name],
        "name": name,
        "test": "Positiv",
        "popup": f"<p>{cases[name]} positiv getestet in {name}<br/>RKI-Daten Stand 17.3.</p>"
    })

