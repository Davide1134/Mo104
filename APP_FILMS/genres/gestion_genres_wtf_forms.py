"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms import PasswordField

class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    Nom_personne_wtf = StringField("Clavioter le Nom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_genre_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    Mdp_personne_wtf = PasswordField("Clavioter le MDP", validators=[Length(min=8, max=200, message="8 caractère minimum")])
    Email_personne_regexp = '[a-zA-Z0-9_\-]+@([a-zA-Z0-9_\-]+\.)+(com|org|edu|nz|au|fr|ch)'
    Email_personne_wtf = StringField("Clavioter l'email", validators=[Length(min=8, max=30, message="min 2 max 20"), Regexp(Email_personne_regexp,
                                                                                                                                 message="Email imposible, Ex: "
                                                                                                                                         "Prenom@email.ch "
                                                                                                                                         )])
    submit = SubmitField("Enregistrer genre")

class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    nom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    Nom_personne_update_wtf = StringField("Modifier le Nom", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])

    Mdp_personne_update_wtf = PasswordField("Clavioterr le MDP", validators=[Length(min=8, max=200, message="8 caractère minimum")])
    Email_personne_update_regexp = '[a-zA-Z0-9_\-]+@([a-zA-Z0-9_\-]+\.)+(com|org|edu|nz|au|fr|ch)'
    Email_personne_update_wtf = StringField("Modifier l'email",validators=[Length(min=8, max=30, message="min 2 max 20"), Regexp(Email_personne_update_regexp,
                                                                                                                                 message="Email imposible, Ex: "
                                                                                                                                         "Prenom@email.ch "
                                                                                                                                         )])
    submit = SubmitField("Enregistrer")

class FormWTFDeleteGenre(FlaskForm):
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
