import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.utils import timezone

from StudentSite.models import TaskModel, StudentTaskRel
from StudentSite.MathBackend.Task import Task
from StudentSite.MathBackend.OrderType import OrderType


@login_required(login_url="student_site:login_registration")
def matrix(request):
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

    context = {'task': task_obj,
               'relation_id': control_task.id,
               'is_control': True}

    if control_task.matrix_completed:
        context['result'] = True

    context['partial_solve'] = json.dumps(control_task.partial_solve_matrix)

    return render(request, 'StudentSite/site_pages/matrix.html', context)

def matrix_check(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])
    task = st_task_rel.task
    task_obj = Task.from_string(task.str_repr)

    if task.answer_matrix is None:
        task.answer_matrix = task_obj.solve_string()
        task.save()

    st_task_rel.partial_solve_matrix = request.POST['answers_string']
    st_task_rel.save()

    if st_task_rel.partial_solve_matrix == task.answer_matrix:
        result = True
        st_task_rel.matrix_completed = True
        st_task_rel.save()
    else:
        st_task_rel.numberOfAttempts += 1
        st_task_rel.save()
        result = False

    context = {'task': task_obj,
               'result': result,
               'relation_id': st_task_rel.id,
               'is_control': True,
               'partial_solve': json.dumps(st_task_rel.partial_solve_matrix),}

    return render(request, 'StudentSite/site_pages/matrix.html', context)

def properties(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])

    context = {"relation_id": st_task_rel.id,
               "result": True if st_task_rel.properties_completed else None,
               "task": Task.from_string(st_task_rel.task.str_repr),
               "is_control": True,
               "partial_solve": json.dumps(st_task_rel.partial_solve_properties),
               "matrix_solve": json.dumps(st_task_rel.task.answer_matrix)
               }

    return render(request, 'StudentSite/site_pages/properties.html', context)

def check_properties(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])
    task_obj = Task.from_string(st_task_rel.task.str_repr)

    st_task_rel.partial_solve_properties = request.POST['answers_string']
    st_task_rel.save()

    if st_task_rel.task.answer_properties is None:
        st_task_rel.task.answer_properties = task_obj.solve_properties()
        st_task_rel.task.save()

    if st_task_rel.partial_solve_properties == st_task_rel.task.answer_properties:
        result = True
        st_task_rel.properties_completed = True
        st_task_rel.save()
    else:
        st_task_rel.numberOfAttempts += 1
        st_task_rel.save()
        result = False

    context = {"relation_id": st_task_rel.id,
               "result": result,
               "task": task_obj,
               "is_control": True,
               "partial_solve": json.dumps(st_task_rel.partial_solve_properties),
               "matrix_solve": json.dumps(st_task_rel.task.answer_matrix)
               }

    return render(request, 'StudentSite/site_pages/properties.html', context)

def warshalls(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])

    context = {"relation_id": st_task_rel.id,
               "result": True if st_task_rel.is_warshall_completed else None,
               "task": Task.from_string(st_task_rel.task.str_repr),
               "is_control": True,
               "partial_solve": json.dumps(st_task_rel.partial_solve_warshalls),
               "matrix_solve": json.dumps(st_task_rel.task.answer_matrix)
               }

    return render(request, 'StudentSite/site_pages/warshalls.html', context)

def check_warshalls(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])

    st_task_rel.partial_solve_warshalls = request.POST['answers_string']
    task_obj = Task.from_string(st_task_rel.task.str_repr)
    st_task_rel.save()

    if st_task_rel.task.answer_warshalls is None:
        st_task_rel.task.answer_warshalls = task_obj.generate_warshalls_strings()
        st_task_rel.task.save()

    if st_task_rel.task.answer_warshalls == st_task_rel.partial_solve_warshalls:
        st_task_rel.is_warshall_completed = True
        st_task_rel.save()
        if task_obj.has_loops():
            st_task_rel.isCompleted = True
            st_task_rel.dateCompleted = timezone.now()
            st_task_rel.save()
            from .views import result
            return result(request)
        result = True
    else:
        st_task_rel.numberOfAttempts += 1
        st_task_rel.save()
        result = False

    context = {"relation_id": st_task_rel.id,
               "result": result,
               "task": task_obj,
               "is_control": True,
               "partial_solve": json.dumps(st_task_rel.partial_solve_warshalls),
               "matrix_solve": json.dumps(st_task_rel.task.answer_matrix),
               }

    return render(request, 'StudentSite/site_pages/warshalls.html', context)

def topological(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])

    context = {"relation_id": st_task_rel.id,
               "result": True if st_task_rel.is_topological_sort_completed else None,
               "task": Task.from_string(st_task_rel.task.str_repr),
               "is_control": True,
               "matrix_solve": json.dumps(st_task_rel.task.answer_matrix)
               }

    if st_task_rel.partial_solve_topological_sort is not None:
        context["partial_solve"] = json.dumps(st_task_rel.partial_solve_topological_sort)

    return render(request, 'StudentSite/site_pages/topological.html', context)

def check_topological(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])

    st_task_rel.partial_solve_topological_sort = request.POST['answers_string']
    task_obj = Task.from_string(st_task_rel.task.str_repr)
    st_task_rel.save()
    correct = task_obj.correct_topological_from_users(st_task_rel.partial_solve_topological_sort)

    if correct == st_task_rel.partial_solve_topological_sort:
        st_task_rel.is_topological_sort_completed = True
        st_task_rel.isCompleted = True
        st_task_rel.dateCompleted = timezone.now()
        st_task_rel.save()
        from .views import result
        return result(request)
    else:
        st_task_rel.numberOfAttempts += 1
        st_task_rel.save()

    context = {
        "relation_id": st_task_rel.id,
        "result": False,
        "task": task_obj,
        "is_control": True,
        "partial_solve": json.dumps(st_task_rel.partial_solve_topological_sort),
        "matrix_solve": json.dumps(st_task_rel.task.answer_matrix)
    }

    return render(request, 'StudentSite/site_pages/topological.html', context)
