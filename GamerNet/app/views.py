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

global prev_acc
prev_acc = "Select Account"


def admin(request):
    global prev_acc
    account_list = get_accounts()
    account_list.sort()
    #print(account_list)
    name = ""
    nick = ""
    games_owned = ""
    if request.method == "GET":  # carregar a pag
        sel_acc = "Select Account"
    if request.method == "POST" and "accountSelect" in request.POST:
        sel_acc = request.POST["accountSelect"]


    if prev_acc == sel_acc:
        sel_acc = "Select Account"
    else:
        prev_acc = sel_acc

    if sel_acc != "Select Account":
        person_info = get_person_info(str(sel_acc))
        name = person_info.pop(0)
        nick = person_info.pop(0)
        games_owned = person_info.copy()



    tparams = {
        'accounts': account_list,
        'default_message': sel_acc,
        'name': name,
        'nick': nick,
        'games': games_owned,
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

global globl_gen
globl_gen = "Select game gender"

def store(request):
    global globl_gen
    sel_gen = "Select game gender"
    place_message = "Search a game"
    warn_message = ""
    genres_list = get_genres()
    game_list = get_games()

    print(game_list)
    #print(genres_list)

    print(request.GET)

    if request.method == "GET" and "genderSelect" in request.GET:
        sel_gen = request.GET["genderSelect"]
        globl_gen =sel_gen
        game_list = get_games_by_genre(str(sel_gen))
        print(sel_gen)

    if request.method == "GET" and "searchGame" in request.GET:
        game_name = request.GET["searchGame"]
        place_message = game_name
        if globl_gen != "Select game gender":
            game_list = search_game(game_name, globl_gen)
        else: game_list = search_game(game_name)


    if len(game_list) == 0:
        warn_message = "Didn't find any results"


    tparams = {
        'default_message': sel_gen,
        'warn_message': warn_message,
        'genres': genres_list,
        'place_message': place_message,
        'game_properties': game_list
    }
    return render(request, 'news.html', tparams)



