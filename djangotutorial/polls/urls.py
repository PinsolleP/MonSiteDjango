from django.urls import path

from . import views

"""
Configuration des URL de l'application Polls.

Ce module définit les routes accessibles dans l'application
et associe chaque URL à une vue Django correspondante.
"""

app_name = "polls"

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
