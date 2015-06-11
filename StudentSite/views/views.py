from django.shortcuts import render
from StudentSite.models import StudentTaskRel
from django.contrib.auth.decorators import login_required
from django.http import Http404


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

@login_required(login_url="student_site:login_registration")
def teachers_view(request):
    user = request.user
    if not user.is_superuser:
        return Http404(request)

    context = {
        "results": StudentTaskRel.objects.filter(isTestTask=True).order_by('student__group', 'student__user__last_name')
    }

    return render(request, 'StudentSite/site_pages/professors_page.html', context)
