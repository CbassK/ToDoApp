from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', ToDoList.as_view(), name='tasks'),
    path('task/<int:pk>/', ToDoDetail.as_view(), name='task'),
    path('create/', ToDoCreate.as_view(), name='task-create'),
    path('update/<int:pk>', ToDoUpdate.as_view(), name='task-update'),
    path('delete/<int:pk>', ToDoDelete.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]

