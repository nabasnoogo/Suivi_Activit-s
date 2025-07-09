from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.user import User
from ..extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Décorateur pour restreindre aux admins
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Accès refusé, vous devez être administrateur.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("Impossible de supprimer un administrateur.", "warning")
        return redirect(url_for('admin.dashboard'))
    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé.", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        is_confirmed = bool(request.form.get('is_confirmed'))
        is_admin = bool(request.form.get('is_admin'))
        user.is_confirmed = is_confirmed
        user.is_admin = is_admin
        db.session.commit()
        flash("Utilisateur mis à jour.", "success")
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_user.html', user=user)
