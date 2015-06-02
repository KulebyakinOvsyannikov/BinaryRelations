from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from StudentSite.models import TaskModel, StudentTaskRel
from StudentSite.MathBackend.Task import Task
from StudentSite.MathBackend.OrderType import OrderType
import json
from django.utils import timezone
from StudentSite.MathBackend.supporting_functions import compose_partial_solve


@login_required(login_url="student_site:login_registration")
def training(request):
    return render(request, 'StudentSite/training.html')

def training_with_difficulty(request, difficulty):
    user = request.user
    student = user.studentmodel
    diff = {'easy': 1, 'medium': 2, 'hard': 3}
    st_task_rel = student.studenttaskrel_set.filter(isTestTask=False, isCompleted=False, task__difficulty=diff[difficulty])

    if len(st_task_rel) == 0:
        task = TaskModel.get_training_task_with_difficulty(difficulty)
        task_obj = Task.from_string(task.str_repr)
        st_task_rel = StudentTaskRel(task=task, student=student, isTestTask=False, dateStarted=timezone.now())
        st_task_rel.save()
    else:
        st_task_rel = st_task_rel[0]
        task_obj = Task.from_string(st_task_rel.task.str_repr)

    context = {'task': task_obj, 'relation_id': st_task_rel.id, 'is_control': False}

    if st_task_rel.matrix_completed:
        context['result'] = True

    context['partial_solve'] = json.dumps(st_task_rel.partial_solve_matrix)

    return render(request, 'StudentSite/site_pages/matrix.html', context)

def check_matrix(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])
    task = st_task_rel.task
    task_obj = Task.from_string(task.str_repr)

    if task.answer_matrix is None:
        task.answer_matrix = task_obj.solve_string()
        task.save()

    st_task_rel.partial_solve_matrix = request.POST['answers_string']
    st_task_rel.save()

    print(st_task_rel.partial_solve_matrix)
    print(task.answer_matrix)

    if st_task_rel.partial_solve_matrix == task.answer_matrix:
        result = True
        st_task_rel.matrix_completed = True
        st_task_rel.save()
    else:
        result = False

    context = {'task': task_obj,
               'result': result,
               'relation_id': st_task_rel.id,
               'is_control': False,
               'partial_solve': json.dumps(st_task_rel.partial_solve_matrix),
               'correct_solve': json.dumps(task.answer_matrix)}

    return render(request, 'StudentSite/site_pages/matrix.html', context)

def properties(request):
    st_task_rel = StudentTaskRel.objects.get(pk=request.POST['relation_id'])

    context = {"relation_id": st_task_rel.id,
               "result": True if st_task_rel.properties_completed else None,
               "task": Task.from_string(st_task_rel.task.str_repr),
               "is_control": False,
               "partial_solve": json.dumps(st_task_rel.partial_solve_properties),
               "matrix_solve": json.dumps(st_task_rel.task.answer_matrix)}

    return render(request, 'StudentSite/site_pages/properties.html', context)

def check_properties(request):
    return None



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

    context = {'json_table_solve': json.dumps(users_solve),
               'json_correct_solve': json.dumps({'table': task.answer_matrix,
                                                 'properties': task.answer_properties}),
               'task': task_obj,
               'task_id': task_id,
               'result': result}

    response = render(request, 'StudentSite/train_base.html', context)

    return response

def train_warshalls(request):
    task_id = request.POST['task_id']
    rel = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(rel.task.str_repr)
    context = {'task': task_obj,
               'task_id': rel.id,
               'json_table_solve': json.dumps(rel.task.answer_matrix),
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
    response.set_cookie('partial_solve', rel.task.answer_matrix)
    response.set_cookie('correct_solve_warshall', warshall_answers)
    return response

def train_topological(request):
    task_id = request.POST['task_id']
    task_rel = StudentTaskRel.objects.get(pk=task_id)
    task_obj = Task.from_string(task_rel.task.str_repr)

    json_data = {'elements': task_obj.elements,
                 'table_solve': task_rel.task.answer_matrix}

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
                            'table_solve': task_rel.task.answer_matrix,
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
