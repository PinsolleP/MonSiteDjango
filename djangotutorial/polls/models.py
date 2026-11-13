"""
Module contenant les modèles de données de l'application polls.

Définit les modèles Question et Choice, leurs relations ainsi que
les méthodes permettant de calculer les résultats des sondages.
"""
import datetime

from django.contrib import admin
from django.db import models
from django.db.models import Sum
from django.utils import timezone

MAX_LENGTH = 20
"""Longueur maximale des textes affichés dans les représentations abrégées."""

def text_excerpt(text, max_length):
    """
        Retourne un extrait de texte limité à une longueur donnée.

        Ajoute trois points de suspension si le texte dépasse la limite.

        Args:
            text (str): Texte à raccourcir.
            max_length (int): Nombre maximal de caractères à conserver.

        Returns:
            str: Texte complet ou extrait suivi de points de suspension.
        """
    return text[:max_length] + ('...' if len(text) > max_length else '')


class Question(models.Model):
    """
        Représente un sondage créé dans l'application.

        Chaque question possède un texte, une date de publication
        et peut être associée à plusieurs choix de réponse.
        """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """
                Retourne une représentation textuelle de la question.

                Affiche la date de publication suivie d'un extrait
                du texte de la question.

                Returns:
                    str: Date de publication et texte abrégé.
                """
        return "{} {}".format(self.pub_date, text_excerpt(self.question_text, MAX_LENGTH))

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        """
                Vérifie si la question a été publiée au cours des dernières 24 heures.

                Returns:
                    bool: True si la publication date de moins d'un jour,
                    False dans le cas contraire.
                """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def age(self):
        """
                Calcule le temps écoulé depuis la publication de la question.

                Returns:
                    datetime.timedelta: Durée écoulée depuis la publication.
                """
        return timezone.now() - self.pub_date

    def get_choices(self):
        """
                Récupère les choix associés à la question et calcule
                le nombre de votes ainsi que leur pourcentage respectif.

                Le total des votes est calculé avec l'agrégation Sum.
                Si aucun vote n'a été enregistré, les pourcentages
                sont fixés à zéro afin d'éviter une division par zéro.

                Returns:
                    list: Liste de tuples contenant :
                        - le texte du choix ;
                        - le nombre de votes ;
                        - le pourcentage de votes.
                """
        choices = self.choice_set.all()
        resultat = self.choice_set.aggregate(total=Sum('votes'))
        total = resultat['total'] or 0
        if total == 0:
            return [(c.choice_text, c.votes, 0) for c in choices]
        else:
            return [(c.choice_text, c.votes, (c.votes / total) * 100) for c in choices]

    def get_max_choice(self):
        """
                Identifie le choix ayant la plus grande proportion de votes.

                Compare les votes de chaque choix au total des votes
                enregistrés pour la question.

                Returns:
                    tuple: Texte du choix gagnant et proportion de votes
                    exprimée sous forme décimale (entre 0 et 1).

                Note:
                    Cette méthode suppose que la question possède des choix
                    et que le total des votes est supérieur à zéro.
                """
        choices = self.choice_set.all()
        resultat = self.choice_set.aggregate(total=Sum('votes'))
        total = resultat['total']
        max_choice = max(choices, key=lambda c: c.votes / total)
        return (max_choice.choice_text, max_choice.votes / total)


class Choice(models.Model):
    """
        Représente une réponse possible à une question.

        Chaque choix est rattaché à une question et possède
        un texte ainsi qu'un nombre de votes.
        """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
                Retourne une représentation textuelle du choix.

                Le texte est limité à la longueur définie par MAX_LENGTH.

                Returns:
                    str: Texte abrégé du choix.
                """
        return text_excerpt(self.choice_text, MAX_LENGTH)
