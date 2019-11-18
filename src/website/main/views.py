from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .utils import generate_code
from . import forms
from . import models
import json
import sys
import logging
sys.path.append("../")
from game_logic.game import Game

views_logger = logging.getLogger(__name__)
games = {}

@login_required
def create_game(request):
    if request.method == "POST":
        if request.POST["create_game"] == "true":
            game = models.Game(player_1=request.user)
            game.save()
            views_logger.info("A game was created by user %s", request.user.username)
        else:
            views_logger.warning("Error while creating a game or POST request with missing input field - user %s", request.user.username)

    games = models.Game.objects.all()
    return render(request, "main/create_game.html", {'games':games})

def login(request):
    error = False
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                auth_login(request, user)
            else:
                error = True
    else:
        form = forms.LoginForm()

    return render(request, "main/login.html", locals())

def logging_out(request):
    logout(request)
    return redirect("/")
class HomePageView(TemplateView):
    template_name = "main/homepage.html"
