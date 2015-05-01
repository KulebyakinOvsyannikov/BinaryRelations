from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import Student, Task, StudentTaskRel
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .MathBackend import Task as Task_Backend
from django.views.decorators.http import require_POST


def index_view(request):
    request.POST = []
    return render(request, 'StudentSite/index.html')


def test_view(request):
    user = request.user
    task_rel = Student.objects.get(user=user).studenttaskrel_set.get(isTestTask=True)
    task_obj = Task_Backend.from_string(task_rel.task.str_repr)
    response = render(request, 'StudentSite/test_base.html', {'task': task_obj, 'task_id': task_rel.id})
    response.set_cookie('partial_solve', task_rel.partial_solve)
    return response


@require_POST
def check_test_task(request):
    task_id = request.POST['task_id']
    task = Task.objects.get(id=task_id)
    task_obj = Task_Backend.from_string(task.str_repr)
    checkboxes_array = [("reflexivity", "reflexive" if task_obj.is_reflexive() else "non-reflexive"),
                        ("anti-reflexivity", "reflexive" if task_obj.is_antireflexive() else "non-reflexive"),
                        ("symmetry", "reflexive" if task_obj.is_symmetric() else "non-reflexive"),
                        ("asymmetry", "reflexive" if task_obj.is_asymmetric() else "non-reflexive"),
                        ("antisymmetry", "reflexive" if task_obj.is_antisymmetric() else "non-reflexive"),
                        ("transitivity", "reflexive" if task_obj.is_transitive() else "non-reflexive"),
                        ("equivalency", "reflexive" if task_obj.is_of_equivalence() else "non-reflexive"),
                        ("order", "reflexive" if task_obj.is_of_order() else "non-reflexive"),
                        ("order-strict", "reflexive" if task_obj.is_reflexive() else "non-reflexive"),
                        ("order-linearity", "reflexive" if task_obj.is_reflexive() else "non-reflexive"),
                        ]
    result = True
    checkboxes_saved_result=""
    for (check_name, check_answer) in checkboxes_array:
        if check_name in request.POST:
            answer = request.POST[check_name]
            result = result and (answer == check_answer)
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
    print(ar_solve)
    student = request.user.student
    rel = task.studenttaskrel_set.get(student=student)
    rel.partial_solve = ar_solve
    rel.save()
    response.set_cookie('partial_solve', ar_solve)
    return response


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