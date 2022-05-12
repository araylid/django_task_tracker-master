import datetime

from django.shortcuts import render, redirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from catalog.models import User, Task, Project, Description
from catalog.forms import CreateNewTaskForm, CreateNewDescriptionForm, \
    UpdateTaskForm, FilterTaskForm, AuthUserForm, RegisterUserForm
from catalog.serializers import UserSerializer, ProjectSerializer, \
    TaskSerializer, DescriptionSerializer

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import HttpResponseRedirect

from datetime import date

print(date.today())


# API
RESPONSE_NOT_ALLOWED = HttpResponseNotAllowed(['POST', 'GET'])



class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TasksList(generics.ListCreateAPIView):
    model = Task
    queryset = Task.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('project', 'author', 'status', 'worker', 'added_at')
    serializer_class = TaskSerializer
    search_fields = ('purpose', 'status')


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DescriptionList(generics.ListCreateAPIView):
    model = Description
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        task_pk = self.kwargs['pk']
        task = Task.objects.get(id=task_pk)
        queryset = Description.objects.filter(task=task).all()
        return queryset


class DescriptionDetail(generics.RetrieveAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer



class DescriptionStatistics(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        task_pk = self.kwargs['pk']
        task = Task.objects.get(id=task_pk)
        stat = statistics_dump(Description.objects.filter(task=task).all())
        return Response(stat)


# RENDERING IN TEMPLATES


# def create_task(request):
#     if request.method == 'GET':
#         form = CreateNewTaskForm()
#         return render(request, 'create_task_form.html', {'form': form})
#     elif request.method == 'POST':
#         form = CreateNewTaskForm(request.POST)
#         if form.is_valid():
#             response = form.save()
#             response.author = User.objects.get(username=request.user)
#             response.save()
#         return redirect('root')
#     return HttpResponseNotAllowed(['POST', 'GET'])

class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Task
    template_name = 'create_task_form.html'
    form_class = CreateNewTaskForm
    success_url = reverse_lazy('root')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


# class Create_task(CreateView):
# model = Task
# template_name = 'create_task_form.html'
# form_class = CreateNewTaskForm
# success_url = reverse_lazy('create_task')
#
# def form_valid(self, form):
#     self.object = form.save(commit=False)
#     self.object.author = self.request.user
#     self.object.save()
#     return super(Create_task, self).form_valid(form)
# self.object = form.save(commit=False)
# self.object.author = self.request.user
# self.object.save()
# return super().form_valid(form)


# def delete_task(request, pk):
#     if request.method == 'DELETE' or request.method == 'POST':
#         task = get_object_or_404(Task, id=pk)
#         task.delete()
#         return redirect('root')
#     return HttpResponseNotAllowed(['POST'])


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_deleted.html'
    success_url = reverse_lazy('root')

    def post(self, request, *args, **kwargs):
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


# def update_task(request, pk):
#     if request.method == 'GET':
#         form = UpdateTaskForm()
#         return render(request, 'update_task_form.html', {'form': form})
#     elif request.method == 'POST':
#         form = UpdateTaskForm(request.POST)
#         task = Task.objects.get(id=pk)
#         if form.is_valid():
#             new_status = form.cleaned_data['status']
#             new_worker = form.cleaned_data['worker']
#             task.status = new_status
#             task.worker = new_worker
#             task.save()
#         return redirect('task-detail', pk=pk)
#     else:
#         return HttpResponseNotAllowed(['POST', 'GET'])

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'update_task_form.html'
    form_class = UpdateTaskForm
    success_url = reverse_lazy('root')

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


def create_description(request, pk):
    if request.method == 'GET':
        form = CreateNewDescriptionForm()
        return render(request, 'create_description_form.html', {'form': form})
    elif request.method == 'POST':
        form = CreateNewDescriptionForm(request.POST)
        task = Task.objects.get(id=pk)
        if form.is_valid():
            new_desc = form.cleaned_data['description']
            author = request.user
            # author = form.cleaned_data['author']
            description = Description(description=new_desc, author=author,
                                      task=task)
            description.save()
        return redirect(task.get_absolute_url())
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


def tasks_list(request):
    # if request.method == 'GET':
    #     tasks = Task.objects.all()
    #     form = FilterTaskForm(request.GET)
    #     if form.is_valid():
    #         tasks = tasks_filter(project=form.cleaned_data['project'],
    #                              author=form.cleaned_data['author'],
    #                              worker=form.cleaned_data['worker'],
    #                              status=form.cleaned_data['status'],
    #                              search_text=form.cleaned_data['search_text'])
    #     return render(request, 'catalog/tasks_list.html',
    #                   {'tasks_list': tasks, 'form': form})
    # return HttpResponseNotAllowed(['GET'])

    if request.method == 'GET':
        if request.user.is_authenticated:
            form = FilterTaskForm(request.GET)
            if form.is_valid():
                tasks = tasks_filter(project=form.cleaned_data['project'], status=form.cleaned_data['status'], search_text=form.cleaned_data['search_text'], author=request.user)
                tasks1 = tasks_filter(project=form.cleaned_data['project'], status=form.cleaned_data['status'], search_text=form.cleaned_data['search_text'], worker=request.user)
                tasks2 = tasks_filter(project=form.cleaned_data['project'], status='In progress', search_text=form.cleaned_data['search_text'], worker=request.user)

            return render(request, 'catalog/tasks_list.html', {'tasks_list': tasks, 'tasks_list1': tasks1, 'tasks_list2': tasks2, 'form': form})
        else:
            return redirect('login_page')
    elif request.method == 'POST':
        form = FilterTaskForm(request.POST)
        if form.is_valid():
            tasks = tasks_filter(project=form.cleaned_data['project'],
                                         status=form.cleaned_data['status'],
                                         search_text=form.cleaned_data['search_text'], worker=form.cleaned_data['worker'], author=form.cleaned_data['author'])
            return render(request, 'catalog/tasks_list.html',
                              {'tasks_list': tasks, 'form': form})
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


class TaskDetailView(generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task_descriptions = Description.objects.filter(
            task__id=self.kwargs['pk'])
        context['all_descriptions'] = task_descriptions
        statistics = statistics_dump(task_descriptions)
        context['statistics'] = statistics
        return context



def tasks_filter(**kwargs):
    tasks = Task.objects.all()
    if kwargs.get('project'):
        tasks = tasks.filter(project=kwargs.get('project'))
    if kwargs.get('author'):
        tasks = tasks.filter(author=kwargs.get('author'))
    if kwargs.get('worker'):
        tasks = tasks.filter(worker=kwargs.get('worker'))
    if kwargs.get('status'):
        tasks = tasks.filter(status=kwargs.get('status'))
    if kwargs.get('search_text'):
        tasks = tasks.filter(purpose__icontains=kwargs.get('search_text'))
    return tasks


# This feature makes description statistics.
# Returns the dictionary, where the key is the date,
#   the value is a list with the numbers of various descriptions and authors.
def statistics_dump(descriptions):
    statistic = {}
    for description in descriptions:
        date = description.added_at.date().strftime("%Y-%m-%d")
        if date in statistic:
            statistic[date]['diff_descriptions'] += 1
            statistic[date]['diff_authors'].append(description.author)
        else:
            statistic[date] = {'diff_descriptions': 1, 'diff_authors': [description.author]}
    # for date in statistic:
    #     statistic[date]['diff_authors'] = len(set(statistic[date]['diff_authors']))
    for date in statistic:
        statistic[date]['diff_authors'] = description.author
    return statistic


class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('root')

    def get_success_url(self):
        return self.success_url


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('root')


class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('root')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid

