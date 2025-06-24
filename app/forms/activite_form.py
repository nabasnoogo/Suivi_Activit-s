from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class ActiviteForm(FlaskForm):
    structure = StringField('Structure', validators=[DataRequired()])
    acteurs = StringField('Acteurs', validators=[DataRequired()])
    type_activite = SelectField("Type d'activité", choices=[
        ('Système', 'Système'),
        ('Réseau', 'Réseau'),
        ('Réunion', 'Réunion'),
        ('Atelier', 'Atelier'),
        ('Mission', 'Mission'),
        ('Maintenance', 'Maintenance'),
        ('Activation_Antivirus', 'Activation_Antivirus'),
        ('Creation_de_mail', 'Creation_de_mail'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    autre_type = StringField("Précisez si 'Autre'", validators=[Optional()])
    equipement = StringField('Équipement', validators=[Optional()])
    etat = SelectField('État', choices=[
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé')
    ], validators=[DataRequired()])
    commentaire = TextAreaField('Commentaire', validators=[Optional()])
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])

    fichier = FileField('Fichier joint', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'docx'], 'Fichiers autorisés : jpg, jpeg, png, pdf, docx')
    ])

    submit = SubmitField('Enregistrer')
