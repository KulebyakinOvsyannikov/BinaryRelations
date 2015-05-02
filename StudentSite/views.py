from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import StudentModel, TaskModel, StudentTaskRel
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .MathBackend import Task
from django.views.decorators.http import require_POST
from .MathBackend.OrderType import OrderType
import datetime


def index(request):
    """
    'next' may be passed because of attempt to open test_view while not being logged in
    in this case we set context variable which will be included in login form
    :return: Rendered response for index page.
    """
    context = {}
    if 'next' in request.GET:
        context['next'] = request.GET['next']
    return render(request, 'StudentSite/index.html', context)


@require_POST
def control_check(request):
    """
    :return: rendered response for users attempt to solve test task
    """
    task_id = request.POST['task_id']
    task = TaskModel.objects.get(pk=task_id)
    task_obj = Task.from_string(task.str_repr)

    users_solve = compose_partial_solve(request.POST, len(task_obj.elements))
    rel = StudentTaskRel.objects.get(task=task, student=StudentModel.objects.get(user=request.user))
    rel.partial_solve = users_solve
    rel.save()

    if task.answer_table is None or task.answer_properties is None:
        task.answer_table = task_obj.solve_string()
        task.answer_properties = task_obj.solve_properties()
        task.save()

    result = users_solve == '@'.join([task.answer_table, task.answer_properties])

    if result:
        rel.table_and_props_completed = True
    else:
        rel.numberOfAttempts += 1
    rel.save()

    response = render(request, 'StudentSite/test_base.html', {'task': task_obj,
                                                              'task_id': task_id,
                                                              'result': result})
    response.set_cookie('partial_solve', users_solve)
    response.delete_cookie('correct_solve_table')
    response.delete_cookie('correct_solve_props')
    return response


def logout_action(request):
    logout(request)
    return HttpResponseRedirect(reverse('student_site:index'))


def login_action(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
    if 'next' in request.POST:
        print(request.POST['next'])
        return HttpResponseRedirect(request.POST['next'])
    return HttpResponseRedirect(reverse('student_site:index'))


def registration(request):
    return render(request, 'StudentSite/registration.html')


def login_registration(request):
    return render(request, 'StudentSite/login_registration.html')


@require_POST
def registration_action(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    group = request.POST['group']
    web_site = request.POST['web_site']

    User.objects.create_user(username=username, password=password)
    user = authenticate(username=username, password=password)
    student = StudentModel.objects.create(user=user, website=web_site)
    student.first_name = first_name
    student.last_name = last_name
    student.group = group
    student.save()

    login(request, user)

    return HttpResponseRedirect(reverse('student_site:index'))


def demo(request):
    pass


@login_required(login_url="student_site:login_registration")
def training(request):
    return render(request, 'StudentSite/training.html')


@login_required(login_url="student_site:login_registration")
def control(request):
    user = request.user
    student = user.studentmodel
    control_task = student.studenttaskrel_set.filter(isTestTask=True, isCompleted=False)

    if len(control_task) == 0:
        task = TaskModel.get_control_task()
        task_obj = Task.from_string(task.str_repr)
        control_task = StudentTaskRel(task=task, student=student, isTestTask=True, dateStarted=datetime.date.today())
        control_task.save()
    else:
        control_task = control_task[0]
        task_obj = Task.from_string(control_task.task.str_repr)

    response = render(request, 'StudentSite/test_base.html', {'task': task_obj,
                                                              'task_id': control_task.task_id})
    response.set_cookie('partial_solve', control_task.partial_solve)
    response.delete_cookie('correct_solve_table')
    response.delete_cookie('correct_solve_props')
    return response


def training_with_difficulty(request, difficulty):
    user = request.user
    student = user.studentmodel
    tr_task = student.studenttaskrel_set.filter(isTestTask=False, isCompleted=False)

    if len(tr_task) == 0:
        task = TaskModel.get_training_task_with_difficulty(difficulty)
        task_obj = Task.from_string(task.str_repr)
        tr_task = StudentTaskRel(task=task, student=student, isTestTask=False, dateStarted=datetime.date.today())
        tr_task.save()
    else:
        tr_task = tr_task[0]
        task_obj = Task.from_string(tr_task.task.str_repr)

    response = render(request, 'StudentSite/train_base.html', {'task': task_obj,
                                                               'task_id': tr_task.task_id})
    response.set_cookie('partial_solve', tr_task.partial_solve)
    return response


def check_training(request):
    """
    :return: rendered response for users attempt to solve test task
    """
    task_id = request.POST['task_id']
    task = TaskModel.objects.get(pk=task_id)
    task_obj = Task.from_string(task.str_repr)

    users_solve = compose_partial_solve(request.POST, len(task_obj.elements))

    rel = StudentTaskRel.objects.get(task=task, student=StudentModel.objects.get(user=request.user))
    rel.partial_solve = users_solve
    rel.save()

    if task.answer_table is None or task.answer_properties is None:
        task.answer_table = task_obj.solve_string()
        task.answer_properties = task.solve_properties()
        task.save()

    result = users_solve == '@'.join([task.answer_table, task.answer_properties])

    if result:
        rel.table_and_props_completed = True
    else:
        rel.numberOfAttempts += 1
    rel.save()

    response = render(request, 'StudentSite/train_base.html', {'task': task_obj,
                                                               'task_id': task_id,
                                                               'result': result})
    response.set_cookie('partial_solve', users_solve)
    response.set_cookie('correct_solve_table', task.answer_table)
    response.set_cookie('correct_solve_props', task.answer_properties)
    return response


def compose_partial_solve(requests_POST, num_of_elements):
    res_table = ""
    for i in range(0, num_of_elements):
        for j in range(0, num_of_elements):
            res_table += '+ ' if "%s-%s" % (i,j) in requests_POST else '- '
        res_table = res_table[:-1] + '$'
    res_table = res_table[:-1]

    property_fields = ["reflexivity",
                       "anti-reflexivity",
                       "symmetry",
                       "asymmetry",
                       "antisymmetry",
                       "transitivity",
                       "equivalency",
                       "order",
                       "order-strict",
                       "order-linearity"]
    res_props = ""
    for field in property_fields:
        res_props += field + '=' + (requests_POST[field] if field in requests_POST else 'none') + '$'
    return '@'.join([res_table, res_props[:-1]])


def warshalls(request):
    pass
