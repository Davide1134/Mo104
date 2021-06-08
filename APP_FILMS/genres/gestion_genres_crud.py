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
from APP_FILMS.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_FILMS.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre
from APP_FILMS.genres.gestion_genres_wtf_forms import FormWTFDeleteGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5005/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_personne_sel = 0 >> tous les genres.
                Id_personne_sel = "n" affiche le genre dont l'id est "n"
"""


@obj_mon_application.route("/genres_afficher/<string:order_by>/<int:Id_personne_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, Id_personne_sel):
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
                if order_by == "ASC" and Id_personne_sel == 0:
                    strsql_genres_afficher = """SELECT Id_personne, Nom_personne, Mdp_personne,Email_personne FROM t_personne ORDER BY Id_personne ASC"""
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_personne"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_Id_personne_selected_dictionnaire = {"value_Id_personne_selected": Id_personne_sel}
                    strsql_genres_afficher = """SELECT Id_personne, Nom_personne, Mdp_personne,Email_personne FROM t_personne  WHERE Id_personne = %(value_Id_personne_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_Id_personne_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """SELECT Id_personne, Nom_personne, Mdp_personne,Email_personne FROM t_personne ORDER BY Id_personne DESC"""

                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and Id_personne_sel == 0:
                    flash("""La table "t_personne" est vide. !!""", "warning")
                elif not data_genres and Id_personne_sel > 0:
                    # Si l'utilisateur change l'Id_personne dans l'URL et que le genre n'existe pas,
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
    return render_template("genres/genres_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5005/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "Nom_personne_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
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
                Nom_personne_wtf = form.Nom_personne_wtf.data
                Mdp_personne_wtf = form.Mdp_personne_wtf.data
                Email_personne_wtf = form.Email_personne_wtf.data

                valeurs_insertion_dictionnaire = {"value_Nom_personne": Nom_personne_wtf,
                                                  "value_Mdp_personne_wtf": Mdp_personne_wtf,
                                                  "value_Email_personne_wtf": Email_personne_wtf
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_personne = """INSERT INTO t_personne (Id_personne,Nom_personne, Mdp_personne,Email_personne) VALUES (NULL,%(value_Nom_personne)s,%(value_Mdp_personne_wtf)s,%(value_Email_personne_wtf)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_personne, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('genres_afficher', order_by='DESC', Id_personne_sel=0))

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

    return render_template("genres/genres_ajouter_wtf.html", form=form)


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


@obj_mon_application.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "Id_personne"
    Id_personne_update = request.values['Id_personne_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            Nom_personne_update = form_update.Nom_personne_update_wtf.data
            Nom_personne_update = Nom_personne_update.capitalize()

            Mdp_personne_update = form_update.Mdp_personne_update_wtf.data
            Mdp_personne_update = Mdp_personne_update.capitalize()

            Email_personne_update = form_update.Email_personne_update_wtf.data
            Email_personne_update = Email_personne_update.capitalize()

            valeur_update_dictionnaire = {"value_Id_personne": Id_personne_update,
                                          "value_Nom_personne": Nom_personne_update,
                                          "value_Mdp_personne": Mdp_personne_update,
                                          "value_Email_personne": Email_personne_update}

            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_personne SET Nom_personne = %(value_Nom_personne)s,Mdp_personne = %(value_Mdp_personne)s,Email_personne = %(value_Email_personne)s WHERE Id_personne = %(value_Id_personne)s"""

            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Compte mis à jour !!", "success")
            print(f"Compte mis à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"Id_personne_update"
            return redirect(url_for('genres_afficher', order_by="ASC", Id_personne_sel=0))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "Id_personne" et "intitule_genre" de la "t_personne"
            str_sql_Id_personne = "SELECT Id_personne, Nom_personne,Mdp_personne,Email_personne  FROM t_personne WHERE Id_personne = %(value_Id_personne)s"
            valeur_select_dictionnaire = {"value_Id_personne": Id_personne_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_Id_personne, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_Nom_personne = mybd_curseur.fetchone()

            print(" ", data_Nom_personne, " type ", type(data_Nom_personne), " genre ",
                  data_Nom_personne["Nom_personne"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_update_wtf.html"
            form_update.Nom_personne_update_wtf.data = data_Nom_personne["Nom_personne"]
            form_update.Mdp_personne_update_wtf.data = data_Nom_personne["Mdp_personne"]
            form_update.Email_personne_update_wtf.data = data_Nom_personne["Email_personne"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans genre_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans genre_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")
        flash(f"Erreur dans genre_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")
        flash(f"__KeyError dans genre_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("genres/genre_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete

    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"

    Paramètres : sans

    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


# ****************************************
# BOUTON SUPRIMMER !!!!!!!!!!!
# *****************************************
@obj_mon_application.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "Id_personne"
    Id_personne_delete = request.values['Id_personne_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", Id_personne_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = ['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_Id_personne": Id_personne_delete,
                                              }

                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                # str_sql_delete_films_genre = """DELETE FROM t_personne_film WHERE fk_genre = %(value_Id_personne)s"""
                str_sql_delete_idgenre = """DELETE FROM t_personne WHERE Id_personne = %(value_Id_personne)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_personne_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_personne_film"
                with MaBaseDeDonnee() as mconn_bd:
                    # mconn_bd.mabd_execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('genres_afficher', order_by="ASC", Id_personne_sel=0))



    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans genre_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans genre_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")

        flash(f"Erreur dans genre_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")

        flash(f"__KeyError dans genre_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("genres/genre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)