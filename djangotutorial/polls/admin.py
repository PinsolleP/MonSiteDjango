"""
Module de configuration de l'administration Django de l'application polls.

Personnalise l'affichage et la gestion des modèles Question et Choice
dans l'interface d'administration Django.

Permet notamment d'intégrer les choix directement dans le formulaire
d'une question et de configurer les listes, filtres et recherches.
"""
from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """
        Permet de gérer les choix d'une question directement dans son formulaire.

        Utilise un affichage sous forme de tableau pour intégrer les objets
        Choice associés à une question.

        Attributes:
            model: Modèle utilisé pour les éléments intégrés (Choice).
            extra: Nombre de formulaires vides supplémentaires affichés.
        """
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """
        Personnalise l'interface d'administration du modèle Question.

        Organise les champs du formulaire et configure l'affichage des
        questions, les filtres, la recherche et le tri.

        Attributes:
            fieldsets: Groupes de champs affichés dans le formulaire.
            inlines: Éléments Choice intégrés au formulaire de question.
            list_display: Colonnes affichées dans la liste des questions.
            list_filter: Champs utilisés pour filtrer les questions.
            search_fields: Champs utilisés pour rechercher des questions.
            ordering: Ordre initial de classement des questions.
        """
    fieldsets = [
        (None, {"fields": ['question_text']}),
        ("Date information", {"fields": ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ('question_text', 'pub_date')
    search_fields = ('question_text', 'pub_date')
    ordering = ('question_text', 'pub_date')


class ChoiceAdmin(admin.ModelAdmin):
    """
        Personnalise l'interface d'administration du modèle Choice.

        Configure les colonnes affichées, les possibilités de filtrage,
        la recherche et l'ordre de classement des choix.

        Attributes:
            list_display: Colonnes affichées dans la liste des choix.
            list_filter: Champs utilisés pour filtrer les choix.
            search_fields: Champs utilisés pour rechercher des choix.
            ordering: Ordre initial de classement des choix.
        """
    list_display = ('choice_text', 'votes', 'question')
    list_filter = ('choice_text', 'votes', 'question')
    search_fields = ('choice_text', 'votes', 'question')
    ordering = ('choice_text',)


# Enregistrement des modèles dans l'administration Django.
# Chaque modèle est associé à sa classe de personnalisation.

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
