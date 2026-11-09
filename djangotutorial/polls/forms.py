from django import forms


class QuestionForm(forms.Form):
    question = forms.CharField(label="Votre question", max_length=200, required=True)
    choice1 = forms.CharField(label="Votre réponse 1", max_length=100, required=True)
    choice2 = forms.CharField(label="Votre réponse 2", max_length=100, required=True)
    choice3 = forms.CharField(label="Votre réponse 3", max_length=100, required=False)
    choice4 = forms.CharField(label="Votre réponse 4", max_length=100, required=False)
    choice5 = forms.CharField(label="Votre réponse 5", max_length=100, required=False)
