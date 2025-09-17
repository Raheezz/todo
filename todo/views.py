from django.shortcuts import render,redirect,get_object_or_404
from .models import Todo


from django.contrib.auth.decorators import login_required
from .forms import TodoForm



# Create your views here.

def home(request):
    todos = Todo.objects.all().order_by('-created_at')  # fetch all todo items
    return render(request, 'todo/index.html', {'todos': todos})

from django.shortcuts import render
@login_required
def todo_list(request):
    upcoming_todos = Todo.objects.filter(is_completed=False).order_by('-created_at')
    completed_todos = Todo.objects.filter(is_completed=True).order_by('-updated_at')
    
    context = {
        'upcoming_todos': upcoming_todos,
        'completed_todos': completed_todos,
    }
    return render(request, 'todo_list.html', context)


def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Todo.objects.create(title=title, description=description)
    return redirect('todo_list')

def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_completed = True
    todo.save()
    return redirect('todo_list')

def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect('todo_list')

def undo_complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_completed = False
    todo.save()
    return redirect('todo_list')
def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.save()
    return redirect('todo_list')



from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user  # 👈 assign the logged-in user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/create.html', {'form': form})


from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm

def register(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('todo_list')

        elif action == 'register':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('todo_list')
            else:
                print(register_form.errors)  # ✅ log errors to console (PythonAnywhere error log)

    return render(request, 'register.html', {
        'login_form': login_form,
        'register_form': register_form,
    })




from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# views.py
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')                              
    user = authenticate(username=username, password=password)

    if user is not None:
        return JsonResponse({'message': 'Login successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

