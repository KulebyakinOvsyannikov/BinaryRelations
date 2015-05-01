from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import StudentModel, TaskModel, StudentTaskRel
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .MathBackend import Task as Task_Backend
from django.views.decorators.http import require_POST
from .MathBackend.relation_type import OrderType


def index_view(request):
    request.POST = []
    return render(request, 'StudentSite/index.html')


def test_view(request):
    user = request.user
    task_rel = StudentModel.objects.get(user=user).studenttaskrel_set.get(isTestTask=True)
    task_obj = Task_Backend.from_string(task_rel.task.str_repr)
    response = render(request, 'StudentSite/test_base.html', {'task': task_obj, 'task_id': task_rel.id})
    response.set_cookie('partial_solve', task_rel.partial_solve)
    return response


@require_POST
def check_test_task(request):
    task_id = request.POST['task_id']
    task = TaskModel.objects.get(id=task_id)
    task_obj = Task_Backend.from_string(task.str_repr)
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

    result = True
    checkboxes_saved_result = ""
    for (check_name, check_answer) in checkboxes_array:
        if check_name in request.POST:
            answer = request.POST[check_name]
            result = result and (answer == check_answer)
            if not result:
                print(answer)
            checkboxes_saved_result = '$'.join([checkboxes_saved_result, "%s=%s" % (check_name, answer)])
    checkboxes_saved_result = checkboxes_saved_result[1:]

    ar_solve = []
    for i in range(0, len(task_obj.elements)):
        ar_row = []
        for j in range(0, len(task_obj.elements)):
            if "%s-%s" % (i, j) in request.POST:
                ar_row.append(True)
            else:
                ar_row.append(False)
        ar_solve.append(ar_row)
    result = result and (task_obj.solve() == ar_solve)
    response = render(request, 'StudentSite/test_base.html', {'task': task_obj,
                                                              'task_id': task_id,
                                                              'result': result})
    for i in range(0, len(ar_solve)):
        ar_solve[i] = ' '.join(['+' if elem else '-' for elem in ar_solve[i]])
    ar_solve = '$'.join(ar_solve)
    ar_solve = '@'.join([ar_solve, checkboxes_saved_result])
    student = request.user.studentmodel
    rel = task.studenttaskrel_set.get(student=student)
    rel.partial_solve = ar_solve
    rel.save()
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
    return HttpResponseRedirect(reverse('student_site:index_view'))