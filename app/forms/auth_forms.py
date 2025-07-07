from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import re

# --- VALIDATEUR PERSONNALISÉ ---
def validate_strong_password(form, field):
    password = field.data
    erreurs = []

    if len(password) < 8:
        erreurs.append("au moins 8 caractères")
    if not re.search(r'[a-z]', password):
        erreurs.append("une lettre minuscule")
    if not re.search(r'[A-Z]', password):
        erreurs.append("une lettre majuscule")
    if not re.search(r'\d', password):
        erreurs.append("un chiffre")
    if not re.search(r'[\W_]', password):
        erreurs.append("un caractère spécial")

    if erreurs:
        raise ValidationError("Le mot de passe doit contenir " + ", ".join(erreurs) + ".")

# --- Formulaire d'inscription ---
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        validate_strong_password
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe ne correspondent pas.')
    ])
    submit = SubmitField("S'inscrire")

    # Validation personnalisée pour les adresses e-mail
    def validate_email(self, field):
        if not field.data.lower().endswith('.gov.bf'):
            raise ValidationError("Seules les adresses se terminant par .gov.bf sont autorisées.")

# --- Formulaire de connexion ---
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

# --- Formulaire pour demander un lien de réinitialisation ---
class RequestResetForm(FlaskForm):
    email = StringField('Adresse e-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Envoyer le lien de réinitialisation')

# --- Formulaire pour définir un nouveau mot de passe ---
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nouveau mot de passe', validators=[
        DataRequired(),
        validate_strong_password
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe ne correspondent pas.')
    ])
    submit = SubmitField('Réinitialiser le mot de passe')
