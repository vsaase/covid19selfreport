import sys
import random
from flask import Flask, render_template, jsonify, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import request, flash
from flask_bootstrap import Bootstrap
from models import QuizForm, DeleteForm
import json
from copy import deepcopy
import firebase_admin
import urllib
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore
from itsdangerous import URLSafeTimedSerializer, Signer
from plz.plz2kreis import plz2kreis, plz2longlat

from util import convertFirebaseTimeToPythonTime

testing_mode = True

if testing_mode:
    from config_test import Config
    cred = credentials.Certificate("covid19test-218a3-firebase-adminsdk-o6s3e-40e98ea53d.json")
else:
    from config import Config
    cred = credentials.Certificate("covid19-selfreport-firebase-adminsdk-jfup1-8a45aedc76.json")

app = Flask(__name__)
app.config.from_object(Config)

Bootstrap(app)

firebase_admin.initialize_app(cred)
db = firestore.client()
report_ref = db.collection("Report")

BASECOORDS = [51.3150172, 9.3205287]


def generate_confirmation_token(signature):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(signature, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        signature = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return signature


def createreportdict(form):
    dct = {}

    dct["plz"] = form.plz.data

    crd = json.loads(form.geolocation.data)
    dct["latitude"] = crd["latitude"]
    dct["longitude"] = crd["longitude"]
    dct["accuracy"] = crd["accuracy"]
    if dct["latitude"] == 0:
        dct["longitude"], dct["latitude"] = plz2longlat(dct["plz"])
        
    dct["latitude_rand"] = dct["latitude"] + 0.01 * random.random()
    dct["longitude_rand"] = dct["longitude"] + 0.01 * random.random()

    dct["username"] = form.username.data
    s = Signer(form.password.data)
    dct["signature"] = str(s.sign(form.username.data))
    dct["age"] = form.age.data
    dct["sex"] = form.sex.data
    dct["plz"] = form.plz.data

    dct["fever"] = form.fever.data
    dct["headache"] = form.headache.data
    dct["cough"] = form.cough.data
    dct["shortnessbreath"] = form.shortnessbreath.data
    dct["musclepain"] = form.musclepain.data
    dct["sorethroat"] = form.sorethroat.data
    dct["nausea"] = form.nausea.data
    dct["diarrhea"] = form.diarrhea.data
    dct["rhinorrhea"] = form.rhinorrhea.data

    dct["travelhistory"] = form.travelhistory.data
    dct["contacthistory"] = form.contacthistory.data
    dct["notherstest"] = form.notherstest.data
    
    dct["arzt"] = form.arzt.data
    dct["test"] = form.test.data
    dct["datetest"] = None if form.datetest.data is None else form.datetest.data.strftime("%d.%m.%Y")
    dct["quarantine"] = form.quarantine.data
    dct["datequarantine"] = None if form.datetest.data is None else form.datequarantine.data.strftime("%d.%m.%Y")

    try:
        dct["kreis"] = plz2kreis[dct["plz"]]
    except:
        dct["kreis"] = ""
        print(f"error converting PLZ {dct['plz']} to Kreisebene")

    dct["timestamp"] = firestore.SERVER_TIMESTAMP
    dct["email_confirmed"] = False
    dct["overwritten"] = False
    dct["source"] = "report"
    dct["token"] = str(generate_confirmation_token(dct["signature"]))
    return dct


@app.route('/landkreis/<name>', methods=['GET', 'POST'])
def landkreis(name):
    return render_template('landkreis.html', name=name)

@app.route('/report', methods=['GET', 'POST'])
def report():
    username = request.cookies.get('username')
    if username:
        form = QuizForm(request.form, dayssymptoms=0, notherstest=0, username=username, meta={'locales': ['de_DE', 'de']})
    else:
        form = QuizForm(request.form, dayssymptoms=0, notherstest=0, meta={'locales': ['de_DE', 'de']})
    
    if form.validate_on_submit():
        dct = createreportdict(form)
        report_ref.document(dct["token"]).set(dct)

        oldreports = report_ref.where("signature", '==', dct["signature"]).stream()
        for oldreport in oldreports:
            oldreport = oldreport.to_dict()
            if oldreport["token"] != dct["token"]:
                oldreport["overwritten"] = True
                report_ref.document(oldreport["token"]).set(oldreport)
                
        template = redirect("/")
        response = make_response(template)
        response.set_cookie('signature', dct["signature"], max_age = 60*60*24*365*2)
        response.set_cookie('username', dct["username"], max_age = 60*60*24*365*2)
        return response

    else:
        return render_template('map.html', form=form, show_report=True, mandatory_done=False, plz="00000")

@app.route('/<plz>', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def map(plz = '00000'):
    signature = request.cookies.get('signature')

    if signature:
        resp = make_response(render_template('map.html', form=None, show_report=False, mandatory_done=False, plz=plz))
        return resp

    else:
        return redirect("/report")


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm(request.form)
    if not form.validate_on_submit():
        return render_template('delete.html', form=form)
    if request.method == 'POST':
        s = Signer(form.password.data)
        signature = str(s.sign(form.username.data))
        oldreports = report_ref.where("signature", '==', signature).stream()
        ndel = 0
        for oldreport in oldreports:
            oldreport = oldreport.to_dict()
            if oldreport["overwritten"] == False:
                ndel += 1
            oldreport["overwritten"] = True
            oldreport["deleted"] = True
            report_ref.document(oldreport["token"]).set(oldreport)

        return render_template('delete_success.html', ndel=ndel)


@app.route('/map/<plz>')
@app.route("/map")
def shortcut(plz='00000'):
    return render_template('index.html', plz=plz)


@app.route('/impressum')
def impressum():
    return render_template('impressum.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/getreports')
def getreports():
    reports = [doc.to_dict() for doc in report_ref.where("overwritten", '==', False).stream()]
    data = [{
        "latitude": report["latitude_rand"],
        "longitude": report["longitude_rand"],
        "test": report["test"],
        "date": report["timestamp"].strftime("%d.%m.%Y"),
        "fever": "" if "fever" not in report else report["fever"],
        "headache": 0 if "headache" not in report else report["headache"],
        "cough": 0 if "cough" not in report else report["cough"],
        "shortnessbreath": 0 if "shortnessbreath" not in report else report["shortnessbreath"],
        "musclepain": 0 if "musclepain" not in report else report["musclepain"],
        "sorethroat": 0 if "sorethroat" not in report else report["sorethroat"],
        "nausea": 0 if "nausea" not in report else report["nausea"],
        "diarrhea": 0 if "diarrhea" not in report else report["diarrhea"],
        "rhinorrhea": 0 if "rhinorrhea" not in report else report["rhinorrhea"]
    } for report in reports]
    return jsonify({"data": data})


if __name__ == '__main__':
    app.run(debug=True)
