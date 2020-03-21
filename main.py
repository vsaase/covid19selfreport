import sys
import random
from flask import Flask, render_template, jsonify, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import request, flash
from flask_bootstrap import Bootstrap
from models import QuizForm, DeleteForm, LandkreisForm
import json
from copy import deepcopy
import firebase_admin
import urllib
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore
from itsdangerous import URLSafeTimedSerializer, Signer

from util import covertFirebaseTimeToPythonTime

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
rki_simulation = db.collection("RKI_Laender")
landkreise = db.collection("Landkreise")

BASECOORDS = [51.3150172,9.3205287]


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
    crd = json.loads(form.geolocation.data)
    dct["latitude"] = crd["latitude"]
    dct["longitude"] = crd["longitude"]
    dct["latitude_rand"] = dct["latitude"] + 0.01 * random.random()
    dct["longitude_rand"] = dct["longitude"] + 0.01 * random.random()
    dct["accuracy"] = crd["accuracy"]

    dct["test"] = form.test.data
    dct["arzt"] = form.arzt.data
    dct["quarantine"] = form.quarantine.data
    dct["datetest"] = None if form.datetest.data is None else form.datetest.data.strftime("%d.%m.%Y")
    dct["notherstest"] = form.notherstest.data
    dct["symptoms"] = ', '.join(form.symptoms.data)
    dct["dayssymptoms"] = form.dayssymptoms.data
    dct["notherssymptoms"] = form.notherssymptoms.data
    dct["age"] = form.age.data
    dct["sex"] = form.sex.data
    dct["plz"] = form.plz.data
    dct["email_addr"] = form.email_addr.data
    s = Signer(form.password.data)
    dct["signature"] = str(s.sign(form.email_addr.data))

    dct["timestamp"] = firestore.SERVER_TIMESTAMP
    dct["email_confirmed"] = False
    dct["overwritten"] = False
    dct["source"] = "report"
    dct["token"] = str(generate_confirmation_token(dct["signature"]))
    return dct


@app.route('/landkreis/<name>', methods=['GET', 'POST'])
def landkreis(name):
    form = LandkreisForm(request.form, name=name)
    kreisreportdocs = landkreise.where("name","==",name).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()
    kreisreporte = [doc.to_dict() for doc in kreisreportdocs]
    if not form.validate_on_submit():
        return render_template('landkreis.html', form=form, name=name, records=kreisreporte, colnames=["ncases", "source", "timestamp"])
    if request.method == 'POST':
        kreisreport = deepcopy(kreisreporte[0])
        kreisreport["ncases"] = form.ncases.data
        kreisreport["source"] = form.source.data
        kreisreport["number"] += 1
        kreisreport["popup"] = f'<p>{name}<br/>{form.ncases.data} Fälle<br/>Quelle: <a href="{form.source.data}">{form.source.data}</a><br/><br/><a href="/landkreis/{urllib.parse.quote(name)}">aktuelle Zahlen eintragen</a></p>'
        kreisreport["timestamp"] = datetime.datetime.now()
        landkreise.document(name + str(kreisreport["number"])).set(kreisreport)
        old = deepcopy(kreisreporte[0])
        old["overwritten"] = True
        landkreise.document(old["name"] + str(old["number"])).set(old)
        return redirect("/")


@app.route('/report', methods=['GET', 'POST'])
def report():
    form = QuizForm(request.form)
    if not form.validate_on_submit():
        return render_template('report.html', form=form)
    if request.method == 'POST':
        dct = createreportdict(form)
        
        report_ref.document(dct["token"]).set(dct)

        oldreports = report_ref.where("signature", '==', dct["signature"]).stream()
        for oldreport in oldreports:
            oldreport = oldreport.to_dict()
            if oldreport["token"] != dct["token"]:
                oldreport["overwritten"] = True
                report_ref.document(oldreport["token"]).set(oldreport)

        #return render_template('confirm_mail.html', mail=dct["email_addr"])

        template = render_template('success.html', mail=dct["email_addr"], risk="mittleres")
        response = make_response(template)
        response.set_cookie('signature', dct["signature"], max_age=60 * 60 * 24 * 365 * 2)
        return response


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm(request.form)
    if not form.validate_on_submit():
        return render_template('delete.html', form=form)
    if request.method == 'POST':
        s = Signer(form.password.data)
        signature = str(s.sign(form.email_addr.data))
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


@app.route('/')
def index():

    # read Cookie
    signature = request.cookies.get('signature')

    # if not exist
    date_time_obj = None
    if not signature:
        # create & forward to mandatory questionaire
        return redirect(url_for('report'))
    else:
        oldreports = report_ref.where("signature", '==', signature).stream()
        timestamp = None
        for oldreport in oldreports:
            oldreport = oldreport.to_dict()
            if timestamp is None or \
                    timestamp < oldreport["timestamp"]:
                timestamp = oldreport["timestamp"]
        date_time_obj = covertFirebaseTimeToPythonTime(timestamp)
        now = datetime.utcnow()


    # if Update needed?
    time_diff = timedelta(seconds=15)
    if date_time_obj + time_diff < now:
        # foward to addiitional survey
        return redirect(url_for('report'))
    else:
        # Show the user the map
        return render_template('index.html')


@app.route('/impressum')
def impressum():
    return render_template('impressum.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/getreports')
def getreports():
    reports = [doc.to_dict() for doc in report_ref.where("overwritten", '==', False).stream()]
    coords = [{
        "latitude": report["latitude_rand"], 
        "longitude": report["longitude_rand"],
        "symptoms": report["symptoms"],
        "dayssymptoms": report["dayssymptoms"],
        "test": report["test"],
        "source": report["source"],
        "nothers": report["notherssymptoms"],
        "date": report["timestamp"].strftime("%d.%m.%Y")
    } for report in reports]
    return jsonify({"coords": coords})


@app.route('/getrki')
def getrki():
    reports = [doc.to_dict() for doc in rki_simulation.stream()]
    coords = [{
        "latitude": report["latitude"], 
        "longitude": report["longitude"],
        "test": report["test"],
        "ncases": report["ncases"],
        "source": report["source"],
        "popup": report["popup"]
    } for report in reports]
    return jsonify({"coords": coords})


@app.route('/getlaender')
def getlaender():
    reports = [doc.to_dict() for doc in landkreise.where("overwritten", '==', False).stream()]
    coords = [{
        "latitude": report["latitude"], 
        "longitude": report["longitude"],
        "test": report["test"],
        "ncases": report["ncases"],
        "source": report["source"],
        "popup": report["popup"]
    } for report in reports]
    return jsonify({"coords": coords})


if __name__ == '__main__':
    app.run(debug=True)
