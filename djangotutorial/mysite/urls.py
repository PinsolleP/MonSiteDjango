"""
Configuration des URL du projet mysite.

La liste `urlpatterns` associe les URL aux vues.
Pour plus d'informations, consultez :
https://docs.djangoproject.com/en/5.2/topics/http/urls/

Exemples :

Vues basées sur des fonctions
    1. Ajouter un import : from my_app import views
    2. Ajouter une URL à urlpatterns : path('', views.home, name='home')

Vues basées sur des classes
    1. Ajouter un import : from other_app.views import Home
    2. Ajouter une URL à urlpatterns : path('', Home.as_view(), name='home')

Inclure une autre configuration d'URL
    1. Importer la fonction include() : from django.urls import include, path
    2. Ajouter une URL à urlpatterns : path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
] + debug_toolbar_urls()
