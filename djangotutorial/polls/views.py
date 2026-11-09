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
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["frequency"] = self.object.get_choices()
        return context


class StatisticsView(generic.TemplateView):
    template_name = "polls/statistics.html"

    def get_context_data(self, **kwargs):
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
    model = Question
    template_name = "polls/results.html"


class AllQuestionsView(generic.ListView):
    template_name = "polls/all.html"

    def get_queryset(self):
        """Return all the questions."""
        return Question.objects.all()


def vote(request, question_id):
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
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def create_question(request):

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question_text = form.cleaned_data["question"]

            question = Question.objects.create(question_text=question_text, pub_date=timezone.now())

            choices = [
                form.cleaned_data["choice1"],
                form.cleaned_data["choice2"],
                form.cleaned_data["choice3"],
                form.cleaned_data["choice4"],
                form.cleaned_data["choice5"],
            ]
            for choice in choices:
                if choice:
                    Choice.objects.create(question=question,
                                          choice_text=choice
                                          )
            return redirect("polls:index")
    else:
        form = QuestionForm()

    return render(request, "polls/name.html", {"form": form})
