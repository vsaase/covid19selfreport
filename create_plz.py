import json
import firebase_admin
import random
from firebase_admin import credentials, firestore
import urllib
from shapely.geometry import shape, Point, mapping
from shapely.ops import unary_union
import requests
from datetime import datetime
from plz.plz2kreis import plz5stellig2kreis, plz2kreis

with open("plz/plz-5stellig.geojson") as f:
    data = json.load(f)

for i, feature in enumerate(data["features"]):
    try:
        polygon = max(shape(feature["geometry"]), key=lambda a: a.area)
    except:
        polygon = shape(feature["geometry"])
    #feature["geometry"] = mapping(polygon.simplify(0.002))
    try:
        feature["properties"]["Kreis"] = plz5stellig2kreis[feature["properties"]["plz"]]
    except:
        try:
            feature["properties"]["Kreis"] = plz2kreis[feature["properties"]["plz"]]
        except:
            feature["properties"]["Kreis"] = ""


with open('static/plz.geojson', 'w') as json_file:
  json.dump(data, json_file)