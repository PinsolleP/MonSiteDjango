"""
Configuration des URL de l'application polls.

Ce module définit les routes accessibles pour l'application
et associe chaque URL à une vue chargée de traiter la requête.

Les noms de routes sont regroupés dans l'espace de noms "polls",
ce qui permet de les appeler sous la forme "polls:nom_de_route".
"""
from django.urls import path

from . import views

# Espace de noms de l'application.
# Permet de distinguer les routes de polls de celles des autres applications.

app_name = "polls"

# Déclaration des routes de l'application.
urlpatterns = [
    # Page d'accueil : affiche les cinq dernières questions.
    path("", views.IndexView.as_view(), name="index"),

    # Détail d'une question identifiée par sa clé primaire (pk).
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),

    # Résultats d'une question identifiée par sa clé primaire.
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),

    # Enregistrement d'un vote pour une question donnée.
    # La valeur question_id est transmise à la fonction vote().
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # Affichage de l'ensemble des questions.
    path("all/", views.AllQuestionsView.as_view(), name="all"),

    # Affichage des fréquences et pourcentages d'une question.
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),

    # Affichage des statistiques générales de l'application.
    path("statistics/", views.StatisticsView.as_view(), name="statistics"),
    
    # Accès au formulaire de création d'un nouveau sondage.
    path("add/", views.create_question, name="add"),
]
