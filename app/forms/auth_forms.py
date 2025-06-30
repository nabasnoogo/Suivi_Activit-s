from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# --- Formulaire d'inscription ---
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=6, message='Le mot de passe doit comporter au moins 6 caractères.')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe ne correspondent pas.')
    ])
    submit = SubmitField("S'inscrire")

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
        Length(min=6, message='Le mot de passe doit contenir au moins 6 caractères.')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe ne correspondent pas.')
    ])
    submit = SubmitField('Réinitialiser le mot de passe')
