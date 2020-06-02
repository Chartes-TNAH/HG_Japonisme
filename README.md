# HG_Japonisme

HG Japonisme est une application web (python-Flask) qui vise à présenter le japonisme d'Henri Guérard (1846-1897), artiste éclectique de la fin du XIXe siècle et collectionneur, à travers son œuvre gravé. Elle a été développée par Auriane Quoix.

## Description du projet

La structure de l'application est organisée autour de deux facettes de l'œuvre de Guérard : la gravure d'interprétation et la gravure originale. La section "Reproductions d'objets", est destinée à accueillir à la fois les gravures d'interprétation et les objets ayant servi de modèle, tandis que la section "Gravures originales" présente des œuvres qui laissent davantage transparaître l'attrait profond de Guérard pour l'art japonais.
L'artiste en a à la fois adopté ses thèmes, comme le naturalisme, mais il est également parvenu à s'approprier des procédés techniques et des principes de constructions propres aux estampes japonaises.

Cette application est prévue pour pouvoir être enrichie par des contributeurs. Le contenu qu'elle présente n'est donc pas exhaustif.
Il est possible de contribuer à la base en créant un compte utilisateur.

## Technologies utilisées

L'application a été créée avec les langages Python 3, HTML, CSS, ainsi qu'à partir d'une base de données MySQL.

## Comment installer HG Japonisme ?

- Installer Python 3
- Avec le terminal, se placer à l'endroit où l'on souhaite installer l'application
- Cloner ce repository (pour cela faire un git clone + l'adresse du repository)
- Installer un environement virtuel (virtualenv ou Anaconda par exemple) puis l'activer : ```virtualenv -p python3 env``` puis ```source env/bin/activate``` (ou bien avec Anaconda, après l'avoir installé) ```conda create --name <envname> python=3``` puis ```source activate <envname>```
- Installer les librairies nécessaires au fonctionnement de l’application (pour cela voir le fichier "requirements.txt"): ```pip install -r requirements.txt```
- Lancer le fichier run.py: ```python3 run.py```
