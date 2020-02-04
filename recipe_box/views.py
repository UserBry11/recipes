# Responsible for managing database data to html templates
from django.shortcuts import render
from recipe_box.models import Author, Recipe


def index(request):
    items = Recipe.objects.all()

    return render(request, 'index.html', {'recipes': items})
# author, author_id, description, id, instructions, time_required, title


def details(request, id):
    item = Recipe.objects.get(id=id)

    return render(request, 'details.html', {'item': item})


def auth_deets(request, description):
    item = Recipe.objects.get(description=description)
    return render(request, 'author.html', {'tree': "item"})
