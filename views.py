from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Task
from .forms import TaskForm


def index(request):
    tasks = Task.objects.all()
    todo = [t for t in tasks if t.started_at is None]
    in_progress = [t for t in tasks if t.started_at is not None and t.completed_at is None]
    completed = [t for t in tasks if t.completed_at is not None]

    context = {
        'todo': todo,
        'in_progress': in_progress,
        'completed': completed
    }

    return render(request, 'mainstay_kanban/index.html', context)


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added')
            return redirect('mainstay_kanban:index')
        else:
            messages.error(request, 'Errors')
    else:
        form = TaskForm()

    return render(request, 'mainstay_kanban/add.html', {'form': form})    


def edit_task(request, task_id):
    task_ = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task_)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task editted')
            return redirect('mainstay_kanban:index')
        else:
            messages.error(request, 'Errors')
    else:
        form = TaskForm(instance=task_)

    return render(request, 'mainstay_kanban/edit.html', {'form': form})

def start_task(request, task_id):
    task_ = get_object_or_404(Task, id=task_id)
    task_.started_at = datetime.today()
    task_.save()
    messages.success(request, 'Task marked as started')
    return redirect('mainstay_kanban:index')


def complete_task(request, task_id):
    task_ = get_object_or_404(Task, id=task_id)
    task_.completed_at = datetime.today()
    task_.save()
    messages.success(request, 'Task marked as completed')
    return redirect('mainstay_kanban:index')
