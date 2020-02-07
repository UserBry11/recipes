# Responsible for managing database data to html templates
from django.shortcuts import render, reverse, HttpResponseRedirect
from recipe_box.models import Author, Recipe
from recipe_box.forms import AddRecipe, AddAuthor


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


def add_recipe(request):
    html = "addrecipes.html"

    if request.method == "POST":
        form = AddRecipe(request.POST)
# Data from request.POST is added to TakeData() container.
# Contains everythong POSTed from user
        if form.is_valid():
            data = form.cleaned_data
            # Cleans up unecesssary data from form
            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions']
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipe()

    return render(request, html, {'formKey': form})


def add_author(request):
    html = 'addauthors.html'

    if request.method == 'POST':
        form = AddAuthor(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthor()

    return render(request, html, {'formKey': form})





















