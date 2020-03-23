from flask_wtf import Form, RecaptchaField
from wtforms.widgets.html5 import NumberInput, URLInput
from wtforms.fields.html5 import URLField
from wtforms import SubmitField, HiddenField ,TextField, SelectField, SelectMultipleField, IntegerField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, Email, InputRequired, NumberRange, Optional, URL, ValidationError
import re
from plz.plz2kreis import plz_exists

def validate_plz(form, field):
    if not re.search(r"^[0-9]{5}$", field.data) or not plz_exists(field.data):
        raise ValidationError("Bitte geben Sie eine gültige Postleitzahl an")

def validate_fever(form, field):
    cleaned = field.data.replace(",", ".").replace('°','').replace("Grad","").strip()
    try:
        fever = float(cleaned)
        field.data = str(float(cleaned))
    except:
        raise ValidationError("Bitte geben Sie eine gültige Körpertemperatur an.")
    if fever < 32 or fever > 44:
        raise ValidationError("Bitte geben Sie eine Körpertemperatur zwischen 32 und 44 an.")

# Form ORM
class QuizForm(Form):
    geolocation = HiddenField("geolocation", validators=[Optional()])
    username = TextField('Bitte geben Sie einen Benutzernamen ein:', validators=[InputRequired(message="Bitte geben Sie einen Benutzernamen an")])
    password = PasswordField('Geben Sie ein Passwort ein, falls Sie Ihre Daten später ändern oder löschen wollen. Das Passwort wird nicht-wiederherstellbar verschlüsselt gespeichert.', validators=[InputRequired(message="Bitte geben Sie ein Passwort ein")])
    #email_addr = TextField('Ihr E-mail Addresse', validators=[InputRequired(message="Bitte geben Sie einen E-mail Addresse an")])
    plz = TextField('Bitte geben Sie Ihre Postleitzahl an:', widget=NumberInput(), validators=[InputRequired('Bitte geben Sie Ihre Postleitzahl an'), validate_plz])    
    sex = SelectField("Bitte geben Sie ihr Geschlecht an:",
        choices=[
            ('none', 'keine Angabe'), 
            ('diverse', 'divers'),
            ('female', 'weiblich'),
            ('male', 'männlich'), 
        ] , validators=[InputRequired()])
    age = IntegerField('Geben Sie bitte Ihr Alter ein:', widget=NumberInput(), validators=[NumberRange(min=0, max=120, message="Bitte geben Sie eine Zahl ein.")])
    travelhistory = SelectField('Sind Sie in den letzten 4 Wochen in einem Risikogebiet (Italien, Iran, China, Südkorea, Frankreich, Österreich, Spanien, USA) gewesen?',
                  choices=[
                            ('Nein', 'Nein'), 
                            ('Ja', 'Ja')], 
        validators=[InputRequired()])
    contacthistory = SelectField('Hatten Sie engen Kontakt zu einem bestätigten Fall? Z. B. Kontakt von Angesicht zu Angesicht länger als 15 Minuten, direkter physischer Kontakt (Berührung, Händeschütteln, Küssen), länger als 15 Minuten direkt neben einer infizierten Person (weniger als 2 Meter) verbracht, Kontakt mit oder Austausch von Körperflüssigkeiten, Teilen einer Wohnung?',
                  choices=[
                            ('Nein', 'Nein'), 
                            ('Ja', 'Ja')], 
        validators=[InputRequired()])
    notherstest = IntegerField('Wie viele Menschen, mit denen Sie Kontakt hatten, wurden positiv getestet?', widget=NumberInput(), validators=[NumberRange(min=0, max=100, message="Bitte Zahl mit Nummern eingeben")]) 

    fever = TextField("Falls Sie Fieber hatten, welche Temperatur haben Sie gemessen?", default="", validators=[Optional(), validate_fever])
    headache = IntegerField('Wie stark leiden Sie aktuell unter Kopfschmerzen? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    cough = IntegerField('Wie stark leiden Sie aktuell unter Husten? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    shortnessbreath = IntegerField('Wie stark leiden Sie aktuell unter Kurzatmigkeit? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    musclepain = IntegerField('Wie stark leiden Sie aktuell unter Muskel-Gelekschmerzen? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    sorethroat = IntegerField('Wie stark leiden Sie aktuell unter Halsschmerzen? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    nausea = IntegerField('Wie stark leiden Sie aktuell unter Übelkeit/Erbrechen? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    diarrhea = IntegerField('Wie stark leiden Sie aktuell unter Durchfall? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    rhinorrhea = IntegerField('Wie stark leiden Sie aktuell unter verstopfter Nase? (0 = keine Beschwerden, 10 = extrem stark)', default=0, widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=10, message="Bitte geben Sie eine Zahl zwischen 0 und 10 ein.")])
    
    #dayssymptoms = IntegerField('Falls zutreffend, seit wievielen Tagen haben Sie Symptome?', widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=None, message="Bitte Zahl mit Nummern eingeben")])
    arzt = SelectField('Waren Sie bereits wegen den Symptomen bei einer Ärztin / einem Arzt?', 
        choices=[
            ('Nein', 'Nein'), 
            ('Ja', 'Ja')],
        validators=[InputRequired()] )
    test = SelectField('Wurden Sie bereits auf das Coronavirus getestet und wenn ja, wie fiel der Test aus?', 
        choices=[
            ('Nicht durchgeführt', 'Nein'), 
            ('Ergebnis ausstehend', 'Ja, Ergebnis liegt noch nicht vor'), 
            ('Negativ', 'Ja, Ergebnis negativ'),
            ('Positiv', 'Ja, Ergebnis positiv')],
        validators=[InputRequired()] )
    datetest = DateField('Wenn ja, wann fand der Test statt?', format='%Y-%m-%d', validators=[Optional()])
    quarantine = SelectField('Haben Sie sich in Quarantäne begeben?', 
            choices=[
                ('Nein', 'Nein'), 
                ('Ja', 'Ja')],
            validators=[InputRequired()] )
    datequarantine = DateField('Wenn ja, wann hat Ihre Quarantäne begonnen??', format='%Y-%m-%d', validators=[Optional()])
    #notherssymptoms = IntegerField('Wieviele Menschen, mit denen Sie Kontakt hatten, haben ähnliche Symptome?', widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=100, message="Bitte Zahl mit Nummern eingeben")]) #commenting out a question that was earlier in the app, but does not appear in the google docs sheet.
    recaptcha = RecaptchaField()
    submit = SubmitField('Senden')
    
class DeleteForm(Form):
    username = TextField('Benutzername', validators=[InputRequired(message="Bitte geben Sie einen Benutzernamen an")])
    password = PasswordField('Passwort', validators=[InputRequired(message="Bitte geben Sie ein Passwort ein")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Senden')
    
