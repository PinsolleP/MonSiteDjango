TP Django – Compte rendu

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

1 : Pour rajouter l'interface de la classe Choice, voici les étapes :

Ajoutez l'import Choice depuis models.

Ajoutez cette ligne : admin.site.register(Choice)

Contrôlez grâce à la commande : python manage.py runserver, puis accédez au site en ajoutant /admin.

2 :

Utilisez la commande python manage.py runserver pour accéder au site.

Sélectionnez Question et ajoutez manuellement vos questions.

Pensez à enregistrer.

Faites de même pour les choix des réponses.

3 : Pour visualiser tous les attributs de la classe, il faut sélectionner Question ou Choice pour les voir.

Nous ne pouvons pas filtrer nos données selon les attributs.

Nous ne pouvons pas trier nos données selon les attributs.

Nous ne pouvons pas chercher un contenu parmi tous les champs.

4 : L'objectif est de personnaliser l'administration pour rendre les données plus faciles à consulter.

list_display : les colonnes affichées.

list_filter : les filtres disponibles.

search_fields : les champs dans lesquels rechercher.

ordering : le tri appliqué par défaut.

Pour cela nous devons créer deux classes dans le fichier admin.py :

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('question_text',)
    ordering = ('question_text',)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'votes', 'question')
    list_filter = ('votes',)
    search_fields = ('choice_text',)
    ordering = ('choice_text',)

Ensuite nous devons enregistrer ces modèles dans l'interface d'administration :

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)

5 : Pour ajouter un nouvel utilisateur :

Dans la rubrique Authentication and Authorization, ouvre Users.

Clique sur Add user.

Renseigne un nom d'utilisateur et un mot de passe.

Enregistre le nouvel utilisateur.

Lorsque nous nous déconnectons on ne peut pas se reconnecter avec les infos de ce nouvel utilisateur.

6 : Modifiez manuellement le nouvel utilisateur créé, donnez-lui le « Statut équipe » et réinitialisez son mot de passe.

7 : Mettre à jour l'utilisateur en décochant le statut « Actif ».

2.2.2 Exercice shell

2.2.2.1 : python manage.py shell

2.2.2.1.2 :

from polls.models import Question : importe toutes nos questions.

Question.objects.all() : liste toutes les questions.

for question in Question.objects.all():
    print(question.id, question.question_text, question.pub_date)

2.2.2.2 :

Question.objects.filter(pub_date__month=10)

2.2.2.3 :

>>> q = Question.objects.get(id=2) 
>>> q.id, q.question_text, q.pub_date 
>>> q.choice_set.all() 

2.2.2.4 :

>>> for q in Question.objects.all(): 
...     q.id, q.question_text, q.pub_date 
...     for c in q.choice_set.all(): 
...         c.choice_text, c.votes 

2.2.2.5 :

>>> for q in Question.objects.all(): 
...     q, q.choice_set.count() 

2.2.2.6 :

>>> for c in Choice.objects.all().order_by('votes'): 
...     c.question.question_text, c.choice_text, c.votes 
>>> for q in 
Question.objects.all().order_by('choice__votes').values('question_
text', 'choice__choice_text', 'choice__votes'): 
...     q 
>>> for c in 
Choice.objects.all().order_by('votes').values('question__question_
text', 'choice_text', 'votes'): 
...     c 

2.2.2.7 :

Question.objects.all().order_by('-pub_date') 

2.2.2.8 :

>>> for q in Question.objects.all(): 
...     for c in q.choice_set.all(): 
...         if 'Non' in c.choice_text: 
...             print(q, c.choice_text) 
...             break 

2.2.2.9

>>> q = Question(question_text="Quelle est la couleur du cheval 
blanc d'Henri IV ?", pub_date=timezone.now()) 
>>> q.save() 
>>> q.id  # pour vérifier que la question a bien été rajoutée dans 
la base 

2.2.2.10

>>> q.choice_set.create(choice_text="Blanc", votes=0) 
>>> q.choice_set.create(choice_text="Noir", votes=0) 
>>> q.choice_set.create(choice_text="Gris clair", votes=0) 

2.2.2.11

>>> for q in Question.objects.all(): 
...     if q.was_published_recently(): 
...         q 
ou avec une compréhension de liste : 
>>> [q for q in Question.objects.all() if 
q.was_published_recently()] 

2.2.2.12

>>> from django.contrib.auth.models import User 
>>> User.objects.all() 

2.2.3 Exercice d'écriture de méthodes du modèle




