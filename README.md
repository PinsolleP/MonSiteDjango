# TP Django – Compte rendu

1. PRESENTATION DU PROJET

1.1 Objectif

Ce TP a pour objectif de découvrir le framework Django et de comprendre son fonctionnement à travers la réalisation d'une première application web.

Il s'appuie sur le tutoriel officiel Django 5.2 et permet de découvrir progressivement les mécanismes fondamentaux du framework.

1.2 Environnement technique

Technologie

Version / Utilisation

Python / 3.13

Django / 5.2.18

SQLite3 / Moteur de base de données

PyCharm / Environnement de développement (IDE)

Git / Gestion des versions

GitHub / Hébergement du dépôt et suivi du projet

1.3 Documentation de référence

Documentation officielle Django 5.2

Tutoriel officiel Django 5.2

2.2 Exercices sur les parties 1 et 2 

2.2.1 Exercice d'administration

1 - pour rajouter l'interface de la classe choice, voici les étapes :
    - Ajoutez l'import Choice depuis models
    - Ajoutez cette ligne : admin.site.register(Choice)
    - Contrôlez grace a la commande : python manage.py runserver. puis accèder au site en ajoutant /admin 

2 - utilisez la commande python manage.py runserver pour accèder au site
    - selectionnez question et ajouter manuellement vos questions
    - pensez a enregistrer
    - faites de même pour les choix des réponses

3 - Pour visualiser tous les attributs de la classe , il faut sélectionner question ou choice pour les voirs.
  -  