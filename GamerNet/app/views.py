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

color_people = "RoyalBlue"
color_friends = "white"
make_action = "Add Friend"
sel = "Make Friend"
def table(request):
    account = globl_acc


    global color_people
    global color_friends
    global make_action
    global sel
    if request.method == "GET" and "myinput" in request.GET:
        sel = request.GET["myinput"]

    if request.method == "GET" and "friendAction" in request.GET:
        if request.GET["friendAction"] != "See Games":
            friend_account = request.GET["friendAction"].split("http://GamerNetLibrary.com/")[1]
            print(make_action)
            if make_action == "Add Friend":
                make_friend(account, friend_account)
                make_friend(friend_account, account)  # friend is mutual
            else:
                print("deleting")
                delete_friend(account, friend_account)
                delete_friend(friend_account, account)

    people = get_no_friends(account)

    if sel == "Friends":
        color_people = "white"
        color_friends = "RoyalBlue"
        make_action = "Delete Friend"

        people = get_friends(account)
    else:
        color_people = "RoyalBlue"
        color_friends = "white"
        make_action = "Add Friend"




    tparams = {
        'xml': "html",
        'sel_date': "sel_date",
        'people': people,
        'color1': color_people,
        'color2': color_friends,
        'makeAction': make_action,
        'loggedAccount': globl_acc
    }

    return render(request, "table.html", tparams)

global globl_acc
globl_acc = "Account1"

def admin(request):
    global globl_acc

    account_list = get_accounts()
    account_list.sort()
    #print(account_list)
    name = ""
    nick = ""
    games_owned = ""
    logo = ""

    if request.method == "POST" and "accountSelect" in request.POST:
        sel_acc = request.POST["accountSelect"]
        globl_acc = sel_acc

    if globl_acc != "Select Account":
        person_info = get_person_info(str(globl_acc))
        name = person_info.pop(0)
        nick = person_info.pop(0)
        logo = person_info.pop(0)
        games_owned = person_info.copy()
    games_owned_info = []
    for game in games_owned:
        game = game.split("http://GamerNetLibrary.com/")[1]
        for attrib in get_game_info(game):
            games_owned_info.append(attrib)


    tparams = {
        'accounts': account_list,
        'default_message': globl_acc,
        'name': name,
        'nick': nick,
        'logo':logo,
        'games': games_owned_info,
        'loggedAccount': globl_acc,
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
    account = globl_acc
    place_message = "Search a game"
    warn_message = ""
    genres_list = get_genres()
    game_list = get_games(account)

    print(game_list)
    #print(genres_list)

    print(request.GET)

    if request.method == "GET" and "buyID" in request.GET:
        game_id = request.GET["buyID"].split("http://GamerNetLibrary.com/")[1]
        buy_game(account, game_id)
        game_list = get_games(account)

    if request.method == "GET" and "genderSelect" in request.GET:
        sel_gen = request.GET["genderSelect"]
        globl_gen =sel_gen
        game_list = get_games_by_genre(str(sel_gen), account)
        print(sel_gen)

    elif request.method == "GET" and "searchGame" in request.GET:
        game_name = request.GET["searchGame"]
        place_message = game_name
        if globl_gen != "Select game gender":
            game_list = search_game(game_name, account, globl_gen)
        else: game_list = search_game(game_name, account )

    else: globl_gen = "Select game gender"

    if len(game_list) == 0:
        globl_gen = "Select game gender"
        warn_message = "Didn't find any results"




    tparams = {
        'default_message': globl_gen,
        'warn_message': warn_message,
        'genres': genres_list,
        'place_message': place_message,
        'loggedAccount': globl_acc,
        'game_properties': game_list
    }
    return render(request, 'news.html', tparams)



