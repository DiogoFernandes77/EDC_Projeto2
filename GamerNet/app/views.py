import os
import io
from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
#from queries import *
from django.urls import reverse

from app.queries import *
from app.queries_dbpedia import *

global prev_id
prev_id = 0

def index(request):
    search_input = "Search something"
    info = " "
    if request.method == "GET" and "searchDBpedia" in request.GET:
        search_input = request.GET["searchDBpedia"]

        print(search_input)

    if search_input != "Search something":
        info = dbpedia_get_decription(search_input)
        if len(info) == 0:
            info = "Nothing was found"
        else:
            info = info[0]



    tparams = {
        'search_input': search_input,
        'searched': search_input,
        'info': info,

    }

    return render(request, 'index.html', tparams)

color_people = "RoyalBlue"
color_friends = "white"
make_action = "Add Friend"
sel = "Make Friend"
def social(request):
    account = globl_acc


    global color_people
    global color_friends
    global color_suggested
    global make_action
    global sel
    if request.method == "GET" and "myinput" in request.GET:
        sel = request.GET["myinput"]

    if request.method == "GET" and "friendAction" in request.GET:
        action = request.GET["friendAction"].split("see")

        print("action")
        print(action)
        if len(action) == 1:
            friend_account = request.GET["friendAction"].split("http://GamerNetLibrary.com/")[1]
            #print(make_action)
            if make_action == "Add Friend":
                make_friend(account, friend_account)
                make_friend(friend_account, account)  # friend is mutual
            else:
                #print("deleting")
                delete_friend(account, friend_account)
                delete_friend(friend_account, account)

        else:
            id2_account = request.GET["friendAction"].split("see")[1]
            user2_account = id2_account.split("http://GamerNetLibrary.com/")[1]

            person_info = get_person_info(user2_account)
            name = person_info.pop(0)
            nick = person_info.pop(0)
            logo = person_info.pop(0)
            games_owned = person_info.copy()
            games_owned_info = []

            common_games= get_common_games(account,user2_account)
            common_games_info = []
            for game in common_games:
                game = game.split("http://GamerNetLibrary.com/")[1]
                for attrib in get_game_info(game):
                    common_games_info.append(attrib)

            print("Common Games")
            print(common_games_info)

            for game in games_owned:
                game = game.split("http://GamerNetLibrary.com/")[1]
                for attrib in get_game_info(game):
                    games_owned_info.append(attrib)

            tparams = {
                'name': name,
                'nick': nick,
                'logo':logo,
                'games': games_owned_info,
                'commonGames': common_games_info,
                'commonFriends': get_common_friends(account,user2_account),
                'loggedAccount': globl_acc,
                'error' : "error"
                }

            return render(request, 'profile.html', tparams)

    people = get_no_friends(account)

    if sel == "Friends":
        color_people = "white"
        color_suggested = "White"
        color_friends = "RoyalBlue"

        make_action = "Delete Friend"

        people = get_friends(account)
    elif sel == "Sugggested":

        color_people = "white"
        color_suggested = "RoyalBlue"
        color_friends = "White"
        make_action = "Add Friend"

        people = get_recommended_friends(account)
    else:
        color_people = "RoyalBlue"
        color_suggested = "White"
        color_friends = "white"
        make_action = "Add Friend"

    tparams = {
        'xml': "html",
        'sel_date': "sel_date",
        'people': people,
        'color1': color_people,
        'color2': color_friends,
        'color3': color_suggested,
        'makeAction': make_action,
        'loggedAccount': globl_acc
    }

    return render(request, "datasocial.html", tparams)


global globl_acc
globl_acc = "Account1"

def myaccount(request):
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
    return render(request,'myaccount.html', tparams)



global globl_gen
globl_gen = "Select game gender"

def store(request):
    global globl_gen
    account = globl_acc
    place_message = "Search a game"
    warn_message = ""
    genres_list = get_genres()
    game_list = get_games(account)


    if request.method == "GET" and "buyID" in request.GET:
        game_id = request.GET["buyID"].split("http://GamerNetLibrary.com/")[1]
        buy_game(account, game_id)
        game_list = get_games(account)

    if request.method == "GET" and "genderSelect" in request.GET:
        sel_gen = request.GET["genderSelect"]
        globl_gen =sel_gen
        game_list = get_games_by_genre(str(sel_gen), account)
        #print(sel_gen)

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
    return render(request, 'shop.html', tparams)



