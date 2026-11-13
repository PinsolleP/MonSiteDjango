"""
Module contenant les formulaires de l'application polls.

Définit les formulaires utilisés pour recueillir et valider
les informations saisies par les utilisateurs lors de la création
d'un sondage.
"""
from django import forms


class QuestionForm(forms.Form):
    """
        Formulaire de création d'un sondage.

        Permet à l'utilisateur de saisir une question et jusqu'à
        cinq réponses possibles.

        Les deux premières réponses sont obligatoires.
        Les trois suivantes sont facultatives.

        Le formulaire assure la validation des données saisies
        avant leur traitement par la vue.

        Attributes:
            question (CharField): Texte de la question, obligatoire,
                limité à 200 caractères.
            choice1 (CharField): Première réponse, obligatoire,
                limitée à 100 caractères.
            choice2 (CharField): Deuxième réponse, obligatoire,
                limitée à 100 caractères.
            choice3 (CharField): Troisième réponse facultative,
                limitée à 100 caractères.
            choice4 (CharField): Quatrième réponse facultative,
                limitée à 100 caractères.
            choice5 (CharField): Cinquième réponse facultative,
                limitée à 100 caractères.
        """
    question = forms.CharField(label="Votre question", max_length=200, required=True)
    choice1 = forms.CharField(label="Votre réponse 1", max_length=100, required=True)
    choice2 = forms.CharField(label="Votre réponse 2", max_length=100, required=True)
    choice3 = forms.CharField(label="Votre réponse 3", max_length=100, required=False)
    choice4 = forms.CharField(label="Votre réponse 4", max_length=100, required=False)
    choice5 = forms.CharField(label="Votre réponse 5", max_length=100, required=False)
