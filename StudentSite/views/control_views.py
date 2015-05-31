from django.views.decorators.http import require_POST
from django.shortcuts import render
from StudentSite.models import TaskModel, StudentTaskRel, StudentModel
from StudentSite.MathBackend.Task import Task
from StudentSite.MathBackend.OrderType import OrderType
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from StudentSite.MathBackend.supporting_functions import compose_partial_solve
import json

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

    if task.answer_matrix is None or task.answer_properties is None:
        task.answer_matrix = task_obj.solve_string()
        task.answer_properties = task_obj.solve_properties()
        task.save()

    result = users_solve == '@'.join([task.answer_matrix, task.answer_properties])

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

    context['json_table_solve'] = json.dumps(control_task.task.answer_matrix)
    context['json_partial_warshalls'] = json.dumps(control_task.partial_solve_warshalls)

    return render(request, 'StudentSite/control_warshalls.html', context)

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
    response.set_cookie('partial_solve', train_task.task.answer_matrix)
    return response

def control_topological(request):
    user = request.user
    student = user.studentmodel
    control_task = student.studenttaskrel_set.filter(isTestTask=True, isCompleted=False)[0]
    task_obj = Task.from_string(control_task.task.str_repr)

    json_data = {'elements': task_obj.elements,
                            'table_solve': control_task.task.answer_matrix}

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
                            'table_solve': task_rel.task.answer_matrix,
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