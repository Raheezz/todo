from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

from django.contrib.auth import views as register_views
from .views import login_user

router = DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('complete/<int:todo_id>/', views.complete_todo, name='complete_todo'),
    path('undo_complete/<int:todo_id>/', views.undo_complete_todo, name='undo_complete_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('api/', include(router.urls)),
    path('login/', register_views.LoginView.as_view(), name='login'),
    path('logout/', register_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', login_user, name='login'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    
]



