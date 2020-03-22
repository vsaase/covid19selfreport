import json
import random
import urllib
from shapely.geometry import shape, Point, mapping
from shapely.ops import unary_union
import requests
from datetime import datetime
from plz.plz2kreis import plz5stellig2kreis, plz2kreis

with open("plz/plz-5stellig.geojson") as f:
    data = json.load(f)

with open('static/landkreise_simplify200.geojson') as f:
    kreise = json.load(f)

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
    for kreis in kreise["features"]:
        kreisname  = kreis["properties"]["BEZ"] + ' ' + kreis["properties"]["GEN"]
        if kreisname == feature["properties"]["Kreis"]:
            feature["properties"]["estimated_cases"] = round(kreis["properties"]["cases_per_100k"] * feature["properties"]["einwohner"] / 100000)


with open('static/plz.geojson', 'w') as json_file:
  json.dump(data, json_file)