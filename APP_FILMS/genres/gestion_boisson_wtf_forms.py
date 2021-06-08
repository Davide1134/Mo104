"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import DateField
from wtforms.validators import Length
from wtforms.validators import Regexp


class FormWTFAjouterboisson(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    prix_boisson_wtf_regexp = "^([0-9]+.[0-9])"
    Marque_wtf = StringField("Clavioter la marque ", validators=[Length(min=2, max=20, message="min 2 max 20")])
    prix_boisson_wtf = StringField("Entre le prix ",validators=[Length(min=4, message="Format non Respecter"), Regexp(
                                                                                                             prix_boisson_wtf_regexp,message= "format demander Ex: 00.00.CHF" )])


    quantite_boisson_wtf = StringField("Entre le nombre de quantité")
    Date_achat_boisson_wtf = DateField("Entre la date d'achat")
    Date_peremption_boisson_wtf = DateField("Entre la date de péremption")
    submit = SubmitField("Enregistrer genre")

class FormWTFUpdateboisson(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    prix_boisson_update_regexp = "^([0-9]+.[0-9])"
    marque_update = StringField("Clavioter la marque ", validators=[Length(min=2, max=20, message="min 2 max 20")])
    Prix_boisson_update = StringField("Entre le prix ", validators=[Length(min=4, message="Format non Respecter"), Regexp(
        prix_boisson_update_regexp, message="format demander Ex: 00.00.CHF")])

    Quantite_boisson_update = StringField("Entre le nombre de quantité")
    Date_achat_boisson_update = DateField("Entre la date d'achat")
    Date_peremption_boisson_update = DateField("Entre la date de péremption")
    submit = SubmitField("Enregistrer")

class FormWTFDeleteboisson(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    Nom_personne_delete_wtf = StringField("Effacer ce compte ?")
    submit_btn_del = SubmitField("Effacer ")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
