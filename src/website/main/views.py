from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .utils import generate_code
from . import forms
from . import models
import json, sys, logging
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

    games = models.Game.objects.filter(player_1__id=request.user.id)
    return render(request, "main/create_game.html", {'games':games})

@login_required
def game(request, game_id):
    game = models.Game.objects.get(id=game_id)
    if request.user == game.player_1 or request.user == game.player_2:
        return render(request, "main/game.html", {"game":game})
    else:
        return render(request, "main/error.html", {"error_type":"You do not have access to this game"})

    

def login_view(request):
    error = False
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
            else:
                error = True
    else:
        form = forms.LoginForm()

    return render(request, "main/login.html", locals())

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def list_avalaible_games(request):
    games = models.Game.objects.filter(game_state=0)
    return render(request, "main/list_game.html", {"games":games})
@login_required
def join_game(request, game_id):
    game = models.Game.objects.get(id=game_id)
    game.player_2 = request.user
    game.save()
    return redirect("/game/" + str(game.id))

def start_game(request, game_id):
    game = models.Game.objects.get(id=game_id)
    if game.start_game() == -1:
        return render(request, "main/error.html", {'error_type': 'Missing one player to start the game'})   

    return redirect("/game/" + str(game.id))

def action(request, game_id, action):
    game = models.Game.objects.get(id=game_id)
    game.send_direction(action, request.user)
    return redirect("/game/" + str(game.id))

class HomePageView(TemplateView):
    template_name = "main/homepage.html"
