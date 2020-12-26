import os
import io
from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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

def news(request):
    return render(request, 'news.html')



