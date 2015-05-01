from django.contrib import admin
from StudentSite.models import TaskModel, StudentModel, StudentTaskRel
# Register your models here.


class AdminModel(admin.ModelAdmin):
    pass


admin.site.register(TaskModel, AdminModel)
admin.site.register(StudentModel, AdminModel)
admin.site.register(StudentTaskRel, AdminModel)