from flask_wtf import Form, RecaptchaField
from wtforms.widgets.html5 import NumberInput, URLInput
from wtforms.fields.html5 import URLField
from wtforms import SubmitField, HiddenField, TextField, SelectField, SelectMultipleField, IntegerField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, Email, InputRequired, NumberRange, Optional, URL, ValidationError
import re
from plz.plz2kreis import plz_exists


def validate_plz(form, field):
    if not re.search(r"^[0-9]{5}$", field.data) or not plz_exists(field.data):
        raise ValidationError("Bitte geben Sie eine gültige Postleitzahl an")
    
# Form ORM
class QuizForm(Form):
    geolocation = HiddenField("geolocation", validators=[Optional()])
    symptoms = SelectMultipleField('Markieren Sie die Symptome, die sie haben (zum Markieren mehrerer Optionen am PC Strg-Taste (Ctrl) gedrückt halten):', 
        choices=[
            ('Fieber', 'Fieber'), 
            ('Müdigkeit', 'Müdigkeit'), 
            ('Husten', 'Husten'), 
            ('Niesen', 'Niesen'), 
            ('Gliederschmerzen', 'Gliederschmerzen'), 
            ('Schnupfen', 'Schnupfen'), 
            ('Halsschmerzen', 'Halsschmerzen'), 
            ('Durchfall', 'Durchfall'), 
            ('Kopfschmerzen', 'Kopfschmerzen'), 
            ('Kurzatmigkeit', 'Kurzatmigkeit'),
        ], 
        validators=[Optional()], render_kw={"size": "10"})

    dayssymptoms = IntegerField('Seit wievielen Tagen haben Sie Symptome?', widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=None, message="Bitte Zahl mit Nummern eingeben")])
    notherssymptoms = IntegerField('Wieviele Menschen, mit denen Sie Kontakt hatten, haben ähnliche Symptome?', widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=100, message="Bitte Zahl mit Nummern eingeben")])
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
    notherstest = IntegerField('Wieviele Menschen, mit denen Sie Kontakt hatten, wurden positiv getestet?', widget=NumberInput(), validators=[NumberRange(min=0, max=100, message="Bitte Zahl mit Nummern eingeben")])
    quarantine = SelectField('Haben Sie sich in Quarantäne begeben?', 
            choices=[
                ('Nein', 'Nein'), 
                ('Ja', 'Ja')],
            validators=[InputRequired()] )
    age = IntegerField('Wie alt sind Sie (Jahre)', widget=NumberInput(), validators=[NumberRange(min=0, max=120, message="Bitte Zahl mit Nummern eingeben")])
    sex = SelectField("Welches Geschlecht haben Sie",
    choices=[
            ('', ''), 
            ('female', 'weiblich'),
            ('male', 'männlich'), 
     ] , validators=[InputRequired()])
    plz = TextField('Bitte geben Sie Ihre Postleitzahl an', widget=NumberInput(), validators=[InputRequired('Bitte geben Sie Ihre Postleitzahl an'), validate_plz])
    email_addr = TextField('Ihr Benutzername', validators=[InputRequired(message="Bitte geben Sie einen Benutzernamen an")])
    password = PasswordField('Geben Sie ein Passwort ein, falls Sie Ihre Daten später ändern oder löschen wollen. Das Passwort wird auf dem Server nicht-wiederherstellbar verschlüsselt gespeichert.', validators=[InputRequired(message="Bitte geben Sie ein Passwort ein")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Senden')


class DeleteForm(Form):
    email_addr = TextField('Benutzername', validators=[InputRequired(message="Bitte geben Sie einen Benutzernamen an")])
    password = PasswordField('Passwort', validators=[InputRequired(message="Bitte geben Sie ein Passwort ein")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Senden')
    