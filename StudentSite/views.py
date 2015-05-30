from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import StudentModel, TaskModel, StudentTaskRel
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .MathBackend import Task
from .MathBackend.supporting_functions import compose_partial_solve
from django.views.decorators.http import require_POST
from django.core import serializers
from .MathBackend.OrderType import OrderType
from django.utils import timezone
import json


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
    print(request.path)
    users = User.objects.filter(username=username)
    if len(users) != 0:
        return render(request, 'StudentSite/registration.html', {'used_name': True})

    User.objects.create_user(username=username, password=password)
    user = authenticate(username=username, password=password)
    student = StudentModel.objects.create(user=user, website=web_site)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    student.group = group
    student.save()

    login(request, user)

    if 'next' in request.POST:
        print(request.POST['next'])
        return HttpResponseRedirect(request.POST['next'])

    return HttpResponseRedirect(reverse('student_site:index'))


def demo(request):
    task = TaskModel.get_demo_task()
    task_obj = Task.from_string(task.str_repr)

    if task.answer_table is None or task.answer_properties is None:
        task.answer_table = task_obj.solve_string()
        task.answer_properties = task_obj.solve_properties()
        task.answer_warshalls = task_obj.generate_warshalls_answers_string()
        task.save()

    tips = task_obj.generate_demo_strings()
    json_data = json.dumps({'elements': task_obj.elements,
                            'tips': tips[0],
                            'tips_highlights': tips[1],
                            'table_answers': task.answer_table,
                            'props_answers': task.answer_properties,
                            'warshalls_answers': task.answer_warshalls,
                            'topological_answers': task_obj.topological_sort()})

    response = render(request, 'StudentSite/demo.html', {'task': task_obj,
                                                         'json_data': json_data})

    return response


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
        control_task = StudentTaskRel(task=task, student=student, isTestTask=True, dateStarted=timezone.now())
        control_task.save()
    else:
        control_task = control_task[0]
        task_obj = Task.from_string(control_task.task.str_repr)

    context = {'task': task_obj, 'task_id': control_task.task_id}
    if control_task.table_and_props_completed:
        context['result'] = True

    response = render(request, 'StudentSite/test_base.html', context)
    response.set_cookie('partial_solve', control_task.partial_solve)
    response.delete_cookie('correct_solve_table')
    response.delete_cookie('correct_solve_props')
    return response


def training_with_difficulty(request, difficulty):
    user = request.user
    student = user.studentmodel
    diff = {'easy': 1, 'medium': 2, 'hard': 3}
    tr_task = student.studenttaskrel_set.filter(isTestTask=False, isCompleted=False, task__difficulty=diff[difficulty])

    if len(tr_task) == 0:
        task = TaskModel.get_training_task_with_difficulty(difficulty)
        task_obj = Task.from_string(task.str_repr)
        tr_task = StudentTaskRel(task=task, student=student, isTestTask=False, dateStarted=timezone.now())
        tr_task.save()
    else:
        tr_task = tr_task[0]
        task_obj = Task.from_string(tr_task.task.str_repr)

    context = {'task': task_obj, 'task_id': tr_task.id}
    if tr_task.table_and_props_completed:
        context['result'] = True
    else:
        tr_task.numberOfAttempts += 1
    tr_task.save()

    context['json_table_solve'] = json.dumps(tr_task.partial_solve)
    print(context['json_table_solve'])

    response = render(request, 'StudentSite/train_base.html', context)

    return response


def check_training(request):
    """
    :return: rendered response for users attempt to solve test task
    """
    task_id = request.POST['task_id']
    rel = StudentTaskRel.objects.get(pk=task_id)
    task = rel.task
    task_obj = Task.from_string(rel.task.str_repr)

    users_solve = compose_partial_solve(request.POST, len(task_obj.elements))

    # rel = StudentTaskRel.objects.get(task=task, student=StudentModel.objects.get(user=request.user))
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

    context = {'json_table_solve': json.dumps(users_solve),
               'json_correct_solve': json.dumps({'table': task.answer_table,
                                                 'properties': task.answer_properties}),
               'task': task_obj,
               'task_id': task_id,
               'result': result}

    response = render(request, 'StudentSite/train_base.html', context)

    return response


def control_warshalls(request):
    user = request.user
    student = user.studentmodel
    control_task = student.studenttaskrel_set.filter(isTestTask=True, isCompleted=False)[0]
    task_obj = Task.from_string(control_task.task.str_repr)

    context = {'task': task_obj, 'task_id': control_task.id}
    if control_task.is_warshall_completed:
        context['result'] = True

    if task_obj.is_of_order() != OrderType.not_of_order:
        context['is_of_order'] = True

    context['json_table_solve'] = json.dumps(control_task.task.answer_table)
    context['json_partial_warshalls'] = json.dumps(control_task.partial_solve_warshalls)

    return render(request, 'StudentSite/control_warshalls.html', context)


def control_warshalls_check_tables(request):
    task_id = request.POST['task_id']
    control_task = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(control_task.task.str_repr)

    warshall_answers = control_task.task.answer_warshalls
    if warshall_answers is None:
        warshall_answers = task_obj.generate_warshalls_strings_tables()
        task = control_task.task
        task.answer_warshalls = ' '.join(warshall_answers)
        task.save()
    else:
        warshall_answers = warshall_answers.split(' ')

    result = True
    partial_solve_warshall = []
    for i in range(0, len(task_obj.elements)):
        users_response = request.POST['warshall_check_' + str(i)]
        result = result and (users_response == warshall_answers[i])
        partial_solve_warshall.append(users_response)

    control_task.partial_solve_warshalls = ' '.join(partial_solve_warshall)
    control_task.save()

    response = render(request, 'StudentSite/control_warshalls.html', {'task': task_obj,
                                                                      'task_id': task_id,
                                                                      'result': result})
    response.set_cookie('partial_solve_warshall', ' '.join(partial_solve_warshall))
    response.set_cookie('partial_solve', control_task.task.answer_table)
    return response

def control_warshalls_check(request):
    task_id = request.POST['task_id']
    train_task = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(train_task.task.str_repr)

    warshall_answers = train_task.task.answer_warshalls
    if warshall_answers is None:
        warshall_answers = task_obj.generate_warshalls_answers_string()
        task = train_task.task
        task.answer_warshalls = warshall_answers
        task.save()

    users_solve = request.POST['warshall_check']
    print(warshall_answers)
    result = warshall_answers == users_solve

    train_task.partial_solve_warshalls = users_solve
    is_of_order = task_obj.is_of_order() != OrderType.not_of_order
    print(is_of_order)

    if result:
        train_task.is_warshall_completed = True
        if not is_of_order:
            train_task.isCompleted = True
    else:
        train_task.numberOfAttempts += 1
    train_task.save()



    response = render(request, 'StudentSite/control_warshalls.html',
                      {'task': task_obj,
                       'task_id': task_id,
                       'result': result,
                       'is_of_order': is_of_order})

    response.set_cookie('partial_solve_warshall', users_solve)
    response.set_cookie('partial_solve', train_task.task.answer_table)
    return response


def train_warshalls(request):
    task_id = request.POST['task_id']
    rel = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(rel.task.str_repr)
    context = {'task': task_obj,
               'task_id': rel.id,
               'json_table_solve': json.dumps(rel.task.answer_table),
               'json_warshalls_partial': json.dumps(rel.partial_solve_warshalls)}

    return render(request, 'StudentSite/train_warshalls.html', context)


def train_warshalls_check(request):
    task_id = request.POST['task_id']
    rel = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(rel.task.str_repr)

    warshall_answers = rel.task.answer_warshalls
    if warshall_answers is None:
        warshall_answers = task_obj.generate_warshalls_answers_string()
        task = rel.task
        task.answer_warshalls = warshall_answers
        task.save()

    users_solve = request.POST['warshall_check']
    result = warshall_answers == users_solve

    rel.partial_solve_warshalls = users_solve
    is_of_order = (task_obj.is_of_order() != OrderType.not_of_order)

    if result:
        rel.is_warshall_completed = True
        if not is_of_order:
            rel.isCompleted = True
            rel.dateCompleted = timezone.now()

    else:
        rel.numberOfAttempts += 1
    rel.save()

    response = render(request, 'StudentSite/train_warshalls.html', {'task': task_obj,
                                                                    'task_id': task_id,
                                                                    'result': result,
                                                                    'is_of_order': is_of_order})
    response.set_cookie('partial_solve_warshall', users_solve)
    response.set_cookie('partial_solve', rel.task.answer_table)
    response.set_cookie('correct_solve_warshall', warshall_answers)
    return response


def control_topological(request):
    user = request.user
    student = user.studentmodel
    control_task = student.studenttaskrel_set.filter(isTestTask=True, isCompleted=False)[0]
    task_obj = Task.from_string(control_task.task.str_repr)

    json_data = {'elements': task_obj.elements,
                            'table_solve': control_task.task.answer_table}

    if control_task.partial_solve_topological_sort is not None:
        json_data['partial_solve_sort'] = control_task.partial_solve_topological_sort

    json_data = json.dumps(json_data)

    response = render(request, 'StudentSite/control_topological_sort.html', {'task': task_obj,
                                                                             'task_id': control_task.id,
                                                                             'json_data': json_data})
    #table_solve = control_task.task.answer_table
    #response.set_cookie('partial_solve', table_solve)
    #response.delete_cookie('correct_solve_warshall')
    #if control_task.partial_solve_warshalls is not None:
        #response.set_cookie('partial_solve_warshall', control_task.partial_solve_warshalls)
    return response


def control_topological_check(request):
    task_id = request.POST['task_id']
    task_rel = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(task_rel.task.str_repr)

    students_answers = []
    for i in range(0, len(task_obj.elements)):
        students_answers.append(int(request.POST['submit_element-%s' % i]))


    task_rel.partial_solve_topological_sort = ' '.join([str(elem) for elem in students_answers])

    json_data = json.dumps({'elements': task_obj.elements,
                            'table_solve': task_rel.task.answer_table,
                            'partial_solve_sort': task_rel.partial_solve_topological_sort})

    order = task_obj.is_of_order()

    result = (task_obj.is_correct_topological_sort(students_answers, order.is_strict()) == -1)

    if result:
        task_rel.is_topological_sort_completed = True
        task_rel.isCompleted = True
        task_rel.dateCompleted = timezone.now()
    else:
        task_rel.numberOfAttempts += 1

    task_rel.save()

    response = render(request, 'StudentSite/control_topological_sort.html', {'task': task_obj,
                                                                             'task_id': task_rel.id,
                                                                             'result': result,
                                                                             'json_data': json_data})
    return response


def train_topological(request):
    task_id = request.POST['task_id']
    task_rel = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(task_rel.task.str_repr)

    json_data = {'elements': task_obj.elements,
                 'table_solve': task_rel.task.answer_table}

    if task_rel.partial_solve_topological_sort is not None:
        json_data['partial_solve_sort'] = task_rel.partial_solve_topological_sort

    json_data = json.dumps(json_data)

    response = render(request, 'StudentSite/train_topological_sort.html', {'task': task_obj,
                                                                             'task_id': task_rel.id,
                                                                             'json_data': json_data})

    return response


def train_topological_check(request):
    task_id = request.POST['task_id']
    task_rel = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(task_rel.task.str_repr)

    students_answers = []
    for i in range(0, len(task_obj.elements)):
        students_answers.append(int(request.POST['submit_element-%s' % i]))


    task_rel.partial_solve_topological_sort = ' '.join([str(elem) for elem in students_answers])

    json_data = json.dumps({'elements': task_obj.elements,
                            'table_solve': task_rel.task.answer_table,
                            'partial_solve_sort': task_rel.partial_solve_topological_sort})

    order = task_obj.is_of_order()

    result = task_obj.is_correct_topological_sort(students_answers, order.is_strict())

    context = {'task': task_obj,
               'task_id': task_rel.id,
               'result': result == -1,
               'json_data': json_data }

    if result == -1:
        task_rel.is_topological_sort_completed = True
        task_rel.isCompleted = True
        task_rel.dateCompleted = timezone.now()
    else:
        task_rel.numberOfAttempts += 1
        context['error_id'] = result

    task_rel.save()

    response = render(request, 'StudentSite/train_topological_sort.html', context)
    return response


def add_task(request):
    if 'task_str' in request.POST:
        task_str = request.POST['task_str']
        diff = request.POST['difficulty']
        TaskModel.objects.create(str_repr=task_str, difficulty=int(diff))
        return HttpResponseRedirect(reverse('student_site:add_task'))
    return render(request, 'StudentSite/forms/add_task_form.html')