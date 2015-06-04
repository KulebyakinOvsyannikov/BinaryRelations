from django.shortcuts import render
from StudentSite.models import TaskModel
from StudentSite.MathBackend.Task import Task
import json


def demo(request):
    task = TaskModel.get_demo_task()
    task_obj = Task.from_string(task.str_repr)

    if task.answer_matrix is None or task.answer_properties is None:
        task.answer_matrix = task_obj.solve_string()
        task.answer_properties = task_obj.solve_properties()
        task.answer_warshalls = task_obj.generate_warshalls_strings()
        task.save()

    tips = task_obj.generate_demo_strings()
    json_data = json.dumps({'tips': tips[0],
                            'tipsHighlights': tips[1],
                            'matrixAnswers': task.answer_matrix,
                            'propertiesAnswers': task.answer_properties,
                            'warshallAnswers': task.answer_warshalls,
                            'topologicalAnswers': task_obj.topological_sort()})

    return render(request, 'StudentSite/demo.html', {'task': task_obj,
                                                     'json_demo_data': json_data,
                                                     'json_elements': json.dumps(task_obj.elements)})
