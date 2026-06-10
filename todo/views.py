from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Task


# 🔐 LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'todo/login.html', {'error': 'Invalid credentials'})

    return render(request, 'todo/login.html')


# 📝 REGISTER
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'todo/register.html', {'error': 'User already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'todo/register.html')


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 🏠 HOME
@login_required
def home(request):
    query = request.GET.get('q')
    filter_type = request.GET.get('filter')
    priority = request.GET.get('priority')   # ⭐ NEW

    # ➕ ADD TASK
    if request.method == 'POST':
        title = request.POST.get('title')
        pr = request.POST.get('priority')

        if title and title.strip():
            Task.objects.create(
                title=title,
                priority=pr,
                user=request.user
            )

        return redirect('home')

    # 📋 USER TASKS
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    # 🔍 SEARCH
    if query:
        tasks = tasks.filter(title__icontains=query)

    # 🎯 STATUS FILTER
    if filter_type == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_type == 'pending':
        tasks = tasks.filter(completed=False)

    # ⭐ PRIORITY FILTER
    if priority == 'H':
        tasks = tasks.filter(priority='H')
    elif priority == 'M':
        tasks = tasks.filter(priority='M')
    elif priority == 'L':
        tasks = tasks.filter(priority='L')

    return render(request, 'todo/home.html', {'tasks': tasks})


# ❌ DELETE
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('home')


# ✔️ COMPLETE
def complete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('home')


# ✏️ EDIT
def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')

        if title and title.strip():
            task.title = title
            task.priority = priority
            task.save()

        return redirect('home')

    return render(request, 'todo/edit.html', {'task': task})