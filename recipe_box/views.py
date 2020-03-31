from django.shortcuts import render, reverse, HttpResponseRedirect
from recipe_box.models import Author, Recipe
from recipe_box.forms import AddRecipe, AddAuthor, SignupForm, LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


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


@login_required()
def add_recipe(request):
    html = "addrecipes.html"

    if request.user.is_staff:
        try:
            Author.objects.get(name=request.user)
        except Author.DoesNotExist:
            Author.objects.create(
                name=request.user,
                bio='',
                user=request.user
            )

    if request.method == "POST":
        form = AddRecipe(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if request.user.is_staff:
                author_user = Author.objects.get(user__username=data['author'])
                # obj, created = Author.objects.get_or_create(
                #     name=data['author'],
                #     user=request.user,
            #         defaults={'birthday': date(1940, 10, 9)},
                # )
            else:
                author_user = Author.objects.get(user=request.user)

            Recipe.objects.create(
                title=data['title'],
                author=author_user,
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions']
            )

            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipe()

    return render(request, html, {'formKey': form})


@staff_member_required()
def signup_view(request):
    html = "signup.html"

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'],
            )

            # login(request, user)
            Author.objects.create(
                name=data['username'],
                user=user
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, html, {'form': form})


def login_view(request):
    html = "login.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
                )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, html, {
        'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


@staff_member_required()
def add_author(request):
    html = 'addauthors.html'

    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['username'],
                bio=data['bio'],
                user=data['user']
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthor()

    return render(request, html, {'formKey': form})
