from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django import forms
from django.forms import ValidationError

from .models import User, Course
from .filters import CourseFilter
# Create your views here.


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "data/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "data/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "data/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "data/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "data/register.html")


def index(request):
    if request.method == "GET":
        try:
            courses = CourseFilter(request.GET, queryset=Course.objects.all())
        except Course.DoesNotExist:
            return render(request, 'data/index.html', {
                "message": "does not exist",
            })

        return render(request, 'data/index.html', {
            "filter": courses,
        })

    if request.method == "POST":
        title = request.POST["title"]

        try:
            course = Course.objects.create(title=title)
        except Course.DoesNotExist:
            return render(request, 'data/index.html', {
                "message": "does not exist",
            })


def division(request):
    pass


def student(request):
    pass
