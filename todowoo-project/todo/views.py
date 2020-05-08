from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo


def index(request):
    return render(request, 'todo/index.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {
            'form': UserCreationForm(),
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already taken. Please use other username!',
                })

        else:
            # Passwords did not match!
            return render(request, 'todo/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'Passwords did not match!',
            })


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {
            'form': AuthenticationForm(),
        })
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(request, 'todo/loginuser.html', {
                'form': AuthenticationForm(),
                'error': 'Username or Password did not match',
            })


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {
            'form': TodoForm(),
        })
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {
                'form': TodoForm(),
                'error': 'Bad data input. Try again.'
            })


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user)

    return render(request, 'todo/currenttodos.html', {'todos': todos})
