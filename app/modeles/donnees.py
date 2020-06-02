from .. app import db
from sqlalchemy import and_
import datetime


# Création des modèles d'après la BDD (db.sqlite) de HG_Japonisme :

# Représentation des tables d'association issues de la BDD
Avoir_sujet = db.Table("avoir_sujet",
    db.Column("oeuvre_id", db.Integer, db.ForeignKey("oeuvre.id_oeuvre"), primary_key=True),
    db.Column("sujet_id", db.Integer, db.ForeignKey("sujet.id_sujet"), primary_key=True))

Avoir_technique = db.Table("avoir_technique",
    db.Column("oeuvre_id", db.Integer, db.ForeignKey("oeuvre.id_oeuvre"), primary_key=True),
    db.Column("technique_id", db.Integer, db.ForeignKey("technique.id_technique"), primary_key=True))

Creer = db.Table("creer",
    db.Column("oeuvre_id", db.Integer, db.ForeignKey("oeuvre.id_oeuvre"), primary_key=True),
    db.Column("artiste_id", db.Integer, db.ForeignKey("artiste.id_artiste"), primary_key=True))

Contribution_utilisateur = db.Table('contribution_utilisateur',
    db.Column('utilisateur_id', db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), primary_key=True),
    db.Column("oeuvre_id", db.Integer, db.ForeignKey("oeuvre.id_oeuvre"), primary_key=True),
    db.Column("artiste_id", db.Integer, db.ForeignKey("artiste.id_artiste"), primary_key=True),
    db.Column("sujet_id", db.Integer, db.ForeignKey("sujet.id_sujet"), primary_key=True),
    db.Column("technique_id", db.Integer, db.ForeignKey("technique.id_technique"), primary_key=True),
    db.Column("localisation_id", db.Integer, db.ForeignKey("localisation.id_localisation"), primary_key=True),
    db.Column('contribution_date', db.DateTime, default=datetime.datetime.utcnow))

# Représentation des autres tables
# Création du modèle Oeuvre via déclaration d'une classe que l'on nomme "Oeuvre"
class Oeuvre(db.Model):
    __tablename__ = "oeuvre"
    id_oeuvre = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    titre = db.Column(db.Text, nullable=False)
    date_oeuvre = db.Column(db.Text)
    dimensions = db.Column(db.Text)
    url_site = db.Column(db.Text)
    manifeste_iiif = db.Column(db.Text)
    iiif_image = db.Column(db.Text)
    localisation_id = db.Column(db.Integer, db.ForeignKey("localisation.id_localisation"))
    categorie_id = db.Column(db.Integer, db.ForeignKey("categorie.id_categorie"))
    localisation = db.relationship("Localisation", back_populates="oeuvres")
    categorie = db.relationship("Categorie", back_populates="oeuvres")
    sujets = db.relationship(
        "Sujet",
        secondary=Avoir_sujet,
        back_populates="oeuvres")
    techniques = db.relationship(
        "Technique",
        secondary=Avoir_technique,
        back_populates="oeuvres")
    artistes = db.relationship(
        "Artiste",
        secondary=Creer,
        back_populates="oeuvres")
    utilisateurs = db.relationship(
        "Utilisateur",
        secondary=Contribution_utilisateur,
        back_populates="oeuvres")


    def get_id(self):
        """
        Retourne l'id de l'objet utilisé ici
        :return: id de l'oeuvre
        """
        return(self.id_oeuvre)

    @staticmethod
    def ajout_oeuvre(ajout_titre, ajout_date_oeuvre, ajout_dimensions, ajout_url_site, ajout_manifeste_iiif, ajout_iiif_image, localisation_id, categorie_id):
        """
        Fonction qui permet d'ajouter une nouvelle oeuvre dans la BDD
        :param ajout_titre: titre de l'oeuvre (str)
        :param ajout_date_oeuvre: date de création de l'oeuvre (str)
        :param ajout_dimensions: dimensions de l'oeuvre (str)
        :param ajout_url_site: lien vers la page de présentation de l'oeuvre (source) - uniquement pour les oeuvres déjà en ligne (str)
        :param ajout_manifeste_iiif: Manifeste IIIF (métadonnées du document) - uniquement s'il en existe un (str)
        :param ajout_iiif_image: lien vers l'image via IIIF - uniquement lorsque c'est possible (str)
        :param localisation_id: id de la localisation de l'oeuvre (int)
        :param categorie_id: id de la catégorie de l'oeuvre (reproduction d'objet ou gravure originale) (int)
        :return:
        """

        erreurs = []
        if not ajout_titre:
            erreurs.append("Veuillez renseigner un titre pour cette oeuvre.")
        if not ajout_date_oeuvre:
            erreurs.append("Veuillez renseigner une date pour cette oeuvre. Si la date n'est pas connue, indiquer la mention : n.d.")
        if not ajout_dimensions:
            erreurs.append("Veuillez renseigner des dimensions pour cette oeuvre. Si les dimensions ne sont pas connues, indiquer la mention : dimensions inconnues.")
  
        # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

        # Le propre de la gravure est d'être un art reproductible (avec parfois des variations de couleurs lors des tirages).
        # Vérifier qu'une oeuvre n'est pas déjà présente dans la base étant donné que les champs pourraient comporter
        # les mêmes valeurs pourrait empêcher les contributeurs d'ajouter une nouvelle oeuvre.
        # Ex : la BnF possède plusieurs exemplaires d'une même gravure de Guérard. Il s'agit d'oeuvres différentes mais aux métadonnées identiques.
        # Dans ces conditions, je n'ai donc pas imposé une vérification des entrées déjà présentes dans la base (c'est uniquement valable pour cette fonction).
        
        # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Oeuvre (champs correspondant aux paramètres du modèle)
        nouvelle_oeuvre = Oeuvre(titre=ajout_titre,
                        		 date_oeuvre=ajout_date_oeuvre,
                        		 dimensions=ajout_dimensions,
                        		 url_site=ajout_url_site,
                        		 manifeste_iiif=ajout_manifeste_iiif,
                        		 iiif_image=ajout_iiif_image,
                        		 localisation_id=localisation_id,
                        		 categorie_id=categorie_id)

        #Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
        	db.session.add(nouvelle_oeuvre)
        	db.session.commit()
        	return True, nouvelle_oeuvre

        except Exception as erreur:
        	return False, [str(erreur)]


    @staticmethod
    def maj_oeuvre(id_oeuvre, maj_titre, maj_date_oeuvre, maj_dimensions, maj_url_site, maj_manifeste_iiif, maj_iiif_image, localisation_id, categorie_id):
        """
        Fonction qui permet de modifier les métadonnées d'une oeuvre dans la BDD
        :param id_oeuvre: id de l'oeuvre (int)
        :param maj_titre: titre de l'oeuvre (str)
        :param maj_date_oeuvre: date de création de l'oeuvre (str)
        :param maj_dimensions: dimensions de l'oeuvre (str)
        :param maj_url_site: lien vers la page de présentation de l'oeuvre (source) - uniquement pour les oeuvres déjà en ligne (str)
        :param maj_manifeste_iiif: Manifeste IIIF (métadonnées du document) - uniquement s'il en existe un (str)
        :param maj_iiif_image: lien vers l'image via IIIF - uniquement lorsque c'est possible (str)
        :param localisation_id: id de la localisation de l'oeuvre (int)
        :param categorie_id: id de la catégorie de l'oeuvre (reproduction d'objet ou gravure originale) (int)
        :return:
        """

        erreurs = []
        if not maj_titre:
            erreurs.append("Veuillez renseigner un titre pour cette oeuvre.")
        if not maj_date_oeuvre:
            erreurs.append("Veuillez renseigner une date pour cette oeuvre. Si la date n'est pas connue, indiquer la mention : n.d.")
        if not maj_dimensions:
            erreurs.append("Veuillez renseigner des dimensions pour cette oeuvre. Si les dimensions ne sont pas connues, indiquer la mention : dimensions inconnues.")
       
        if len(erreurs) > 0:
            return False, erreurs

        # Récupération de l'oeuvre grâce à l'identifiant
        modif_oeuvre = Oeuvre.query.get(id_oeuvre)

        # L'utilisateur doit modifier au moins un champ
        if modif_oeuvre.titre == maj_titre \
                and modif_oeuvre.date_oeuvre == maj_date_oeuvre \
                and modif_oeuvre.dimensions == maj_dimensions \
                and modif_oeuvre.url_site == maj_url_site \
                and modif_oeuvre.manifeste_iiif == maj_manifeste_iiif \
                and modif_oeuvre.iiif_image == maj_iiif_image \
                and modif_oeuvre.localisation_id == localisation_id \
                and modif_oeuvre.categorie_id == categorie_id :
            erreurs.append("Aucune modification n'a été réalisée.")


        if len(erreurs) > 0:
            return False, erreurs

        # Si aucune erreur n'a été détectée, mise à jour des données
        else :
            modif_oeuvre.titre=maj_titre
            modif_oeuvre.date_oeuvre=maj_date_oeuvre
            modif_oeuvre.dimensions=maj_dimensions
            modif_oeuvre.url_site=maj_url_site
            modif_oeuvre.manifeste_iiif=maj_manifeste_iiif
            modif_oeuvre.iiif_image=maj_iiif_image
            modif_oeuvre.localisation_id=localisation_id
            modif_oeuvre.categorie_id=categorie_id

        try:
            db.session.add(modif_oeuvre)
            db.session.commit()
            return True, modif_oeuvre

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def supprimer_oeuvre(id_oeuvre):
        """
        Fonction qui permet de supprimer une oeuvre de la BDD.
        :param id_oeuvre: id de l'oeuvre (int)
        :return:
        """
        suppr_oeuvre = Oeuvre.query.get(id_oeuvre)

        try:
            db.session.delete(suppr_oeuvre)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def associer_oeuvre_et_utilisateur(id_oeuvre, id_utilisateur):
        '''
        Fonction qui permet d'associer un contributeur à une oeuvre
        :param id_oeuvre: identifiant de l'oeuvre (int)
        :param id_utilisateur: identifiant de l'utilisateur (int)
        :return:
        '''
        erreurs = []
        if not id_oeuvre:
            erreurs.append("Il n'y a pas d'oeuvre à associer.")
        if not id_utilisateur:
            erreurs.append("Il n'y a pas d'utilisateur à associer.")

        oeuvr = Oeuvre.query.filter(Oeuvre.id_oeuvre == id_oeuvre).first()
        utilis = Utilisateur.query.filter(Utilisateur.id_utilisateur == id_utilisateur).first()

        if oeuvr is None or utilis is None:
            return

        if oeuvr not in utilis.oeuvres: 
            utilis.oeuvres.append(oeuvr)

        db.session.add(utilis)
        db.session.commit()

        return erreurs


# Création du modèle Localisation via déclaration d'une classe que l'on nomme "Localisation"
class Localisation(db.Model):
    __tablename__ = "localisation"
    id_localisation = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label_lieu_conservation = db.Column(db.Text)
    label_ville_conservation = db.Column(db.Text)
    oeuvres = db.relationship("Oeuvre", back_populates="localisation")
    utilisateurs = db.relationship(
        "Utilisateur",
        secondary=Contribution_utilisateur,
        back_populates="localisations")
	

    def get_id(self):
        """
        Retourne l'id de l'objet utilisé ici
        :return: id de la localisation de l'oeuvre
        """
        return(self.id_localisation)

    @staticmethod
    def ajout_localisation(ajout_label_lieu_conservation, ajout_label_ville_conservation):
        """
        Fonction qui permet d'ajouter une nouvelle localisation de l'oeuvre dans la BDD
        :param ajout_label_lieu_conservation: lieu de conservation de l'oeuvre (str)
        :param ajout_label_ville_conservation: ville de conservation de l'oeuvre (str)
        :return:
        """

        erreurs = []
        if not ajout_label_lieu_conservation:
            erreurs.append("Veuillez renseigner un lieu de conservation. Mentions possibles : localisation inconnue, collection particulière.")

        # Tous les enregistrements de all_label_localisation dans la table Localisation sont récupérés.
        all_label_localisation = Localisation.query.with_entities(db.and_(Localisation.label_lieu_conservation, Localisation.label_ville_conservation))
        all_label_localisation = [tlbl[0] for tlbl in all_label_localisation.all()]

        # Si le lieu et la ville de conservation ne sont pas déjà dans la table technique, création d'un nouvel enregistrement.
        if ajout_label_lieu_conservation and ajout_label_ville_conservation:
            if ajout_label_lieu_conservation or ajout_label_ville_conservation not in all_label_localisation:
                lieu_cons = Localisation(label_lieu_conservation=ajout_label_lieu_conservation,
                                        label_ville_conservation=ajout_label_ville_conservation)
  
                # Ajout et commit de ce nouvel enregistrement
                db.session.add(lieu_cons)
                db.session.commit()
                # Si le lieu et la ville de conservation sont déjà dans la base, la valeur de l'enregistrement est associée à celle déjà présente dans la base.
            else:
                lieu_cons = Localisation.query.filter(db.and_(Localisation.label_lieu_conservation == ajout_label_lieu_conservation,
                                                              Localisation.label_ville_conservation == ajout_label_ville_conservation)).first()

        try:
            return lieu_cons
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def maj_localisation(id_localisation, maj_label_lieu_conservation, maj_label_ville_conservation):
        """
        Fonction qui permet de modifier la localisation d'une oeuvre dans la BDD
        :param id_localisation: id de localisation de l'oeuvre (int)
        :param maj_label_lieu_conservation: lieu de conservation de l'oeuvre (str)
        :param maj_label_ville_conservation: ville de conservation de l'oeuvre (str)
        :return:
        """

        erreurs = []
        if not maj_label_lieu_conservation:
            erreurs.append("Veuillez renseigner un lieu de conservation. Mentions possibles : localisation inconnue, collection particulière.")
        
        if len(erreurs) > 0:
            return False, erreurs

        modif_localisation = Localisation.query.get(id_localisation)

        if modif_localisation.label_lieu_conservation == maj_label_lieu_conservation \
                and modif_localisation.label_ville_conservation == maj_label_ville_conservation :
            erreurs.append("Aucune modification n'a été réalisée.")

        if len(erreurs) > 0:
            return False, erreurs

        else :
            modif_localisation.label_lieu_conservation=maj_label_lieu_conservation
            modif_localisation.label_ville_conservation=maj_label_ville_conservation

        try:
            db.session.add(modif_localisation)
            db.session.commit()
            return True, modif_localisation

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def supprimer_localisation(id_localisation):
        """
        Fonction qui permet de supprimer une localisation de la BDD.
        :param id_localisation: id de localisation de l'oeuvre (int)
        :return:
        """
        suppr_localisation = Localisation.query.get(id_localisation)

        try:
            db.session.delete(suppr_localisation)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def associer_localisation_et_oeuvre(id_localisation, id_oeuvre):
        '''
        Fonction qui permet d'associer une localisation à une oeuvre
        :param id_localisation: identifiant de la localisation à associer à l'oeuvre (int)
        :param id_oeuvre: identifiant de l'oeuvre qui doit être associée à la localisation (int)
        :return:
        '''
        erreurs = []
        if not id_localisation:
            erreurs.append("Il n'y a pas de localisation à associer.")
        if not id_oeuvre:
            erreurs.append("Il n'y a pas d'oeuvre à associer.")

        localis = Localisation.query.filter(Localisation.id_localisation == id_localisation).first()
        oeuvr = Oeuvre.query.filter(Oeuvre.id_oeuvre == id_oeuvre).first()

        if localis is None or oeuvr is None:
            return

        if localis not in oeuvr.localisations: 
            oeuvr.localisations.append(localis)

        db.session.add(oeuvr)
        db.session.commit()

        return erreurs


    @staticmethod
    def associer_localisation_et_utilisateur(id_localisation, id_utilisateur):
        '''
        Fonction qui permet d'associer un contributeur à une localisation
        :param id_localisation: identifiant du lieu (int)
        :param id_utilisateur: identifiant de l'utilisateur (int)
        :return:
        '''
        erreurs = []
        if not id_localisation:
            erreurs.append("Il n'y a pas de localisation à associer.")
        if not id_utilisateur:
            erreurs.append("Il n'y a pas d'utilisateur à associer.")

        localis = Localisation.query.filter(Localisation.id_localisation == id_localisation).first()
        utilis = Utilisateur.query.filter(Utilisateur.id_utilisateur == id_utilisateur).first()

        if localis is None or utilis is None:
            return

        if localis not in utilis.localisations: 
            utilis.localisations.append(localis)

        db.session.add(utilis)
        db.session.commit()

        return erreurs
            

# Création du modèle Categorie via déclaration d'une classe que l'on nomme "Categorie"
class Categorie(db.Model):
    __tablename__ = "categorie"
    id_categorie = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label_categorie = db.Column(db.Text)
    oeuvres = db.relationship("Oeuvre", back_populates="categorie")
    

# Création du modèle Sujet via déclaration d'une classe que l'on nomme "Sujet"
class Sujet(db.Model):
    __tablename__ = "sujet"
    id_sujet = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label_sujet = db.Column(db.Text)
    oeuvres = db.relationship(
        "Oeuvre",
        secondary=Avoir_sujet,
        back_populates="sujets")
    utilisateurs = db.relationship(
        "Utilisateur",
        secondary=Contribution_utilisateur,
        back_populates="sujets")


    def get_id(self):
        """
        Retourne l'id de l'objet utilisé ici
        :return: id du sujet caractérisant l'oeuvre
        """
        return(self.id_sujet)

    @staticmethod
    def ajout_sujet(ajout_label_sujet):
        """
        Fonction qui permet d'ajouter un sujet caractérisant une oeuvre dans la BDD
        :param ajout_label_sujet: sujet qui caractérise l'oeuvre (str)
        :return:
        """

        erreurs = []
        if not ajout_label_sujet:
            erreurs.append("Veuillez renseigner un sujet.")
        
        # Tous les enregistrements de all_label_sujet dans la table Sujet sont récupérés.
        all_label_sujet = Sujet.query.with_entities(Sujet.label_sujet)
        all_label_sujet = [tlbl[0] for tlbl in all_label_sujet.all()]
        
        # Si le sujet n'est pas déjà dans la table sujet, création d'un nouvel enregistrement.
        if ajout_label_sujet:
            if ajout_label_sujet not in all_label_sujet:
                lab_suj = Sujet(label_sujet=ajout_label_sujet)
  
                # Ajout et commit de ce nouvel enregistrement
                db.session.add(lab_suj)
                db.session.commit()
                # Si le sujet est déjà dans la base, la valeur de l'enregistrement est associée à celle déjà présente dans la base.
            else:
                lab_suj = Sujet.query.filter(Sujet.label_sujet == ajout_label_sujet).first()

        try:
            return lab_suj
        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def maj_sujet(id_sujet, maj_label_sujet):
        """
        Fonction qui permet de modifier un sujet caractérisant une oeuvre dans la BDD
        :param id_sujet: id du sujet (int)
        :param maj_label_sujet: sujet qui caractérise l'oeuvre (str)
        :return:
        """

        erreurs = []
        if not maj_label_sujet:
            erreurs.append("Veuillez renseigner un sujet.")
              
        if len(erreurs) > 0:
            return False, erreurs

        modif_sujet = Sujet.query.get(id_sujet)

        if modif_sujet.label_sujet == maj_label_sujet :
            erreurs.append("Aucune modification n'a été réalisée.")

        if len(erreurs) > 0:
            return False, erreurs

        else :
            modif_sujet.label_sujet=maj_label_sujet

        try:
            db.session.add(modif_sujet)
            db.session.commit()
            return True, modif_sujet

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def supprimer_sujet(id_sujet):
        """
        Fonction qui permet de supprimer un sujet caractérisant une oeuvre de la BDD.
        :param id_sujet: id du sujet (int)
        :return:
        """
        suppr_sujet = Sujet.query.get(id_sujet)

        try:
            db.session.delete(suppr_sujet)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def associer_sujet_et_oeuvre(id_sujet, id_oeuvre):
        '''
        Fonction qui permet d'associer un sujet à une oeuvre
        :param id_sujet: identifiant du sujet à associer à l'oeuvre (int)
        :param id_oeuvre: identifiant de l'oeuvre qui doit être associée au sujet (int)
        :return:
        '''
        erreurs = []
        if not id_sujet:
            erreurs.append("Il n'y a pas de sujet à associer.")
        if not id_oeuvre:
            erreurs.append("Il n'y a pas d'oeuvre à associer.")

		# Récupération du sujet qui correspond à l'id puis de l'oeuvre qui correspond à l'id
        suj = Sujet.query.filter(Sujet.id_sujet == id_sujet).first()
        oeuvr = Oeuvre.query.filter(Oeuvre.id_oeuvre == id_oeuvre).first()

        # Si les identifiants ne correspondent à rien, aucune action n'est réalisée
        if suj is None or oeuvr is None:
            return

        # Si le sujet n'est pas déjà dans la liste de sujets contenue dans "sujets", il est ajouté à cette liste
        if suj not in oeuvr.sujets: 
            oeuvr.sujets.append(suj)

        db.session.add(oeuvr)
        db.session.commit()

        return erreurs


    @staticmethod
    def associer_sujet_et_utilisateur(id_sujet, id_utilisateur):
        '''
        Fonction qui permet d'associer un contributeur à un sujet
        :param id_sujet: identifiant du sujet (int)
        :param id_utilisateur: identifiant de l'utilisateur (int)
        :return:
        '''
        erreurs = []
        if not id_sujet:
            erreurs.append("Il n'y a pas de sujet à associer.")
        if not id_utilisateur:
            erreurs.append("Il n'y a pas d'utilisateur à associer.")

        suj = Sujet.query.filter(Sujet.id_sujet == id_sujet).first()
        utilis = Utilisateur.query.filter(Utilisateur.id_utilisateur == id_utilisateur).first()

        if suj is None or utilis is None:
            return

        if suj not in utilis.sujets: 
            utilis.sujets.append(suj)

        db.session.add(utilis)
        db.session.commit()

        return erreurs


# Création du modèle Technique via déclaration d'une classe que l'on nomme "Technique"
class Technique(db.Model):
    __tablename__ = "technique"
    id_technique = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label_technique = db.Column(db.Text)
    oeuvres = db.relationship(
        "Oeuvre",
        secondary=Avoir_technique,
        back_populates="techniques")
    utilisateurs = db.relationship(
        "Utilisateur",
        secondary=Contribution_utilisateur,
        back_populates="techniques")


    def get_id(self):
        """
        Retourne l'id de l'objet utilisé ici
        :return: id de la technique de réalisation de l'oeuvre
        """
        return(self.id_technique)

    @staticmethod
    def ajout_technique(ajout_label_technique):
        """
        Fonction qui permet d'ajouter une technique de réalisation d'une oeuvre dans la BDD
        :param ajout_label_technique: technique de réalisation de l'oeuvre (str)
        :return:
        """

        erreurs = []
        if not ajout_label_technique:
            erreurs.append("Veuillez renseigner une technique. Si celle-ci est inconnue, indiquer : technique non connue")

        # Tous les enregistrements de all_label_technique dans la table Technique sont récupérés.
        all_label_technique = Technique.query.with_entities(Technique.label_technique)
        all_label_technique = [tlbl[0] for tlbl in all_label_technique.all()]
        
        # Si la technique n'est pas déjà dans la table technique, création d'un nouvel enregistrement.
        if ajout_label_technique:
            if ajout_label_technique not in all_label_technique:
                techni = Technique(label_technique=ajout_label_technique)
  
                # Ajout et commit de ce nouvel enregistrement
                db.session.add(techni)
                db.session.commit()
                # Si cette technique est déjà dans la base, la valeur de l'enregistrement est associée à celle déjà présente dans la base.
            else:
                techni = Technique.query.filter(Technique.label_technique == ajout_label_technique).first()

        try:
            return techni
        except Exception as erreur:
            return False, [str(erreur)]



    @staticmethod
    def maj_technique(id_technique, maj_label_technique):
        """
        Fonction qui permet de modifier une technique de réalisation d'une oeuvre dans la BDD
        :param id_technique: id de la technique (int)
        :param maj_label_technique: technique de réalisation de l'oeuvre (str)
        :return:
        """

        erreurs = []
        if not maj_label_technique:
            erreurs.append("Veuillez renseigner une technique.")
                
        if len(erreurs) > 0:
            return False, erreurs

        modif_technique = Technique.query.get(id_technique)

        if modif_technique.label_technique == maj_label_technique :
            erreurs.append("Aucune modification n'a été réalisée.")

        if len(erreurs) > 0:
            return False, erreurs

        else :
            modif_technique.label_technique=maj_label_technique

        try:
            db.session.add(modif_technique)
            db.session.commit()
            return True, modif_technique

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def supprimer_technique(id_technique):
        """
        Fonction qui permet de supprimer une technique de réalisation d'une oeuvre de la BDD.
        :param id_technique: id de la technique (int)
        :return:
        """
        suppr_technique = Technique.query.get(id_technique)

        try:
            db.session.delete(suppr_technique)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def associer_technique_et_oeuvre(id_technique, id_oeuvre):
        '''
        Fonction qui permet d'associer une technique de réalisation à une oeuvre
        :param id_technique: identifiant de la technique à associer à l'oeuvre (int)
        :param id_oeuvre: identifiant de l'oeuvre qui doit être associée à la technique (int)
        :return:
        '''
        erreurs = []
        if not id_technique:
            erreurs.append("Il n'y a pas de technique à associer.")
        if not id_oeuvre:
            erreurs.append("Il n'y a pas d'oeuvre à associer.")

        techn = Technique.query.filter(Technique.id_technique == id_technique).first()
        oeuvr = Oeuvre.query.filter(Oeuvre.id_oeuvre == id_oeuvre).first()

        if techn is None or oeuvr is None:
            return

        if techn not in oeuvr.techniques: 
            oeuvr.techniques.append(techn)

        db.session.add(oeuvr)
        db.session.commit()

        return erreurs


    @staticmethod
    def associer_technique_et_utilisateur(id_technique, id_utilisateur):
        '''
        Fonction qui permet d'associer un contributeur à une technique
        :param id_technique: identifiant de la technique (int)
        :param id_utilisateur: identifiant de l'utilisateur (int)
        :return:
        '''
        erreurs = []
        if not id_technique:
            erreurs.append("Il n'y a pas de technique à associer.")
        if not id_utilisateur:
            erreurs.append("Il n'y a pas d'utilisateur à associer.")

        techn = Technique.query.filter(Technique.id_technique == id_technique).first()
        utilis = Utilisateur.query.filter(Utilisateur.id_utilisateur == id_utilisateur).first()

        if techn is None or utilis is None:
            return

        if techn not in utilis.techniques: 
            utilis.techniques.append(techn)

        db.session.add(utilis)
        db.session.commit()

        return erreurs


# Création du modèle Artiste via déclaration d'une classe que l'on nomme "Artiste"
class Artiste(db.Model):
    __tablename__ = "artiste"
    id_artiste = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text)
    annee_naissance = db.Column(db.Integer)
    annee_mort = db.Column(db.Integer)
    oeuvres = db.relationship(
        "Oeuvre",
        secondary=Creer,
        back_populates="artistes")
    utilisateurs = db.relationship(
        "Utilisateur",
        secondary=Contribution_utilisateur,
        back_populates="artistes")



    def get_id(self):
        """
        Retourne l'id de l'objet utilisé ici
        :return: id de l'artiste
        """
        return(self.id_artiste)

    @staticmethod
    def ajout_artiste(ajout_nom, ajout_prenom, ajout_annee_naissance, ajout_annee_mort):
        """
        Fonction qui permet d'ajouter un nouvel artiste dans la BDD
        :param ajout_nom: nom de l'artiste (str)
        :param ajout_prenom: prénom de l'artiste (str)
        :param ajout_annee_naissance: année de naissance de l'artiste (int)
        :param ajout_annee_mort: année de décès de l'artiste (int)
        :return:
        """

        erreurs = []
        if not ajout_nom:
            erreurs.append("Veuillez renseigner le nom de famille de l'artiste. Si le nom de l'artiste est inconnu, écrire : Artiste inconnu.")


        all_inf_artiste = Artiste.query.with_entities(db.and_(Artiste.nom, Artiste.prenom, Artiste.annee_naissance, Artiste.annee_mort))
        all_inf_artiste = [tlbl[0] for tlbl in all_inf_artiste.all()]

        if ajout_nom and ajout_prenom and ajout_annee_naissance and ajout_annee_mort:
            if ajout_nom or ajout_prenom or ajout_annee_naissance or ajout_annee_mort not in all_inf_artiste:
                artiste_inf = Artiste(nom=ajout_nom,
                                     prenom=ajout_prenom,
                                     annee_naissance=ajout_annee_naissance,
                                     annee_mort=ajout_annee_mort)
  
                db.session.add(artiste_inf)
                db.session.commit()
                
            else:
                artiste_inf = Artiste.query.filter(db.and_(Artiste.nom == ajout_nom,
                                                        Artiste.prenom == ajout_prenom,
                                                        Artiste.annee_naissance == ajout_annee_naissance,
                                                        Artiste.annee_mort == ajout_annee_mort)).first()

        try:
            return artiste_inf
        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def maj_artiste(id_artiste, maj_nom, maj_prenom, maj_annee_naissance, maj_annee_mort):
        """
        Fonction qui permet de modifier les données concernant un artiste dans la BDD
        :param id_artiste: id de l'artiste (int)
        :param maj_nom: nom de l'artiste (str)
        :param maj_prenom: prénom de l'artiste (str)
        :param maj_annee_naissance: année de naissance de l'artiste (int)
        :param maj_annee_mort: année de décès de l'artiste (int)
        :return:
        """

        erreurs = []
        if not maj_nom:
            erreurs.append("Veuillez renseigner le nom de famille de l'artiste.")
        
        if len(erreurs) > 0:
            return False, erreurs


        modif_artiste = Artiste.query.get(id_artiste)

        if modif_artiste.nom == maj_nom \
                and modif_artiste.prenom == maj_prenom \
                and modif_artiste.annee_naissance == maj_annee_naissance \
                and modif_artiste.annee_mort == maj_annee_mort :
            erreurs.append("Aucune modification n'a été réalisée.")

        if len(erreurs) > 0:
            return False, erreurs

        else :
            modif_artiste.nom=maj_nom
            modif_artiste.prenom=maj_prenom
            modif_artiste.annee_naissance=maj_annee_naissance
            modif_artiste.annee_mort=maj_annee_mort

        try:
            db.session.add(modif_artiste)
            db.session.commit()
            return True, modif_artiste

        except Exception as erreur:
            return False, [str(erreur)]

    
    @staticmethod
    def supprimer_artiste(id_artiste):
        """
        Fonction qui permet de supprimer un artiste de la BDD.
        :param id_artiste: id de l'artiste (int)
        :return:
        """
        suppr_artiste = Artiste.query.get(id_artiste)

        try:
            db.session.delete(suppr_artiste)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def associer_artiste_et_oeuvre(id_artiste, id_oeuvre):
        '''
        Fonction qui permet d'associer un artiste à une oeuvre
        :param id_artiste: identifiant de l'artiste à associer à l'oeuvre (int)
        :param id_oeuvre: identifiant de l'oeuvre qui doit être associée à l'artiste (int)
        :return:
        '''
        erreurs = []
        if not id_artiste:
            erreurs.append("Il n'y a pas d'artiste à associer.")
        if not id_oeuvre:
            erreurs.append("Il n'y a pas d'oeuvre à associer.")

        artist = Artiste.query.filter(Artiste.id_artiste == id_artiste).first()
        oeuvr = Oeuvre.query.filter(Oeuvre.id_oeuvre == id_oeuvre).first()

        if artist is None or oeuvr is None:
            return

        if artist not in oeuvr.artistes: 
            oeuvr.artistes.append(artist)

        db.session.add(oeuvr)
        db.session.commit()

        return erreurs


    @staticmethod
    def associer_artiste_et_utilisateur(id_artiste, id_utilisateur):
        '''
        Fonction qui permet d'associer un contributeur à un artiste
        :param id_artiste: identifiant de l'artiste (int)
        :param id_utilisateur: identifiant de l'utilisateur (int)
        :return:
        '''
        erreurs = []
        if not id_artiste:
            erreurs.append("Il n'y a pas d'artiste à associer.")
        if not id_utilisateur:
            erreurs.append("Il n'y a pas d'utilisateur à associer.")

        artist = Artiste.query.filter(Artiste.id_artiste == id_artiste).first()
        utilis = Utilisateur.query.filter(Utilisateur.id_utilisateur == id_utilisateur).first()

        if artist is None or utilis is None:
            return

        if artist not in utilis.artistes: 
            utilis.artistes.append(artist)

        db.session.add(utilis)
        db.session.commit()

        return erreurs

