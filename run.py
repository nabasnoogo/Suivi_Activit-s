from app import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    # Démarre l'app en mode production avec waitress
    serve(app, host='0.0.0.0', port=8000)
