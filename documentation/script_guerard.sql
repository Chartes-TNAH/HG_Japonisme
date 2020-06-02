PRAGMA encoding = 'UTF-8';

CREATE TABLE IF NOT EXISTS oeuvre (
  id_oeuvre         			  INTEGER PRIMARY KEY AUTOINCREMENT,                     
  titre       					    TEXT NOT NULL,
  date_oeuvre					      TEXT,                           
  dimensions  					    TEXT,									
  url_site	  					    TEXT,                                    
  manifeste_iiif				    TEXT,
  iiif_image					      TEXT,
  localisation_id				    INTEGER NOT NULL REFERENCES localisation(id_localisation),
  categorie_id              INTEGER NOT NULL REFERENCES categorie(id_categorie)
);

CREATE TABLE IF NOT EXISTS artiste (
  id_artiste        			  INTEGER PRIMARY KEY AUTOINCREMENT,
  nom        					      TEXT NOT NULL,                          
  prenom   						      TEXT,    
  annee_naissance				    INTEGER,
  annee_mort					      INTEGER             
);

CREATE TABLE IF NOT EXISTS creer (
  oeuvre_id         			  INTEGER NOT NULL REFERENCES oeuvre(id_oeuvre),
  artiste_id					      INTEGER NOT NULL REFERENCES artiste(id_artiste),
  PRIMARY KEY (oeuvre_id, artiste_id)  
);

CREATE TABLE IF NOT EXISTS technique (
  id_technique      			  INTEGER PRIMARY KEY AUTOINCREMENT,
  label_technique				    TEXT
);

CREATE TABLE IF NOT EXISTS avoir_technique (
  oeuvre_id						      INTEGER NOT NULL REFERENCES oeuvre(id_oeuvre),
  technique_id      			  INTEGER NOT NULL REFERENCES technique(id_technique),
  PRIMARY KEY (oeuvre_id, technique_id)
);

CREATE TABLE IF NOT EXISTS localisation (
  id_localisation   		    INTEGER PRIMARY KEY AUTOINCREMENT,
  label_lieu_conservation		TEXT, 
  label_ville_conservation	TEXT  
);

CREATE TABLE IF NOT EXISTS categorie (
  id_categorie              INTEGER PRIMARY KEY AUTOINCREMENT,
  label_categorie           TEXT
);

CREATE TABLE IF NOT EXISTS sujet (
  id_sujet			   		      INTEGER PRIMARY KEY AUTOINCREMENT,
  label_sujet					      TEXT
);

CREATE TABLE IF NOT EXISTS avoir_sujet (
  oeuvre_id         		    INTEGER NOT NULL REFERENCES oeuvre(id_oeuvre),
  sujet_id			   			    INTEGER NOT NULL REFERENCES sujet(id_sujet),
  PRIMARY KEY (oeuvre_id, sujet_id)
);

CREATE TABLE IF NOT EXISTS utilisateur (
  id_utilisateur            INTEGER PRIMARY KEY AUTOINCREMENT,
  identifiant			   		    TEXT NOT NULL,
  mot_de_passe					    TEXT NOT NULL,
  nom_utilisateur						TEXT NOT NULL,
  prenom_utilisateur				TEXT NOT NULL,
  email							        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS contribution_utilisateur (
  utilisateur_id            INTEGER NOT NULL REFERENCES utilisateur(id_utilisateur),
  oeuvre_id                 INTEGER NOT NULL REFERENCES oeuvre(id_oeuvre),
  artiste_id                INTEGER NOT NULL REFERENCES artiste(id_artiste),
  sujet_id                  INTEGER NOT NULL REFERENCES sujet(id_sujet),
  technique_id              INTEGER NOT NULL REFERENCES technique(id_technique),
  localisation_id           INTEGER NOT NULL REFERENCES localisation(id_localisation),
  contribution_date         DATETIME DEFAULT CURENT_TIMESTAMP
);
