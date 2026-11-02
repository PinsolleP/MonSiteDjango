from django.urls import path

from . import views

"""
Configuration des URL de l'application Polls.

Ce module définit les routes accessibles dans l'application
et associe chaque URL à une vue Django correspondante.
"""

urlpatterns = [
    path("", views.index, name="index"),
]
