from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import StudentModel, TaskModel, StudentTaskRel
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .MathBackend import Task as Task_Backend
from django.views.decorators.http import require_POST
from .MathBackend.OrderType import OrderType


def index_view(request):
    """
    'next' may be passed because of attempt to open test_view while not being logged in
    in this case we set context variable which will be included in login form
    :return: Rendered response for index page.
    """
    context = {}
    if 'next' in request.GET:
        context['next'] = request.GET['next']
    return render(request, 'StudentSite/index.html', context)


@login_required(login_url="student_site:index_view")
def test_view(request):
    """

    :return: Rendered response for a page with users test task
    """
    # getting user from request
    user = request.user
    # looking for user<->task relation with isTestTask = True and isCompleted = False (should only be one at a time)
    task_rel = StudentModel.objects.get(user=user).studenttaskrel_set.filter(isTestTask=True).get(isCompleted=False)
    # creating object from relations task model
    task_obj = Task_Backend.from_string(task_rel.task.str_repr)
    # rendering response
    response = render(request, 'StudentSite/test_base.html', {'task': task_obj, 'task_id': task_rel.id})
    # setting response cookie with previous progress on task
    response.set_cookie('partial_solve', task_rel.partial_solve)
    return response


@require_POST
def check_test_task(request):
    """
    :return: rendered response for users attempt to solve test task
    """
    # getting task_id
    task_id = request.POST['task_id']
    # getting task model object by id
    task = TaskModel.objects.get(pk=task_id)
    # creating task object
    task_obj = Task_Backend.from_string(task.str_repr)
    # getting all attributes of relation. (not effective for now, we'll probably store all of this in DB in future
    # array of triplets
    # (name of form input, correct value of input)
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
    # saving partial solve result in DB
    rel.partial_solve = ar_solve
    rel.save()
    # setting cookie
    response.set_cookie('partial_solve', ar_solve)
    return response


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('student_site:index_view'))


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
    if 'next' in request.POST:
        print(request.POST['next'])
        return HttpResponseRedirect(request.POST['next'])
    return HttpResponseRedirect(reverse('student_site:index_view'))