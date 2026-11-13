"""
Module de configuration de l'application polls.

Définit la classe PollsConfig utilisée par Django pour identifier
et configurer l'application, notamment le type de clé primaire
automatique utilisé par défaut dans ses modèles.
"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
        Définit la configuration générale de l'application polls.

        Attributes:
            default_auto_field (str): Type de champ utilisé par défaut
                pour les clés primaires automatiques des modèles.
            name (str): Nom Python de l'application Django.
        """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
