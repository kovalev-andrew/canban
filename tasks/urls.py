from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.kanban_board, name='kanban_board'),
    path('create/', views.create_task, name='create_task'),
    path('<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/update/', views.update_task, name='update_task'),
    path('<int:task_id>/delete/', views.delete_task, name='delete_task'),
]

