from datetime import datetime

import firebase_admin
import requests
from firebase_admin import credentials, firestore
from shapely.geometry import shape

# cred = credentials.Certificate("covid19-selfreport-firebase-adminsdk-jfup1-8a45aedc76.json")

cred = credentials.Certificate("covid19test-218a3-firebase-adminsdk-o6s3e-40e98ea53d.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
rki_simulation = db.collection("RKI_Laender")

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
    polygon = shape(feature["geometry"])
    point = polygon.centroid
    print(name)
    ncases = feature["properties"]["Fallzahl"]
    ndeath = feature["properties"]["Death"]
    red_cases = 3000
    hue = 60-60*ncases/red_cases if ncases < red_cases else 0
    color = f'hsl({hue},100%,50%)'
    style = "opacity:1;weight:1;fillOpacity:0.8;color:" + color
    rki_simulation.document(name).set({
        "source": "RKI",
        "latitude": point.y,
        "longitude": point.x,
        "ncases": ncases,
        "ndeath": ndeath,
        "name": name,
        "test": "Positiv",
        "popup": f'<p>{ncases} positiv getestet in {name}<br/>{ndeath} Todesfälle<br/>'
                 f'Letzter Abruf von <a href="{link_to_page}"> um {last_fetch.strftime("%d.%m.%Y %H:%M:%S")}"</p>',
        "style:": style
    })
