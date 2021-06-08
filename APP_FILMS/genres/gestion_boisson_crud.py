"""
    Fichier : gestion_genres_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les genres.
"""
import re
import sys

from flask import flash, session
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask_wtf import form

from APP_FILMS import obj_mon_application
from APP_FILMS.database.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.erreurs.msg_erreurs import *
from APP_FILMS.erreurs.exceptions import *
from APP_FILMS.essais_wtf_forms.wtf_forms_1 import MonPremierWTForm
from APP_FILMS.genres.gestion_boisson_wtf_forms import FormWTFAjouterboisson
from APP_FILMS.genres.gestion_boisson_wtf_forms import FormWTFUpdateboisson
from APP_FILMS.genres.gestion_boisson_wtf_forms import FormWTFDeleteboisson

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5005/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                Id_boisson_sel = 0 >> tous les genres.
                Id_boisson_sel = "n" affiche le genre dont l'id est "n"
"""


@obj_mon_application.route("/boisson_afficher.html/<string:order_by>/<int:Id_boisson_sel>", methods=['GET', 'POST'])
def boisson_afficher(order_by, Id_boisson_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion genres ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and Id_boisson_sel == 0:
                    strsql_boisson_afficher = """SELECT Id_boisson,Type_boisson, Marque, Prix_boisson,quantite_boisson,Date_achat_boisson,Date_peremption_boisson FROM t_boisson,t_type_boisson ORDER BY Id_boisson,fk_tp_boisson ASC"""
                    mc_afficher.execute(strsql_boisson_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_personne"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_Id_boisson_selected_dictionnaire = {"value_Id_boisson_selected": Id_boisson_sel

                                                               }
                    strsql_boisson_afficher = """SELECT Id_boisson,Type_boisson, Marque, Prix_boisson,quantite_boisson,Date_achat_boisson,Date_peremption_boisson FROM t_boisson,t_type_boisson  WHERE Id_boisson = %(value_Id_boisson_selected)s,	fk_tp_boisson = %(value_fk_tp_boisson_selected)s"""

                    mc_afficher.execute(strsql_boisson_afficher, valeur_Id_boisson_selected_dictionnaire)
                else:
                    strsql_boisson_afficher = """SELECT Id_boisson, Type_boisson, Marque, Prix_boisson, quantite_boisson,Date_achat_boisson,Date_peremption_boisson FROM t_boisson,t_type_boisson ORDER BY Id_boisson,fk_tp_boisson DESC"""

                    mc_afficher.execute(strsql_boisson_afficher)

                data_boisson = mc_afficher.fetchall()

                print("data_genres ", data_boisson, " Type : ", type(data_boisson))

                # Différencier les messages si la table est vide.
                if not data_boisson and Id_boisson_sel == 0:
                    flash("""La table "t_boisson" est vide. !!""", "warning")
                elif not data_boisson and Id_boisson_sel > 0:
                    # Si l'utilisateur change l'Id_boisson dans l'URL et que le genre n'existe pas,
                    flash(f"Le Compte demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_personne" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Comptes affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur}")
            raise Exception(f"RGG Erreur générale. {erreur}")
            raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("genres/boisson_afficher.html", data=data_boisson)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5005/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "marque_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/boisson_ajouter_wtf.html", methods=['GET', 'POST'])
def boisson_ajouter_wtf():
    form = FormWTFAjouterboisson()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion genres ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():

                Marque_wtf = form.Marque_wtf.data
                prix_boisson_wtf = form.prix_boisson_wtf.data
                quantite_boisson_wtf = form.quantite_boisson_wtf.data
                Date_achat_boisson_wtf = form.Date_achat_boisson_wtf.data
                Date_peremption_boisson_wtf = form.Date_peremption_boisson_wtf.data


                valeurs_insertion_dictionnaire = {

                                                  "value_Marque_wtf": Marque_wtf,
                                                  "value_prix_boisson_wtf": prix_boisson_wtf,
                                                  "value_quantite_boisson_wtf": quantite_boisson_wtf,
                                                  "value_Date_achat_boisson_wtf": Date_achat_boisson_wtf,
                                                  "value_Date_peremption_boisson_wtf": Date_peremption_boisson_wtf
                                                  }

                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_boisson = """INSERT INTO t_boisson (Id_boisson, Marque,Prix_boisson,quantite_boisson,Date_achat_boisson,Date_peremption_boisson) VALUES (NULL,%(value_Marque_wtf)s,%(value_prix_boisson_wtf)s,%(value_quantite_boisson_wtf)s,%(value_Date_achat_boisson_wtf)s,%(value_Date_peremption_boisson_wtf)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_boisson, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('boisson_afficher', order_by='DESC', Id_boisson_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_genre_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_genre_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_genr_crud:
            code, msg = erreur_gest_genr_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion genres CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_genr_crud.args[0]} , "
                  f"{erreur_gest_genr_crud}", "danger")


    return render_template("genres/boisson_ajouter_wtf.html", form=form)





"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update

    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""
