from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import Student
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpRequest
from .MathBackend import Task


def index_view(request):
    request.POST = []
    return render(request, 'StudentSite/index.html')


def test_view(request):
    user = request.user
    task = Student.objects.get(user=user).studenttaskrel_set.get(isTestTask=True)
    task_obj = Task.from_string(task.task.str_repr)
    print(task_obj)
    return render(request, 'StudentSite/test_base.html', {'task': task_obj})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('student_site:index_view'))


def login_view(request):
    print(request.POST)
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            print(user)
    return HttpResponseRedirect(reverse('student_site:index_view'))