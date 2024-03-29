
import firebase_admin
import urllib
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore
from plz.plz2kreis import plz2longlat
import random

from config import Config
cred = credentials.Certificate("covid19-selfreport-firebase-adminsdk-jfup1-8a45aedc76.json")
cred = credentials.Certificate("covid19test-218a3-firebase-adminsdk-o6s3e-40e98ea53d.json")

firebase_admin.initialize_app(cred)
db = firestore.client()
report_ref = db.collection("Report")

reports = report_ref.where("plz", '>', "55442").stream()

for report in reports:
    dct = report.to_dict()
    try:
        dct["longitude"], dct["latitude"] = plz2longlat(dct["plz"])
        dct["latitude_rand"] = dct["latitude"] + 0.01 * random.random()
        dct["longitude_rand"] = dct["longitude"] + 0.01 * random.random()
        report_ref.document(dct["token"]).set(dct)
    except:
        pass