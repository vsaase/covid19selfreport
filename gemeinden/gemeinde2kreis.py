import geojson
import json
from shapely.geometry import shape, Point
from shapely.ops import unary_union
import pandas as pd

f = open("gemeinden/gemeinde2kreis.json")
gemeinde2kreis = json.load(f)
f.close()


def f_gemeinde2kreis():
    f = open("gemeinden/gemeinden_simplify200.geojson")
    data = json.load(f)
    f.close()

    f = open("static/landkreise_simplify200.geojson")
    landkreise = json.load(f)
    f.close()

    gemeinde2kreis = {}

    for kreis in landkreise["features"]:
        kreispolygon = shape(kreis["geometry"])
        for feature in data["features"]:
            gemeinde = feature["properties"]["DEBKG_ID"]
            point = shape(feature["geometry"]).centroid
            if point.within(kreispolygon):
                kreisname = kreis["properties"]["BEZ"] + ' ' + kreis["properties"]["GEN"]
                if gemeinde in gemeinde2kreis.keys() and gemeinde2kreis[gemeinde] != kreisname:
                    print(f"conflict: {gemeinde} is already in {gemeinde2kreis[gemeinde]} when trying to add to {kreisname}")
                gemeinde2kreis[gemeinde] = kreisname
    with open('gemeinden/gemeinde2kreis.json', 'w') as json_file:
        json.dump(gemeinde2kreis, json_file)
