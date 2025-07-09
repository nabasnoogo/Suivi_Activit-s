from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User
from ..extensions import db, login_manager, mail
from ..forms.auth_forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from ..utils.token import generate_confirmation_token, confirm_token
from flask_mail import Message
from functools import wraps

auth = Blueprint('auth', __name__)

# === User loader ===
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === Décorateur pour confirmation e-mail ===
def email_confirmed_required(view_function):
    @wraps(view_function)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not current_user.is_confirmed:
            flash("Veuillez confirmer votre e-mail pour accéder à cette page.", "warning")
            return redirect(url_for('auth.unconfirmed'))
        return view_function(*args, **kwargs)
    return decorated_view

# === Inscription ===
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = generate_password_hash(form.password.data)

        if User.query.filter_by(email=email).first():
            flash("Cet e-mail est déjà utilisé.", "warning")
            return redirect(url_for('auth.register'))

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('confirm_email.html', confirm_url=confirm_url)
        subject = "Confirmation de votre compte"

        try:
            send_email(user.email, subject, html)
            flash("Un e-mail de confirmation vous a été envoyé.", "info")
        except Exception as e:
            flash("Erreur lors de l'envoi de l'e-mail. Voir la console.", "danger")
            print(f"[ERREUR ENVOI EMAIL] {e}")

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

# === Confirmation de l'e-mail ===
@auth.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash("Le lien de confirmation est invalide ou a expiré.", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash("Compte déjà confirmé.", "info")
    else:
        user.is_confirmed = True
        db.session.commit()
        flash("Compte confirmé avec succès !", "success")
    return redirect(url_for('auth.login'))

# === Connexion ===
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if not user.is_confirmed:
                flash("Veuillez confirmer votre e-mail avant de continuer.", "warning")
                return redirect(url_for('auth.unconfirmed'))
            flash("Connexion réussie", "success")
            return redirect(url_for('activites.list_activites'))
        else:
            flash("Email ou mot de passe incorrect", "danger")
    elif request.method == 'POST':
        flash("Veuillez corriger les erreurs dans le formulaire.", "danger")

    return render_template('login.html', form=form)

# === Utilisateur non confirmé ===
@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_confirmed:
        return redirect(url_for('activites.list_activites'))
    flash("Vous devez confirmer votre e-mail pour accéder à cette application.", "warning")
    return render_template('unconfirmed.html')

# === Déconnexion ===
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnecté avec succès", "info")
    return redirect(url_for('auth.login'))

# === Fonction générique d'envoi d'e-mail ===
def send_email(to, subject, html):
    try:
        msg = Message(subject, recipients=[to], html=html)
        mail.send(msg)
    except Exception as e:
        print(f"[SIMULÉ] Sujet : {subject}")
        print(f"[SIMULÉ] À : {to}")
        print("[SIMULÉ] Contenu HTML :")
        print(html)
        print(f"[SIMULÉ] Erreur : {e}")

# === Réinitialisation : demande de lien ===
@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('activites.list_activites'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash("Si l'adresse existe, un lien de réinitialisation a été envoyé.", "info")
        return redirect(url_for('auth.login'))

    return render_template('reset_request.html', form=form)

# === Réinitialisation : envoi du mail avec token ===
def send_reset_email(user):
    token = user.generate_reset_token()
    reset_url = url_for('auth.reset_token', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=reset_url)
    subject = "Réinitialisation de votre mot de passe"

    try:
        send_email(user.email, subject, html)
    except Exception as e:
        print("[ERREUR ENVOI EMAIL - RESET] ", e)

# === Réinitialisation : via le lien ===
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('activites.list_activites'))

    user = User.verify_reset_token(token)
    if not user:
        flash("Le lien est invalide ou a expiré.", "danger")
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash("Votre mot de passe a été réinitialisé avec succès.", "success")
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', form=form)
