import os
import io
from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
#from queries import *
from django.urls import reverse

from app.queries import *

global prev_id
prev_id = 0



def index(request):

    #print(info)
    tparams = {
        'countries' : "info",
        'default_message': "Game categories",
        'total_cases' : "total_cases",
        'total_deaths' : "total_deaths",
        'array_cases' : "array_monthCases",
        'array_deaths' : "array_monthDeaths",
    }

    return render(request, 'index.html', tparams)

def table(request):

    tparams =  {
        'xml' : "html",
        'sel_date' : "sel_date"
    }

    #return HttpResponse(html)
    return render(request, "table.html", tparams)

def admin(request):


    tparams = {
        'countries': "info",
        'default_message': "Select country",
        'error' : "error"
    }
    return render(request,'admin.html', tparams)

def admin_update(request, countryID): #updating  view


    tparams = {
        'countries': "info",
        'default_message': "country_name",
        'error' :"error"
    }

    return render(request, 'admin.html', tparams)

global prev_gen
prev_gen = "Select game gender"

def store(request):
    global prev_gen
    genres_list = get_genres()
    game_list = get_games()

    print(game_list)
    #print(genres_list)


    if request.method == "GET":  # carregar a pag
        sel_gen = "Select game gender"

    if request.method == "POST" and "genderSelect" in request.POST:
        sel_gen = request.POST["genderSelect"]
        print(sel_gen)

    if prev_gen == sel_gen:
        sel_gen = "Select game gender"
    else:
        prev_gen = sel_gen

    if sel_gen != "Select game gender":
        game_list = get_games_by_genre(str(sel_gen))

    tparams = {
        'default_message': sel_gen,
        'genres': genres_list,
        'game_properties': game_list
    }
    return render(request, 'news.html', tparams)



