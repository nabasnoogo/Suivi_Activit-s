from ..extensions import db
from datetime import datetime

class Activite(db.Model):
    __tablename__ = 'activites'

    id = db.Column(db.Integer, primary_key=True)
    structure = db.Column(db.String(100), nullable=False)
    acteurs = db.Column(db.String(200), nullable=False)
    type_activite = db.Column(db.String(50), nullable=False)
    equipement = db.Column(db.String(100), nullable=True)
    etat = db.Column(db.String(20), nullable=False)
    commentaire = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=True)
    fichier = db.Column(db.String(255), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Activite {self.type_activite} du {self.date}>"
