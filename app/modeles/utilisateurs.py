from werkzeug.security import generate_password_hash, check_password_hash
# Permet le hash des mots de passe
from flask_login import UserMixin
# UserMixin facilite l'implémentation d'une classe utilisateur
from sqlalchemy import or_
# Permet d'utiliser l'opérateur 'or' au sein des fonctions destinées à requêter la base de données.

from .. app import db, login

from .donnees import Contribution_utilisateur

# Création du modèle Utilisateur via déclaration d'une classe que l'on nomme "Utilisateur"
class Utilisateur(UserMixin, db.Model):
    __tablename__ = "utilisateur"
    id_utilisateur = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    identifiant = db.Column(db.String(45), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    nom_utilisateur = db.Column(db.Text, nullable=False)
    prenom_utilisateur = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    oeuvres = db.relationship(
        "Oeuvre",
        secondary=Contribution_utilisateur,
        back_populates="utilisateurs")
    artistes = db.relationship(
        "Artiste",
        secondary=Contribution_utilisateur,
        back_populates="utilisateurs")
    sujets = db.relationship(
        "Sujet",
        secondary=Contribution_utilisateur,
        back_populates="utilisateurs")
    techniques = db.relationship(
        "Technique",
        secondary=Contribution_utilisateur,
        back_populates="utilisateurs")
    localisations = db.relationship(
        "Localisation",
        secondary=Contribution_utilisateur,
        back_populates="utilisateurs")
    

    @staticmethod
    def identification(identifiant_u, mot_de_passe_u):
        """ Identifie un utilisateur. Si cela fonctionne, ses données sont renvoyées.
        :param identifiant_u: Identifiant de l'utilisateur
        :param mot_de_passe_u: Mot de passe de l'utilisateur
        :return: Données de l'utilisateur (si réussite). Dans le cas contraire : None
        """
        user = Utilisateur.query.filter(Utilisateur.identifiant == identifiant_u).first()
        if user and check_password_hash(user.mot_de_passe, mot_de_passe_u):
            return user
        return None
    

    @staticmethod
    def creation(identifiant_creer, mot_de_passe_creer, nom_utilisateur_creer, prenom_utilisateur_creer, email_creer):
        """ Permet de créer un compte utilisateur. Retourne un tuple (booléen, User ou liste).
        S'il y a une erreur, la fonction renvoie 'False', suivi d'une liste d'erreurs.
        Dans le cas contraire, elle renvoie 'True', suivi de la donnée enregistrée.

        :param identifiant_creer: Identifiant de l'utilisateur
        :param mot_de_passe_creer: Mot de passe de l'utilisateur (minimum 6 caractères)
		:param nom_utilisateur_creer: Nom de l'utilisateur
		:param prenom_utilisateur_creer: Prénom de l'utilisateur
        :param email_creer: E-mail de l'utilisateur
        :return: tuple
        """
        erreurs = []
        if not identifiant_creer:
            erreurs.append("L'identifiant fourni est vide.")
        if not mot_de_passe_creer or len(mot_de_passe_creer) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court (6 caractères minimum).")
        if not nom_utilisateur_creer:
            erreurs.append("Le nom fourni est vide.")
        if not prenom_utilisateur_creer:
            erreurs.append("Le prénom fourni est vide.")  
        if not email_creer:
            erreurs.append("L'e-mail fourni est vide.")


        # Vérification que l'e-mail ou l'identifiant ne sont pas déjà utilisés
        uniques = Utilisateur.query.filter(
            db.or_(Utilisateur.email == email_creer, Utilisateur.identifiant == identifiant_creer)
        ).count()
        if uniques > 0:
            erreurs.append("L'e-mail ou l'identifiant sont déjà utilisés.")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # S'il n'y a aucune erreur, création de l'utilisateur
        user = Utilisateur(
            identifiant=identifiant_creer,
            mot_de_passe=generate_password_hash(mot_de_passe_creer),
            nom_utilisateur=nom_utilisateur_creer,
            prenom_utilisateur=prenom_utilisateur_creer,
            email=email_creer
        )

        try:
            # Ajout au transport vers la base de données
            db.session.add(user)
            # Envoi du paquet
            db.session.commit()

            # Renvoi des données
            return True, user

        except Exception as erreur:
            return False, [str(erreur)]


    def get_id(self):
        """
        Retourne l'id de l'objet utilisé ici
        :return: id de l'utilisateur
        """ 
        return (self.id_utilisateur)


    @login.user_loader
    def trouver_utilisateur_via_id(id_utilisateur):
        """
        Permet de récupérer un utilisateur grâce à son identifiant
        :return: id de l'utilisateur
        """
        return Utilisateur.query.get(int(id_utilisateur))
