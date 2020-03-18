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

f = open("landkreise_simplify200.geojson")
data = json.load(f)
f.close()


lat_bounds = [47.27012360470944, 55.099168977100774]
long_bounds = [5.866755374775609, 15.04181565646822]

laenderpolygons = {}
for feature in data["features"]:
    name = feature["properties"]["GEN"]
    polygon = shape(feature["geometry"])
    if name in laenderpolygons.keys():
        laenderpolygons[name] = unary_union([polygon, laenderpolygons[name]])
    else:
        laenderpolygons[name] = polygon

for name in laenderpolygons.keys():
    polygon = laenderpolygons[name]
    point = polygon.centroid
    print(name)
    source = "keine Zahlen vorhanden"
    ncases = 0
    number = 0
    # kreisreport = next(landkreise.where("name","==",name).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).get())
    # if kreisreport.exists:
    #     kreisreport = kreisreport.to_dict()
    #     source = kreisreport["source"]
    #     ncases = kreisreport["ncases"]
    #     number = kreisreport["number"] + 1

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
        "popup": f'<p>{name}<br/>{ncases} Fälle<br/>Quelle: {source}<br/><a href="/landkreis/{urllib.parse.quote(name)}">aktuelle Zahlen eintragen<a/><p/>'
    }
    print("setting " + name)
    landkreise.document(name + str(dct["number"])).set(dct)

