#Module principal de l'application (initialisation et configuration)

#Les différentes importations :
from flask import Flask
# importation de la classe Flask depuis le module flask
from flask_sqlalchemy import SQLAlchemy
# importation de la classe SQLAlchemy depuis l'extension flask_sqlalchemy (permet de lier la base de données à l'application et d'effectuer des requêtes sur cette base)
from flask_login import LoginManager
# importation de la classe LoginManager depuis l'extension flask_login (permet d'implémenter un système d'autorisation et de gérer des utilisateurs)
import os
# importation du module os (permet d’interagir avec le système d’exploitation)
from .constantes import CONFIG


#Définition des chemins (lié au module os) :
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# stockage du chemin menant au fichier courant
templates = os.path.join(chemin_actuel, "templates")
# stockage du chemin menant aux templates
statics = os.path.join(chemin_actuel, "static")
# stockage du chemin menant aux statics

#Création d'une instance de la classe SQLAlchemy :
db = SQLAlchemy()
# il s'agit de lier l'instance à l'application Flask

#Création d'une instance de la classe LoginManager :
login = LoginManager()
# lie l'instance à l'application Flask
# permettra notamment de conserver les paramètres de connexion des utilisateurs

#Création d'une instance de la classe Flask :
app = Flask(__name__,
    template_folder=templates,
    static_folder=statics
	)

# __name__ (le premier argument) doit correspondre au nom du package ou du module de l'application.
# Lorsqu'un seul module est utilisé, il est préférable d'employer le nom "__name__".
# Ce nom est utilisé pour trouver des ressources sur le système de fichiers.
# Il peut aussi être utilisé par des extensions pour améliorer les informations de débogage.
# Le but de ce premier paramètre est de donner à Flask une idée de ce qui fait partie de notre application.

# Ensuite sont définis les dossiers contenants les templates et les statics.

#Importation des routes depuis le dossier routes
from .routes import routes, errors


def config_app(config_name="production"):
    """ créé l'application """
    app.config.from_object(CONFIG[config_name])
    # configuration de l'app en appelant la constante CONFIG qui définit s'il s'agit de l'app test ou app de production
    # les configurations sont contenues dans le fichier constantes.py, où l'on retrouve la BDD associée

    # Set up extensions
    db.init_app(app)
    login.init_app(app)

    return app

