from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TaskModel(models.Model):
    str_repr = models.CharField(max_length=255)
    answer_table = models.CharField(max_length=255, null=True, default=None)
    answer_properties = models.CharField(max_length=255, null=True, default=None)
    difficulty = models.IntegerField(default=0)


class StudentModel(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(null=True)
    group = models.CharField(max_length=8)
    first_name = models.CharField(max_length=56)
    last_name = models.CharField(max_length=56)
    tasks = models.ManyToManyField(TaskModel, through='StudentTaskRel')


class StudentTaskRel(models.Model):
    task = models.ForeignKey(TaskModel)
    student = models.ForeignKey(StudentModel)
    isTestTask = models.BooleanField()
    partial_solve = models.CharField(max_length=255, default='')
    isCompleted = models.BooleanField(default=False)
    numberOfAttempts = models.IntegerField(default=0)
    dateStarted = models.DateField(auto_created=True)
    dateCompleted = models.DateField(null=True)
