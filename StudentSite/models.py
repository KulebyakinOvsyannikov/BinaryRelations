from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    str_repr = models.CharField(max_length=255)


class Student(models.Model):
    user = models.OneToOneField(User)
    tasks = models.ManyToManyField(Task, through='StudentTaskRel')


class StudentTaskRel(models.Model):
    task = models.ForeignKey(Task)
    student = models.ForeignKey(Student)
    isTestTask = models.BooleanField()
    isCompleted = models.BooleanField(default=False)
    numberOfAttempts = models.IntegerField(default=0)
    dateStarted = models.DateField(auto_created=True)
    dateCompleted = models.DateField(null=True)
