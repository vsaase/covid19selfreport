import geojson
import json
import firebase_admin
import random
from firebase_admin import credentials, firestore
import urllib
import pandas as pd
import datetime
from copy import deepcopy
import math

risklayer = pd.read_csv("risklayer/Risklayer Kreisebene Quellen - Studie 21032020 0330 - Haupt.csv", header=4) 

f = open("static/landkreise_simplify200.geojson")
data = json.load(f)
f.close()

maxval = 0

for i, row in risklayer.iterrows(): 
    name = row.loc["GEN"]+' '+row.loc["BEZ"]
    for i, feature in enumerate(data["features"]):
        name2 = feature["properties"]["GEN"] + ' ' + feature["properties"]["BEZ"]
        if name == name2:
            ncases = int(row.loc["Coronavirus Fälle bis 21.03 00:00"])
            casespp = ncases/feature["properties"]["destatis"]["population"] 
            if casespp > maxval:
                maxval = casespp


for i, row in risklayer.iterrows(): 
    name = row.loc["GEN"]+' '+row.loc["BEZ"]
    for i, feature in enumerate(data["features"]):
        name2 = feature["properties"]["GEN"] + ' ' + feature["properties"]["BEZ"]
        if name == name2:
            ncases = int(row.loc["Coronavirus Fälle bis 21.03 00:00"])
            casespp = ncases/feature["properties"]["destatis"]["population"] 
            source = row.loc["Quelle 1"]
            h = (1.0 - (casespp/maxval)**0.5) * 60
            feature["properties"]["risklayer"] = {
                "ncases": ncases, 
                "source": source, 
                "popup": f'<p>{name}<br/>{ncases} Fälle<br/>{"{:10.2f}".format(100*casespp)} Prozent der Bevölkerung<br/>Quelle: <a href="{source}">{source}</a><br/>Daten <a href="https://docs.google.com/spreadsheets/d/1wg-s4_Lz2Stil6spQEYFdZaBEp8nWW26gVyfHqvcl8s/htmlview#gid=0">crowdsourced von Risklayer GmbH</a><br/>Stand 21.3. 03:30<br/><a href="/landkreis/{name}">Statistik Dashboard</a></p>',
                "color": "hsl(" + str(h) + ", 100%, 50%)" #"rgb(" + str(round(math.log(1+ncases)*256/math.log(1+maxval))) + ",0,0)"
            }

with open('static/landkreise_risklayer.geojson', 'w') as json_file:
  json.dump(data, json_file)
