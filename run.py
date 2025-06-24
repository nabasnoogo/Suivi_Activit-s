# run.py

# On importe la fonction create_app depuis le package app
from app import create_app

# On crée une instance de l'application Flask en appelant la fonction create_app()
app = create_app()

# Ce bloc s'exécute uniquement si le fichier est exécuté directement
if __name__ == '__main__':
    # On démarre l'application Flask en mode debug
    # Cela permet de voir les erreurs facilement et de recharger automatiquement quand on modifie le code
    app.run(debug=True)
