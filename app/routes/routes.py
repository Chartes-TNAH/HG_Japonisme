from flask import render_template, url_for, request, redirect, flash
# render_template : permet de relier les templates aux routes
# url_for : permet de construire des url vers les fonctions et les pages html
# request : permet à flask de manipuler les requêtes et réponses HTTP
# redirect : permet une redirection vers l'url d'une autre route
# flash : permet l'envoi de messages flash

from flask_login import current_user, login_user, logout_user, login_required
# va permettre de gérer les sessions utilisateur

from sqlalchemy import or_, and_

from app.app import app, login

from app.modeles.donnees import Oeuvre, Localisation, Categorie, Sujet, Technique, Artiste
from app.modeles.utilisateurs import Utilisateur
from app.constantes import RESULTATS_PAR_PAGE



# Définition des routes
@app.route("/")
def accueil():
    """
    Route permettant l'affichage de la page d'accueil
    :return: template accueil.html
    """
    return render_template("pages/accueil.html", nom="HG_Japonisme")
# La fonction render_template prend comme premier argument le chemin du template


@app.route("/a_propos")
def a_propos():
    """
    Route permettant l'affichage de la page 'à propos'
    :return: template a_propos.html
    """
    return render_template("pages/a_propos.html", nom="HG_Japonisme")


@app.route("/repro_objets")
def repro_objets():
    """
    Route permettant d'afficher la page présentant les œuvres de catégorie "Reproductions d'objets" de la base de données
    :return: template repro_objets.html
    """
    reproductions_objets = Oeuvre.query.filter(Oeuvre.categorie_id == 1).all()
    return render_template("pages/repro_objets.html", nom="HG_Japonisme", reproductions_objets=reproductions_objets)


@app.route("/grav_originales")
def grav_originales():
    """
    Route permettant d'afficher la page présentant les œuvres de catégorie "Gravures originales" de la base de données
    :return: template grav_originales.html
    """
    gravures_originales = Oeuvre.query.filter(Oeuvre.categorie_id == 2).all()
    return render_template("pages/grav_originales.html", nom="HG_Japonisme", gravures_originales=gravures_originales)


@app.route("/notice_oeuvre/<int:id_oeuvre>")
def notice_oeuvre(id_oeuvre):
    """
    Route permettant d'afficher la notice d'une oeuvre
    :return: template notice_oeuvre.html
    """

    noticeoeuvre = Oeuvre.query.filter(Oeuvre.id_oeuvre==id_oeuvre).first()
    artiste1 = Artiste.query.filter(Artiste.oeuvres.any(Oeuvre.id_oeuvre==id_oeuvre)).first()
    techn1 = Technique.query.filter(Technique.oeuvres.any(Oeuvre.id_oeuvre==id_oeuvre)).first()
    suj1 = Sujet.query.filter(Sujet.oeuvres.any(Oeuvre.id_oeuvre==id_oeuvre)).first()
    localis1 = Localisation.query.filter(Localisation.oeuvres.any(Oeuvre.id_oeuvre==id_oeuvre)).first()
    return render_template("pages/notice_oeuvre.html", nom="HG_Japonisme", oeuvre=noticeoeuvre, artiste=artiste1, technique=techn1, sujet=suj1, localisation=localis1)


@app.route("/index_artistes")
def index_artistes() :
    """
    Route permettant d'afficher l'index des noms d'artistes
    :return: template index_artistes.html
    """
    title = "index_artistes"
    artist = Artiste.query.all()

    if len(artist) == 0:
        return render_template("pages/index_artistes.html", artist=artist, title=title)
    else : 
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

    artist = Artiste.query.order_by(Artiste.nom
            ).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_artistes.html", nom="HG_Japonisme", artist=artist, title=title)


@app.route("/index_localisations")
def index_localisations() :
    """
    Route permettant d'afficher l'index des lieux de conservation des oeuvres
    :return: template index_localisations.html
    """
    title = "index_localisations"
    lieu = Localisation.query.all()

    if len(lieu) == 0:
        return render_template("pages/index_localisations", lieu=lieu, title=title)
    else : 
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

    lieu = Localisation.query.order_by(Localisation.label_lieu_conservation
            ).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_localisations.html", nom="HG_Japonisme", lieu=lieu, title=title)


@app.route("/index_sujets")
def index_sujets() :
    """
    Route permettant d'afficher l'index des sujets associés aux oeuvres
    :return: template index_sujets.html
    """
    title = "index_sujets"
    suj = Sujet.query.all()

    if len(suj) == 0:
        return render_template("pages/index_sujets", suj=suj, title=title)
    else : 
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

    suj = Sujet.query.order_by(Sujet.label_sujet
            ).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_sujets.html", nom="HG_Japonisme", suj=suj, title=title)


@app.route("/index_techniques")
def index_techniques() :
    """
    Route permettant d'afficher l'index des techniques de réalisation des oeuvres
    :return: template index_techniques.html
    """
    title = "index_techniques"
    techn = Technique.query.all()

    if len(techn) == 0:
        return render_template("pages/index_techniques", techn=techn, title=title)
    else : 
        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

    techn = Technique.query.order_by(Technique.label_technique
            ).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
    return render_template("pages/index_techniques.html", nom="HG_Japonisme", techn=techn, title=title)


@app.route("/recherche")
def recherche():
    """
    Route permettant d'effectuer une recherche et d'afficher une liste de résultats
    :return : affichage du template recherche.html
    """

    mot_clef = request.args.get("mot_clef", None)
    page = request.args.get("page", 1)
    
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else :
        page = 1

    # création d'une liste vide pour les résultats
    resultats = []

    title = "Recherche"
    if mot_clef:
    # Si un mot_clef est entré dans la barre de recherche, les tables de la base de données sont requêtées afin de trouver les correspondances.
    # Les résultats sont stockés dans la liste 'resultats = []'
        resultats = Oeuvre.query.filter(
            or_(
                Oeuvre.titre.like("%{}%".format(mot_clef)),
                Oeuvre.date_oeuvre.like("%{}%".format(mot_clef)),
                Oeuvre.dimensions.like("%{}%".format(mot_clef)),
                Oeuvre.url_site.like("%{}%".format(mot_clef)),
                Oeuvre.manifeste_iiif.like("%{}%".format(mot_clef)),
                Oeuvre.iiif_image.like("%{}%".format(mot_clef)),
                Oeuvre.localisation.has((Localisation.label_lieu_conservation).like("%{}%".format(mot_clef))),
                Oeuvre.localisation.has((Localisation.label_ville_conservation).like("%{}%".format(mot_clef))),
                Oeuvre.categorie.has((Categorie.label_categorie).like("%{}%".format(mot_clef))),
                Oeuvre.sujet.any((Sujet.label_sujet).like("%{}%".format(mot_clef))),
                Oeuvre.technique.any((Technique.label_technique).like("%{}%".format(mot_clef))),
                Oeuvre.artiste.any((Artiste.nom).like("%{}%".format(mot_clef))),
                Oeuvre.artiste.any((Artiste.prenom).like("%{}%".format(mot_clef))),
                Oeuvre.artiste.any((Artiste.annee_naissance).like("%{}%".format(mot_clef))),
                Oeuvre.artiste.any((Artiste.annee_mort).like("%{}%".format(mot_clef)))
                )  
        ).order_by(Oeuvre.titre.asc()).paginate(page=page, per_page=RESULTATS_PAR_PAGE)
        title = "Résultats de votre recherche : " + mot_clef + "."
    return render_template("pages/recherche.html", resultats=resultats, title=title, mot_clef=mot_clef)


# Routes liées à la gestion du compte utilisateur
@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """
    Route liée à la gestion de l'inscription de l'utilisateur
    :return: template inscription.html ou redirection
    """
    if request.method == "POST":
        statut, informations = Utilisateur.creation(
            identifiant_creer=request.form.get("identifiant_creer", None),
            mot_de_passe_creer=request.form.get("mot_de_passe_creer", None),
            nom_utilisateur_creer=request.form.get("nom_utilisateur_creer", None),
            prenom_utilisateur_creer=request.form.get("prenom_utilisateur_creer", None),
            email_creer=request.form.get("email_creer", None)
            )
        
        if statut is True:
            flash("Inscription effectuée. Vous pouvez désormais vous connecter.", "success")
            return redirect("/")
        else:
            flash("Des erreurs ont été rencontrées : " + ", ".join(informations), "error")
            return render_template("pages/inscription.html", nom="HG_Japonisme")
    else:
        return render_template("pages/inscription.html", nom="HG_Japonisme")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """
    Route liée à la gestion des connexions aux comptes utilisateurs
    :return: template connexion.html ou redirection
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté.", "info")
        return redirect("/")
       
    if request.method == "POST":
        user = Utilisateur.identification(
            identifiant_u=request.form.get("identifiant_u", None), 
            mot_de_passe_u=request.form.get("mot_de_passe_u", None)
        )

        if user:
            flash("Connexion réussie", "success")
            login_user(user)
            return redirect("/")
        else:
            flash("Le nom d'utilisateur ou le mot de passe est incorrect.", "error")
    return render_template("pages/connexion.html", nom="HG_Japonisme")
login.login_view = "connexion"


@app.route("/deconnexion")
def deconnexion():
    """
    Route liée à la gestion des déconnexions des comptes utilisateurs
    :return: redirection vers la page d'accueil
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect("/")


# Routes liées à l'interface utilisateur

#Création de la notice d'une oeuvre
@app.route("/ajout_oeuvre", methods=["GET", "POST"])
@login_required
def ajout_oeuvre():
    """ 
    Route permettant l'ajout une oeuvre et les données qui lui sont associées (artiste, technique, lieu de conservation, sujet) à la BDD
    :param id_oeuvre : identifiant de l'oeuvre
    :return : template ajout_oeuvre.html (ou redirection)
    """
    # Ajout d'une oeuvre
    if request.method == "POST":
        statut, informations = Oeuvre.ajout_oeuvre(
        ajout_titre = request.form.get("ajout_titre", None),
        ajout_date_oeuvre = request.form.get("ajout_date_oeuvre", None),
        ajout_dimensions = request.form.get("ajout_dimensions", None),
        ajout_url_site = request.form.get("ajout_url_site", None),
        ajout_manifeste_iiif = request.form.get("ajout_manifeste_iiif", None), 
        ajout_iiif_image = request.form.get("ajout_iiif_image", None),
        categorie_id = request.form.get("categorie_id", None),
        localisation_id = request.form.get("localisation_id", None),
        )

        if statut is True:
            flash("Ajout d'une nouvelle oeuvre", "success")
            return redirect("/")
        else:
            flash("L'ajout d'une nouvelle oeuvre a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/ajout_oeuvre.html", nom="HG_Japonisme")
    else:
        return render_template("pages/ajout_oeuvre.html", nom="HG_Japonisme")

'''
    #Tentative de réaliser un seul formulaire pour toutes les tables : fonctionne partiellement

    # Ajout d'une technique associée à l'oeuvre
    # Stockage du label de la technique donné par l'utilisateur 
    label_technique = request.form.get("techni", None)

    # Si l'utilateur ajoute une technique, ajout à la table Technique et stockage dans techni
    # Ou bien récupération de l'enregistrement déjà existant dans la table Technique
    if label_technique:
        techni = Technique.ajout_technique(label_technique)
        # Récupération de l'id de la technique en question
        technique_id = techni.get_id()
        # Association de cette technique à l'oeuvre de la page courante
        Technique.associer_technique_et_oeuvre(technique_id, oeuvre_id)


    # Ajout d'un sujet associé à l'oeuvre
    label_sujet = request.form.get("lab_suj", None)

    if label_sujet:
        lab_suj = Sujet.ajout_sujet(label_sujet)
        id_sujet = lab_suj.get_id()
        Sujet.associer_sujet_et_oeuvre(id_sujet, id_oeuvre)


	# Ajout d'une localisation associée à l'oeuvre
    lieuconserv = request.form.get("lieu_cons", None)

    if lieuconserv:
        lieu_cons = Localisation.ajout_localisation(lieuconserv)
        id_localisation = lieu_cons.get_id()
        Localisation.associer_localisation_et_oeuvre(id_localisation, id_oeuvre)


    # Ajout d'un artiste associé à l'oeuvre
    artisteinf = request.form.get("artiste_inf", None)

    if artisteinf:
        artiste_inf = Artiste.ajout_artiste(artisteinf)
        id_artiste = artiste_inf.get_id()
        Artiste.associer_artiste_et_oeuvre(id_artiste, id_oeuvre)

    # Ajout d'une oeuvre
    if request.method == "POST":
        statut, informations = Oeuvre.ajout_oeuvre(
        ajout_titre = request.form.get("ajout_titre", None),
        ajout_date_oeuvre = request.form.get("ajout_date_oeuvre", None),
        ajout_dimensions = request.form.get("ajout_dimensions", None),
        ajout_url_site = request.form.get("ajout_url_site", None),
        ajout_manifeste_iiif = request.form.get("ajout_manifeste_iiif", None), 
        ajout_iiif_image = request.form.get("ajout_iiif_image", None),
        categorie_id = request.form.get("categorie_id", None),
        localisation_id = request.form.get("localisation_id", None),
        )

        if statut is True:
            flash("Ajout d'une nouvelle oeuvre", "success")
            return redirect("/")
        else:
            flash("L'ajout d'une nouvelle oeuvre a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/ajout_oeuvre.html", nom="HG_Japonisme")
    else:
        return render_template("pages/ajout_oeuvre.html", nom="HG_Japonisme")

'''

#Modification de la notice d'une oeuvre
@app.route("/maj_oeuvre/<int:id_oeuvre>", methods=["POST", "GET"])
@login_required
def maj_oeuvre(id_oeuvre):
    """ 
    Route permettant la modification de la notice d'une oeuvre
    :param id_oeuvre: id de l'oeuvre
    :return: template maj_oeuvre.html (ou redirection)
    """

    # En méthode GET, les éléments de l'objet oeuvre correspondant à l'identifiant de la route sont renvoyés.
    if request.method == "GET":
        modif_oeuvre = Oeuvre.query.get(id_oeuvre)
        return render_template("pages/maj_oeuvre.html", nom="HG_Japonisme", modif_oeuvre=modif_oeuvre)

    else:
        statut, informations = Oeuvre.maj_oeuvre(
            id_oeuvre=id_oeuvre,
            maj_titre=request.form.get("maj_titre", None),
            maj_date_oeuvre=request.form.get("maj_date_oeuvre", None),
            maj_dimensions=request.form.get("maj_dimensions", None),
            maj_url_site=request.form.get("maj_url_site", None),
            maj_manifeste_iiif=request.form.get("maj_manifeste_iiif", None),
            maj_iiif_image=request.form.get("maj_iiif_image", None),
            categorie_id=request.form.get("categorie_id", None),
            localisation_id=request.form.get("localisation_id", None),
        )

        if statut is True:
            flash("Modification réussie", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(informations), "danger")
            modif_oeuvre = Oeuvre.query.get(id_oeuvre)
            return render_template("pages/maj_oeuvre.html", nom="HG_Japonisme", modif_oeuvre=modif_oeuvre)

    
    
    ''' Tentative d'un seul formulaire de modification pour toutes les tables : ne fonctionne pas
    # En méthode GET, les éléments de l'objet oeuvre correspondant à l'identifiant de la route sont renvoyés.
    if request.method == "GET":
        modif_oeuvre = Oeuvre.query.get(id_oeuvre)
        return render_template("pages/maj_oeuvre.html", nom="HG_Japonisme", modif_oeuvre=modif_oeuvre)

    # Récupération des données du formulaire à modifier et modification de ces données grâce à la fonction modifier_oeuvre.
    else:
        statut, informations = Oeuvre.maj_oeuvre(
            id_oeuvre=id_oeuvre,
            maj_titre=request.form.get("maj_titre", None),
            maj_date_oeuvre=request.form.get("maj_date_oeuvre", None),
            maj_dimensions=request.form.get("maj_dimensions", None),
            maj_url_site=request.form.get("maj_url_site", None),
            maj_manifeste_iiif=request.form.get("maj_manifeste_iiif", None),
            maj_iiif_image=request.form.get("maj_iiif_image", None),
            categorie_id=request.form.get("categorie_id", None),
            localisation_id=request.form.get("localisation_id", None),
        ).join(Artiste.maj_artiste(
            id_artiste=id_artiste,
            maj_nom=request.form.get("maj_nom", None),
            maj_prenom=request.form.get("maj_prenom", None),
            maj_annee_naissance=request.form.get("maj_annee_naissance", None),
            maj_annee_mort=request.form.get("maj_annee_mort", None)
            )
        ).join(Technique.maj_technique(
            id_technique=id_technique,
            maj_label_technique=request.form.get("maj_label_technique", None)
            )
        ).join(Sujet.maj_sujet(
            id_sujet=id_sujet,
            maj_label_sujet=request.form.get("maj_label_sujet", None)
            )
        ).join(Localisation.maj_localisation(
            id_localisation=id_localisation,
            maj_label_lieu_conservation=request.form.get("maj_label_lieu_conservation", None),
            maj_label_ville_conservation=request.form.get("maj_label_ville_conservation", None)
            )
        )
      
        if statut is True:
            flash("Modification réussie", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ", ".join(informations), "danger")
            modif_oeuvre = Oeuvre.query.get(id_oeuvre)
            return render_template("pages/maj_oeuvre.html", nom="HG_Japonisme", modif_oeuvre=modif_oeuvre)
    '''

#Suppression de la notice d'une oeuvre
@app.route("/supprimer_oeuvre/<int:id_oeuvre>", methods=["POST", "GET"])
@login_required
def supprimer_oeuvre(id_oeuvre):
    """ 
    Route permettant la suppression d'une oeuvre et de ses données dans la BDD
    :param id_oeuvre : id de l'oeuvre
    :return: template supprimer_oeuvre.html (ou redirection)
    """
    suppr_oeuvre = Oeuvre.query.get(id_oeuvre)

    if request.method == "POST":
        statut = Oeuvre.supprimer_oeuvre(
            id_oeuvre=id_oeuvre
        )

        if statut is True:
            flash("Suppression réussie", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué. Réessayez !", "error")
            return redirect("/")
    else:
        return render_template("pages/supprimer_oeuvre.html", nom="HG_Japonisme", suppr_oeuvre=suppr_oeuvre)

