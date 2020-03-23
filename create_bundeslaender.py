from datetime import datetime
import json
import requests
from shapely.geometry import shape, mapping


url = 'https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.geojson'
link_to_page = 'https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/' \
               'ef4b445a53c1406892257fe63129a8ea_0?geometry=-67.085%2C46.270%2C83.340%2C55.886'
r = requests.get(url, allow_redirects=True)
last_fetch = datetime.now()

open('static/bundeslaender_simplify200.geojson', 'wb').write(r.content)
data = r.json()

lat_bounds = [47.27012360470944, 55.099168977100774]
long_bounds = [5.866755374775609, 15.04181565646822]

for feature in data["features"]:
    name = feature["properties"]["LAN_ew_GEN"]
    if "Bodensee" in name:
        continue
    try:
        polygon = max(shape(feature["geometry"]), key=lambda a: a.area)
    except:
        polygon = shape(feature["geometry"])
    feature["geometry"] = mapping(polygon.simplify(0.01))
    print(name)
    ncases = feature["properties"]["Fallzahl"]
    feature["properties"]["cases"] = ncases
    

with open('static/bundeslaender_simplify200.geojson', 'w') as json_file:
  json.dump(data, json_file)