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
    username = TextField('Ihr Benutzername', validators=[InputRequired(message="Bitte geben Sie einen Benutzernamen an")])
    password = PasswordField('Geben Sie ein Passwort ein, falls Sie Ihre Daten später ändern oder löschen wollen. Das Passwort wird auf dem Server nicht-wiederherstellbar verschlüsselt gespeichert.', validators=[InputRequired(message="Bitte geben Sie ein Passwort ein")])
    #email_addr = TextField('Ihr E-mail Addresse', validators=[InputRequired(message="Bitte geben Sie einen E-mail Addresse an")])
    plz = TextField('Bitte geben Sie Ihre Postleitzahl an', widget=NumberInput(), validators=[InputRequired('Bitte geben Sie Ihre Postleitzahl an'), validate_plz])    
    sex = SelectField("Welches Geschlecht haben Sie",
        choices=[
            ('', ''), 
            ('female', 'weiblich'),
            ('male', 'männlich'), 
        ] , validators=[InputRequired()])
    age = IntegerField('Wie alt sind Sie (Jahre)', widget=NumberInput(), validators=[NumberRange(min=0, max=120, message="Bitte Zahl mit Nummern eingeben")])
    travelhistory = SelectField('Sind Sie in den letzten 4 Wochen im Risikogebiet (Italien, Iran, China, Südkorea, Frankreich, Österreich, Spanien, USA) gewesen?',
                  choices=[
                            ('Nein', 'Nein'), 
                            ('Ja', 'Ja')], 
        validators=[InputRequired()])
    contacthistory = SelectField('Hatten Sie engen Kontakt zu einem bestätigten Fall?Enger Kontakt mit einem bestätigten Fall bedeutet:Kontakt von Angesicht zu Angesicht länger als 15 Minuten, Direkter, physischer Kontakt (Berührung, Händeschütteln, Küssen), Länger als 15 Minuten direkt neben einer infizierten Person (weniger als 2 Meter) verbracht Kontakt mit oder Austausch von Körperflüssigkeiten, Teilen einer Wohnung?',
                  choices=[
                            ('Nein', 'Nein'), 
                            ('Ja', 'Ja')], 
        validators=[InputRequired()])
    notherstest = IntegerField('Wie viele Menschen, mit denen Sie Kontakt hatten, wurden positiv getestet?', widget=NumberInput(), validators=[NumberRange(min=0, max=100, message="Bitte Zahl mit Nummern eingeben")]) 
    symptoms = SelectField('Wählen Sie aus, wenn sie unter folgenden Symptomen leiden (zum Markieren mehrerer Optionen am PC Strg-Taste (Ctrl) gedrückt halten):', 
        choices=[
            ('Fieber (38 C)', 'Fieber (38 C)'), 
            ('Husten', 'Husten'),
            ('Kurzatmigkeit', 'Kurzatmigkeit'),
            ('Muskel-Gelekschmerzen', 'Muskel-Gelekschmerzen'), 
            ('Halsschmerzen', 'Halsschmerzen'), 
            ('Kopfschmerzen', 'Kopfschmerzen'),
            ('Übelkeit/Erbrechen', 'Übelkeit/Erbrechen'),
            ('Durchfall', 'Durchfall'),
            ('verstopfte Nase', 'verstopfte Nase'),            
        ], 
        validators=[Optional()], render_kw={"size": "9"})
    dayssymptoms = IntegerField('Falls zutreffend, seit wievielen Tagen haben Sie Symptome?', widget=NumberInput(), validators=[Optional(), NumberRange(min=0, max=None, message="Bitte Zahl mit Nummern eingeben")])
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
    
