from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    str_repr = models.CharField(max_length=255)
    difficulty = models.IntegerField(default=0)


class Student(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(null=True)
    tasks = models.ManyToManyField(Task, through='StudentTaskRel')


class StudentTaskRel(models.Model):
    task = models.ForeignKey(Task)
    student = models.ForeignKey(Student)
    isTestTask = models.BooleanField()
    partial_solve = models.CharField(max_length=255, default='')
    isCompleted = models.BooleanField(default=False)
    numberOfAttempts = models.IntegerField(default=0)
    dateStarted = models.DateField(auto_created=True)
    dateCompleted = models.DateField(null=True)
