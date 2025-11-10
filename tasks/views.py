from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task


@login_required
def kanban_board(request):
    """Display the kanban board with all tasks organized by status"""
    # Filter tasks by current user
    tasks = Task.objects.filter(user=request.user)
    
    # Organize tasks by status
    tasks_by_status = {
        'todo': tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'done': tasks.filter(status='done'),
    }
    
    return render(request, 'tasks/kanban_board.html', {
        'tasks_by_status': tasks_by_status,
        'today': timezone.now().date(),
        'user': request.user
    })


@require_http_methods(["POST"])
@login_required
def create_task(request):
    """Create a new task"""
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    status = request.POST.get('status', 'todo')
    priority = request.POST.get('priority', 'medium')
    due_date = request.POST.get('due_date') or None
    
    if title:
        task = Task.objects.create(
            user=request.user,  # Assign task to current user
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date
        )
        # Always return JSON for AJAX requests
        return JsonResponse({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'due_date': str(task.due_date) if task.due_date else None,
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Title is required'}, status=400)


@require_http_methods(["POST"])
@login_required
def update_task_status(request, task_id):
    """Update task status (for drag and drop)"""
    # Only allow updating own tasks
    task = get_object_or_404(Task, id=task_id, user=request.user)
    new_status = request.POST.get('status')
    
    if new_status in dict(Task.STATUS_CHOICES).keys():
        task.status = new_status
        task.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid status'})


@require_http_methods(["POST"])
@login_required
def delete_task(request, task_id):
    """Delete a task"""
    # Only allow deleting own tasks
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({'success': True})
    return redirect('kanban_board')


@require_http_methods(["POST"])
@login_required
def update_task(request, task_id):
    """Update task details"""
    # Only allow updating own tasks
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    task.title = request.POST.get('title', task.title).strip()
    task.description = request.POST.get('description', task.description).strip()
    task.priority = request.POST.get('priority', task.priority)
    task.due_date = request.POST.get('due_date') or None
    
    if task.title:
        task.save()
        # Always return JSON for AJAX requests
        return JsonResponse({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'due_date': str(task.due_date) if task.due_date else None,
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Title is required'}, status=400)

