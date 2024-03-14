from .models import Task
from .forms import PositionForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class UserLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    
class UserRegister(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super(UserRegister, self).dispatch(*args, **kwargs)
    

class ToDoList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'app/task_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_query = self.request.GET.get('search-area') or ''
        if search_query:
            context['tasks'] = context['tasks'].filter(title__startswith=search_query)
        
        context['search_query'] = search_query
        return context
    
    
class ToDoDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'app/task.html'
    

class ToDoCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'app/task_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ToDoCreate, self).form_valid(form)
    
    
class ToDoUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    template_name = 'app/task_update.html'


class ToDoDelete(LoginRequiredMixin, DeleteView):
    model  = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'app/task_delete.html'
    

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))