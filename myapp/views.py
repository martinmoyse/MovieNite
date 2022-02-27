from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, List, ListedShow

import uuid

# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(redirect_field_name='', login_url='login')
def mylists_view(request):
    if request.method == "GET":
        current_user = request.user
        listOfCurrentUser = List.objects.filter(author=current_user)
        allShowsOnCurrentList = ListedShow.objects.all().filter(listOwner=listOfCurrentUser[0].id)

        # Creates a user list if one doesn't already exist.
        if(len(listOfCurrentUser) == 0):
            generateUniqueID = str(uuid.uuid4())
            uniqueID = generateUniqueID[0:6]
            newList = List(author=current_user, listId=uniqueID)
            newList.save()
            listOfCurrentUser = List.objects.filter(author=current_user)
        context = {
                'list': listOfCurrentUser[0],
                'shows': allShowsOnCurrentList,
                'message': '',
            }
        return render(request, "mylist.html", context)

@login_required(redirect_field_name='', login_url='login')
def explore_view(request):
    current_user = request.user
    listOfCurrentUser = List.objects.filter(author=current_user)
    if request.method == "GET":
        # Creates a user list if one doesn't already exist.
        if(len(listOfCurrentUser) == 0):
            generateUniqueID = str(uuid.uuid4())
            uniqueID = generateUniqueID[0:6]
            newList = List(author=current_user, listId=uniqueID)
            newList.save()
            listOfCurrentUser = List.objects.filter(author=current_user)
        context={
            'list': listOfCurrentUser[0]
        }
        return render(request, "explore.html", context)
    
    if request.method == "POST":
        tt = request.POST.getlist('id')
        t = request.POST.getlist('title')
        rt = request.POST.getlist('rating')
        y = request.POST.getlist('year')
        im = request.POST.getlist('image')
        i = request.POST.getlist('index')
        c = request.POST.getlist('category')
        li = request.POST.getlist('listid')
        
        
       
        newListedShow = ListedShow(
            userOwner = User.objects.get(pk=current_user.id),
            listOwner = List.objects.get(listId=li[0]),
            imdbId = tt[0],
            title = t[0],
            imdbRating = rt[0],
            year = y[0],
            image = im[0]
        )
        current_list = List.objects.get(listId=li[0])
        allShowsOnCurrentList = ListedShow.objects.all().filter(listOwner=current_list)
        notInList = True
        for show in allShowsOnCurrentList:
            if(show.imdbId == tt[0]):
                notInList = False
        if(notInList):
            newListedShow.save()
            message = 'Show added to your list successfully.'
        else:
            message = 'This show is already in your list.'
        context = {
            'category': c[0],
            'index': i[0],
            'message': message,
            'list': listOfCurrentUser[0]
        }
        return render(request, "explore.html", context)

def delete_from_list(request):
    if request.method == "POST":
        current_user = request.user
        
        show_id = request.POST["show_to_delete"]
        toDelete = ListedShow.objects.filter(pk=show_id).delete()

        listOfCurrentUser = List.objects.filter(author=current_user)
        allShowsOnCurrentList = ListedShow.objects.all().filter(listOwner=listOfCurrentUser[0].id)
        context = {
            'list': listOfCurrentUser[0],
            'shows': allShowsOnCurrentList,
            'message': 'Show deleted.'
        }
        return render(request, "mylist.html", context)

@login_required(redirect_field_name='', login_url='login')
def match_view(request):
    if request.method == "GET":
        return render(request, "match.html")

    else:
        current_user = request.user
        list1 = List.objects.filter(author=current_user)
        list1_id = list1[0].id
        list1_shows = ListedShow.objects.all().filter(listOwner=list1_id)

        list2_id = request.POST["list-code"]
        list2 = List.objects.filter(listId=list2_id)
        if(not list2.exists()):
            context = {
            'message': 'List does not exist.'
            }
            return render(request, "match.html", context)
        list2_shows = ListedShow.objects.all().filter(listOwner=list2[0].id)
            
        matches = ListedShow.objects.none()
        message = ''

        for show_list1 in list1_shows:
            for show_list2 in list2_shows:
                if (show_list1.imdbId ==  show_list2.imdbId):
                    matches |= ListedShow.objects.filter(pk=show_list1.id)

        if not matches:
            message = 'No matches found.'
        context = {
            'matches': matches,
            'message': message
        }
        return render(request, "match.html", context)

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        #Ensure password matches confirmation
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        
        #Attempt to create new user
        try:
            user = User.objects.create_user(username,'', password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("explore"))

    else:
        return render(request, "register.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("explore"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
