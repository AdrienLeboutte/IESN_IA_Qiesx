"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_view, name="login_view"),
    path('create_game/', views.create_game),
    path('', views.HomePageView.as_view(), name="homepage"),
    path('game/<str:game_id>/', views.game),
    path('logout/', views.logout_view),
    path('list_games/', views.list_avalaible_games),
    path('join_game/<str:game_id>/', views.join_game),
    path('start_game/<str:game_id>/', views.start_game),
    path('signup/', views.sign_up_view, name="signup_view")
]
