from django.shortcuts import render
from StudentSite.models import StudentTaskRel


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

def result(request):
    task_rel = StudentTaskRel.objects.get(id=request.POST['relation_id'])
    print(task_rel.numberOfAttempts)
    return render(request, 'StudentSite/site_pages/results.html',{
        "task_rel": task_rel,
        "is_control": task_rel.isTestTask
    })
