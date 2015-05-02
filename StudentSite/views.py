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
    # getting task_id
    task_id = request.POST['task_id']
    # getting task model object by id
    task = TaskModel.objects.get(pk=task_id)
    # creating task object
    task_obj = Task.from_string(task.str_repr)
    # getting all attributes of relation. (not effective for now, we'll probably store all of this in DB in future
    # array of triplets
    # (name of form input, correct value of input)
    if task.answer_table is None:
        task.answer_table = task_obj.solve_string()
        task.save()

    checkboxes_array = [
        ("reflexivity", "reflexive" if task_obj.is_reflexive() else "non-reflexive"),
        ("anti-reflexivity", "anti-reflexive" if task_obj.is_antireflexive() else "non-anti-reflexive"),
        ("symmetry", "symmetric" if task_obj.is_symmetric() else "non-symmetric"),
        ("asymmetry", "asymmetric" if task_obj.is_asymmetric() else "non-asymmetric"),
        ("antisymmetry", "antisymmetric" if task_obj.is_antisymmetric() else "non-antisymmetric"),
        ("transitivity", "transitive" if task_obj.is_transitive() else "non-transitive"),
        ("equivalency", "equivalent" if task_obj.is_of_equivalence() else "non-equivalent"),
        ("order", "of-order" if task_obj.is_of_order() != OrderType.not_of_order else "not-of-order"),
        ("order-strict", "strict" if task_obj.is_of_order().is_strict() else "not-strict"),
        ("order-linearity", "linear" if task_obj.is_of_order().is_partial() else "partial")
    ]

    if checkboxes_array[7][1] == 'not-of-order':
        checkboxes_array = checkboxes_array[:-2]

    if task.answer_properties is None:
        task.answer_properties = '$'.join(['='.join([item[0], item[1]]) for item in checkboxes_array])
        task.save()
    # setting initial result to True
    result = True
    # variable for storing users progress
    checkboxes_saved_result = ""
    # iterating over relation attributes list
    for (check_name, check_answer) in checkboxes_array:
        # checking, if current property exists in list (for strict, linear)
        if check_name in request.POST:
            # getting users answer
            answer = request.POST[check_name]
            # modifying result
            result = result and (answer == check_answer)
            # adding answer to saved results
            checkboxes_saved_result = '$'.join([checkboxes_saved_result, "%s=%s" % (check_name, answer)])
    # removing first $ from saved result
    checkboxes_saved_result = checkboxes_saved_result[1:]

    # initializing users solve result for table
    ar_solve = []
    for i in range(0, len(task_obj.elements)):
        # initializing a row of answers
        ar_row = []
        for j in range(0, len(task_obj.elements)):
            # getting value of (i,j) checkbox input
            if "%s-%s" % (i, j) in request.POST:
                # if exists, than True
                ar_row.append(True)
            else:
                ar_row.append(False)
        ar_solve.append(ar_row)
    # modifying result depending on correctness of table
    result = result and (task_obj.solve() == ar_solve)
    # rendering response with result in context
    response = render(request, 'StudentSite/test_base.html', {'task': task_obj,
                                                              'task_id': task_id,
                                                              'result': result})
    # preparing saved result cookie
    for i in range(0, len(ar_solve)):
        ar_solve[i] = ' '.join(['+' if elem else '-' for elem in ar_solve[i]])
    ar_solve = '$'.join(ar_solve)
    ar_solve = '@'.join([ar_solve, checkboxes_saved_result])
    student = request.user.studentmodel
    rel = task.studenttaskrel_set.get(student=student)
    rel.numberOfAttempts += 1
    # saving partial solve result in DB
    rel.partial_solve = ar_solve
    rel.isCompleted = result
    rel.save()
    # setting cookie
    response.set_cookie('partial_solve', ar_solve)
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
    # getting task_id
    task_id = request.POST['task_id']
    # getting task model object by id
    task = TaskModel.objects.get(pk=task_id)
    # creating task object
    task_obj = Task.from_string(task.str_repr)
    # getting all attributes of relation. (not effective for now, we'll probably store all of this in DB in future
    # array of triplets
    # (name of form input, correct value of input)
    if task.answer_table is None:
        task.answer_table = task_obj.solve_string()
        print(task_obj.solve_string())
        task.save()

    checkboxes_array = [
        ("reflexivity", "reflexive" if task_obj.is_reflexive() else "non-reflexive"),
        ("anti-reflexivity", "anti-reflexive" if task_obj.is_antireflexive() else "non-anti-reflexive"),
        ("symmetry", "symmetric" if task_obj.is_symmetric() else "non-symmetric"),
        ("asymmetry", "asymmetric" if task_obj.is_asymmetric() else "non-asymmetric"),
        ("antisymmetry", "antisymmetric" if task_obj.is_antisymmetric() else "non-antisymmetric"),
        ("transitivity", "transitive" if task_obj.is_transitive() else "non-transitive"),
        ("equivalency", "equivalent" if task_obj.is_of_equivalence() else "non-equivalent"),
        ("order", "of-order" if task_obj.is_of_order() != OrderType.not_of_order else "not-of-order"),
        ("order-strict", "strict" if task_obj.is_of_order().is_strict() else "not-strict"),
        ("order-linearity", "linear" if task_obj.is_of_order().is_partial() else "partial")
    ]

    if checkboxes_array[7][1] == 'not-of-order':
        checkboxes_array[8] = ("order-strict", "none")
        checkboxes_array[9] = ("order-linearity", "none")

    if task.answer_properties is None:
        task.answer_properties = '$'.join(['='.join([item[0], item[1]]) for item in checkboxes_array])
        task.save()
    # setting initial result to True
    result = True
    # variable for storing users progress
    checkboxes_saved_result = ""
    # iterating over relation attributes list
    for (check_name, check_answer) in checkboxes_array:
        # checking, if current property exists in list (for strict, linear)
        if check_name in request.POST:
            # getting users answer
            answer = request.POST[check_name]
            # modifying result
            result = result and (answer == check_answer)
            # adding answer to saved results
            checkboxes_saved_result = '$'.join([checkboxes_saved_result, "%s=%s" % (check_name, answer)])
    # removing first $ from saved result
    checkboxes_saved_result = checkboxes_saved_result[1:]

    # initializing users solve result for table
    ar_solve = []
    for i in range(0, len(task_obj.elements)):
        # initializing a row of answers
        ar_row = []
        for j in range(0, len(task_obj.elements)):
            # getting value of (i,j) checkbox input
            if "%s-%s" % (i, j) in request.POST:
                # if exists, than True
                ar_row.append(True)
            else:
                ar_row.append(False)
        ar_solve.append(ar_row)
    # modifying result depending on correctness of table
    result = result and (task_obj.solve() == ar_solve)
    # rendering response with result in context
    response = render(request, 'StudentSite/train_base.html', {'task': task_obj,
                                                               'task_id': task_id,
                                                               'result': result})
    # preparing saved result cookie
    for i in range(0, len(ar_solve)):
        ar_solve[i] = ' '.join(['+' if elem else '-' for elem in ar_solve[i]])
    ar_solve = '$'.join(ar_solve)
    ar_solve = '@'.join([ar_solve, checkboxes_saved_result])
    student = request.user.studentmodel
    rel = task.studenttaskrel_set.get(student=student)
    rel.numberOfAttempts += 1
    # saving partial solve result in DB
    rel.partial_solve = ar_solve
    rel.isCompleted = result
    rel.save()
    # setting cookie
    response.set_cookie('partial_solve', ar_solve)
    response.set_cookie('correct_solve_table', task.answer_table)
    response.set_cookie('correct_solve_props', task.answer_properties)
    return response