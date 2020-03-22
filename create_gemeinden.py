import json
import random
import urllib
from shapely.geometry import shape, Point, mapping
from shapely.ops import unary_union
import requests
import math
from datetime import datetime
from gemeinden.gemeinde2kreis import gemeinde2kreis

with open("static/gemeinden_simplify200.geojson") as f:
    data = json.load(f)

with open('static/landkreise_simplify200.geojson') as f:
    kreise = json.load(f)

for i, feature in enumerate(data["features"]):
    # try:
    #     polygon = max(shape(feature["geometry"]), key=lambda a: a.area)
    # except:
    #     polygon = shape(feature["geometry"])
    # feature["geometry"] = mapping(polygon.simplify(0.002))
    try:
        feature["properties"]["Kreis"] = gemeinde2kreis[feature["properties"]["DEBKG_ID"]]
    except:
        print("no kreis for " + feature["properties"]["GEN"])
        feature["properties"]["Kreis"] = ""
    for kreis in kreise["features"]:
        kreisname  = kreis["properties"]["BEZ"] + ' ' + kreis["properties"]["GEN"]

        if feature["properties"]["Kreis"] == "":
            kreispolygon = shape(kreis["geometry"])
            gemeindepolygon = shape(feature["geometry"])
            if gemeindepolygon.intersection(kreispolygon).area>0:
                feature["properties"]["Kreis"] = kreisname

        if kreisname == feature["properties"]["Kreis"]:
            if "destatis" in feature["properties"]:
                feature["properties"]["estimated_cases"] = round(kreis["properties"]["cases_per_100k"] * feature["properties"]["destatis"]["population"] / 100000)
            else:
                feature["properties"]["estimated_cases"] = "NA"


with open('static/gemeinden_estimated.geojson', 'w') as json_file:
  json.dump(data, json_file)