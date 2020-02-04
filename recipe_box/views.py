# Responsible for managing database data to html templates
from django.shortcuts import render
from recipe_box.models import Author, Recipe


def index(request):
    items = Recipe.objects.all()

    return render(request, 'index.html', {'recipes': items})
# author, author_id, description, id, instructions, time_required, title


def details(request, id):
    item = Recipe.objects.get(id=id)

    return render(request, 'recipe_details.html', {'item': item})

# integer or instance itself. Need pass someth;ing useful
# foreign key pointing to anothre model. Use __method


def auth_deets(request, name):
    item = Recipe.objects.filter(author__name=name)
    return render(request, 'author.html',
                  {
                    'authDeets': item,
                    'authName': name
                  })
