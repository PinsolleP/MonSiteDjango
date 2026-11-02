from django.http import HttpResponse


def index(request):
    """
        Affiche la page d'accueil de l'application Polls.

        Args:
            request: Objet HttpRequest contenant les informations
                     de la requête HTTP.

        Returns:
            HttpResponse: Réponse HTTP contenant un message de bienvenue.
        """
    return HttpResponse("Hello, world. You're at the polls index.")



