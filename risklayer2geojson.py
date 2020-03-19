import geojson
import json
import firebase_admin
import random
from firebase_admin import credentials, firestore
import urllib
import pandas as pd
import datetime
from copy import deepcopy

risklayer = pd.read_csv("Risklayer Kreisebene Quellen - Studie 19032020 0330 - Haupt.csv", header=4) 

f = open("static/landkreise_simplify200.geojson")
data = json.load(f)
f.close()

maxval = 0

for i, row in risklayer.iterrows(): 
    ncases = int(row.loc["Coronavirus Fälle bis 19.03 00:00"])
    if ncases > maxval:
        maxval = ncases


for i, row in risklayer.iterrows(): 
    name = row.loc["GEN"]+' '+row.loc["BEZ"]
    for i, feature in enumerate(data["features"]):
        name2 = feature["properties"]["GEN"] + ' ' + feature["properties"]["BEZ"]
        if name == name2:
            ncases = int(row.loc["Coronavirus Fälle bis 19.03 00:00"])
            source = row.loc["Quelle 1"]
            feature["properties"]["risklayer"] = {
                "ncases": ncases, 
                "source": source, 
                "popup": f'<p>{name}<br/>{ncases} Fälle<br/>Quelle: <a href="{source}">{source}</a><br/>Daten von <a href="https://docs.google.com/spreadsheets/d/1wg-s4_Lz2Stil6spQEYFdZaBEp8nWW26gVyfHqvcl8s/htmlview#gid=0">Risklayer GmbH</a></p>',
                "color": "rgb(" + str(round(ncases**0.5*256/maxval**0.5)) + ",0,0)"
            }

with open('static/landkreise_risklayer.geojson', 'w') as json_file:
  json.dump(data, json_file)

