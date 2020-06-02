from app.app import config_app
# Depuis le fichier app.py (dossier app), importation de la fonction config_app

if __name__ == "__main__":
	app = config_app("production")
	app.run(debug=True)

# Lance l'application
# Le mode debug permet de lancer un débogueur pendant le développement de l'application
