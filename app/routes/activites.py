# Importation des modules nécessaires
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, make_response
from werkzeug.utils import secure_filename
from ..extensions import db
from ..models.activite import Activite
from ..forms.activite_form import ActiviteForm
from datetime import datetime
import os
from weasyprint import HTML
from flask_login import login_required

# Création du blueprint pour les activités f
activites_bp = Blueprint('activites', __name__, url_prefix='/activites')

# ROUTE 1 : Liste des activités (sans filtrage)
@activites_bp.route('/')
@login_required
def list_activites():
    activites = Activite.query.order_by(Activite.date.desc()).all()
    return render_template('list_activites.html', activites=activites)


# ROUTE 2 : Ajouter une activité
@activites_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_activite():
    form = ActiviteForm()

    if form.validate_on_submit():
        # Gestion du type d'activité "Autre"
        if form.type_activite.data == 'Autre' and form.autre_type.data:
            type_activite_final = form.autre_type.data.strip()
        else:
            type_activite_final = form.type_activite.data

        fichier_nom = None
        if form.fichier.data:
            fichier = form.fichier.data
            filename = secure_filename(fichier.filename)
            chemin_upload = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(chemin_upload, exist_ok=True)
            fichier.save(os.path.join(chemin_upload, filename))
            fichier_nom = filename

        nouvelle_activite = Activite(
            structure=form.structure.data,
            acteurs=form.acteurs.data,
            type_activite=type_activite_final,
            equipement=form.equipement.data,
            etat=form.etat.data,
            commentaire=form.commentaire.data,
            date=form.date.data if form.date.data else datetime.utcnow().date(),
            fichier=fichier_nom
        )

        db.session.add(nouvelle_activite)
        db.session.commit()
        flash("Activité ajoutée avec succès.", "success")
        return redirect(url_for('activites.list_activites'))

    return render_template('add_activite.html', form=form, action='Ajouter')

# ROUTE 3 : Modifier une activité
@activites_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_activite(id):
    activite = Activite.query.get_or_404(id)
    form = ActiviteForm(obj=activite)

    # Pré-remplir le champ autre_type si besoin
    if request.method == 'GET':
        choix_types = [c[0] for c in form.type_activite.choices]
        if activite.type_activite not in choix_types:
            form.type_activite.data = 'Autre'
            form.autre_type.data = activite.type_activite

    if form.validate_on_submit():
        if form.type_activite.data == 'Autre' and form.autre_type.data:
            type_activite_final = form.autre_type.data.strip()
        else:
            type_activite_final = form.type_activite.data

        if form.fichier.data:
            fichier = form.fichier.data
            filename = secure_filename(fichier.filename)
            chemin_upload = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(chemin_upload, exist_ok=True)
            fichier.save(os.path.join(chemin_upload, filename))
            activite.fichier = filename

        activite.structure = form.structure.data
        activite.acteurs = form.acteurs.data
        activite.type_activite = type_activite_final
        activite.equipement = form.equipement.data
        activite.etat = form.etat.data
        activite.commentaire = form.commentaire.data
        activite.date = form.date.data if form.date.data else activite.date

        db.session.commit()
        flash("Activité modifiée avec succès.", "success")
        return redirect(url_for('activites.list_activites'))

    return render_template('add_activite.html', form=form, action='Modifier')


# ROUTE 4 : Supprimer une activité
@activites_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_activite(id):
    activite = Activite.query.get_or_404(id)

    if activite.fichier:
        try:
            path = os.path.join(current_app.root_path, 'static', 'uploads', activite.fichier)
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")

    db.session.delete(activite)
    db.session.commit()

    flash("Activité supprimée.", "info")
    return redirect(url_for('activites.list_activites'))


# ROUTE 5 : Génération de rapport avec filtre et export PDF
@activites_bp.route('/rapport_pdf', methods=['GET', 'POST'])
@login_required
def rapport_pdf():
    mois = request.values.get('mois', type=int)
    annee = request.values.get('annee', type=int)
    structure = request.values.get('structure', type=str)
    action = request.form.get('action')  # 'afficher' ou 'telecharger'

    if mois and not annee:
        annee = datetime.utcnow().year

    mois_francais = {
        1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
        7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
    }

    query = Activite.query
    if mois:
        query = query.filter(db.extract('month', Activite.date) == mois)
    if annee:
        query = query.filter(db.extract('year', Activite.date) == annee)
    if structure:
        query = query.filter(Activite.structure.ilike(f"%{structure}%"))
    activites = query.order_by(Activite.date.desc()).all()

    titre_rapport = "Rapport des Activités"
    if mois and annee:
        nom_mois = mois_francais.get(mois, "Mois Inconnu")
        titre_rapport = f"Rapport mensuel de {nom_mois} {annee}"
    elif annee:
        titre_rapport = f"Rapport annuel de {annee}"
    elif structure:
        titre_rapport = f"Rapport des activités - Structure : {structure.upper()}"

    if action == 'telecharger':
        rendered = render_template('rapport_pdf_export.html', activites=activites, titre_rapport=titre_rapport)
        pdf = HTML(string=rendered).write_pdf()
        response = make_response(pdf)

        filename = f"rapport_{titre_rapport.replace(' ', '_').lower()}.pdf"
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    return render_template('rapport_pdf.html',
                           activites=activites,
                           mois=mois,
                           annee=annee,
                           structure=structure,
                           titre_rapport=titre_rapport)
