"""
Module contenant les vues de l'application polls.

Les vues assurent la liaison entre les requêtes HTTP des utilisateurs,
les modèles de données, les formulaires et les templates Django.

Le module gère notamment :
- l'affichage des questions et de leurs détails ;
- l'enregistrement des votes ;
- l'affichage des résultats et des fréquences ;
- le calcul des statistiques générales ;
- la création de nouveaux sondages.
"""
from django.db.models.aggregates import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm
from .models import Choice, Question


class IndexView(generic.ListView):
    """
        Affiche les cinq questions les plus récemment publiées.

        Utilise le modèle Question et le template polls/index.html.

        Attributes:
            template_name (str): Chemin du template utilisé.
            context_object_name (str): Nom de la variable contenant
                la liste des questions dans le template.
        """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """
        Affiche les détails d'une question sélectionnée.

        Utilise le modèle Question pour récupérer automatiquement
        l'objet correspondant à l'identifiant transmis dans l'URL.

        Attributes:
            model: Modèle utilisé pour récupérer la question.
            template_name (str): Chemin du template de détail.
        """
    model = Question
    template_name = "polls/detail.html"


class FrequencyView(generic.DetailView):
    """
        Affiche les fréquences et les pourcentages des votes
        pour une question sélectionnée.

        Récupère les résultats calculés par la méthode get_choices()
        du modèle Question et prépare les données destinées au template.

        Attributes:
            model: Modèle utilisé pour récupérer la question.
            template_name (str): Chemin du template des fréquences.
        """
    model = Question
    template_name = "polls/frequency.html"

    def get_context_data(self, **kwargs):
        """
                Complète le contexte transmis au template des fréquences.

                Ajoute les résultats détaillés, les libellés des choix
                et leurs pourcentages arrondis à deux décimales.

                Args:
                    **kwargs: Arguments supplémentaires transmis à la méthode
                        de contexte de la classe parente.

                Returns:
                    dict: Contexte contenant les informations nécessaires
                    à l'affichage des fréquences.
                """
        context = super().get_context_data(**kwargs)
        context["frequency"] = self.object.get_choices()
        context["labels"] = [c[0] for c in context["frequency"]]
        context["percentages"] = [round(c[2], 2) for c in context["frequency"]]
        return context


class StatisticsView(generic.TemplateView):
    """
        Affiche les statistiques générales de l'application polls.

        Calcule le nombre total de questions, de choix et de votes,
        ainsi que la moyenne de votes par question.

        Attributes:
            template_name (str): Chemin du template des statistiques.
        """
    template_name = "polls/statistics.html"

    def get_context_data(self, **kwargs):
        """
                Calcule et ajoute les statistiques générales au contexte.

                Utilise les agrégations Django pour obtenir le nombre total
                de votes et calcule la moyenne de votes par question.

                Args:
                    **kwargs: Arguments supplémentaires transmis à la méthode
                        de contexte de la classe parente.

                Returns:
                    dict: Contexte contenant les statistiques calculées.
                """
        context = super().get_context_data(**kwargs)
        context["total_questions"] = Question.objects.count()
        context["total_choices"] = Choice.objects.count()
        resultat = Choice.objects.aggregate(total=Sum("votes"))
        total_votes = resultat["total"] or 0
        context["total_votes"] = total_votes
        if context["total_questions"] > 0:
            context["average_votes"] = context["total_votes"] / context["total_questions"]
        else:
            context["average_votes"] = 0
        return context


class ResultsView(generic.DetailView):
    """
        Affiche les résultats d'une question sélectionnée.

        Utilise le modèle Question pour récupérer l'objet correspondant
        à l'identifiant transmis dans l'URL.

        Attributes:
            model: Modèle utilisé pour récupérer la question.
            template_name (str): Chemin du template des résultats.
        """
    model = Question
    template_name = "polls/results.html"


class AllQuestionsView(generic.ListView):
    """
        Affiche la liste complète des questions enregistrées.

        Contrairement à IndexView, cette vue ne limite pas
        le nombre de questions récupérées.

        Attributes:
            template_name (str): Chemin du template utilisé.
        """
    template_name = "polls/all.html"

    def get_queryset(self):
        """
                Récupère toutes les questions enregistrées en base de données.

                Returns:
                    QuerySet: Ensemble des questions existantes.
                """
        """Return all the questions."""
        return Question.objects.all()


def vote(request, question_id):
    """
        Traite le vote d'un utilisateur pour une question donnée.

        Récupère la question et le choix transmis par le formulaire.
        Si le choix est valide, incrémente son nombre de votes
        puis redirige l'utilisateur vers la page des fréquences.

        En cas d'absence ou d'invalidité du choix, réaffiche
        le formulaire avec un message d'erreur.

        Args:
            request: Objet représentant la requête HTTP.
            question_id (int): Identifiant de la question concernée.

        Returns:
            HttpResponse: Réponse HTTP affichant le formulaire
            ou redirigeant vers la page des fréquences.
        """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:frequency", args=(question.id,)))


def create_question(request):
    """
        Permet à un utilisateur authentifié de créer un nouveau sondage.

        Vérifie l'authentification de l'utilisateur, traite le formulaire
        QuestionForm, crée la question puis enregistre les choix renseignés.

        Les deux premières réponses sont obligatoires et les suivantes
        sont facultatives selon les règles définies dans QuestionForm.

        Args:
            request: Objet représentant la requête HTTP.

        Returns:
            HttpResponse: Redirection vers la page d'accueil après
            la création du sondage ou affichage du formulaire de création.
        """
    if not request.user.is_authenticated:
        return redirect("polls:index")

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question_text = form.cleaned_data["question"]

            question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
            question.save()

            choices = [
                form.cleaned_data["choice1"],
                form.cleaned_data["choice2"],
                form.cleaned_data["choice3"],
                form.cleaned_data["choice4"],
                form.cleaned_data["choice5"],
            ]
            for choice in choices:
                if choice:
                    obj_choice = Choice.objects.create(question=question,
                                                       choice_text=choice
                                                       )
                    obj_choice.save()
            return redirect("polls:index")
    else:
        form = QuestionForm()

    return render(request, "polls/name.html", {"form": form})
