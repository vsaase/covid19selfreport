
import json
import random
import urllib
from shapely.geometry import shape, Point, mapping, MultiPolygon
from shapely.ops import unary_union
import requests
from datetime import datetime


url = 'https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.geojson'
link_to_page = 'https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0/data'

r = requests.get(url, allow_redirects=True)
last_fetch = datetime.now()
open('static/landkreise_simplify200.geojson', 'wb').write(r.content)

data = r.json()

for i, feature in enumerate(data["features"]):
    name = feature["properties"]["BEZ"] + ' ' + feature["properties"]["GEN"]
    try:
        polygon = shape(feature["geometry"])
        polygon = MultiPolygon(sorted(polygon, key = lambda a: -a.area ))
    except:
        polygon = shape(feature["geometry"])
    feature["geometry"] = mapping(polygon.simplify(0.002))


with open('static/landkreise_simplify200.geojson', 'w') as json_file:
  json.dump(data, json_file)