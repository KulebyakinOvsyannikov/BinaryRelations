from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from random import randint
from .MathBackend import Task
from time import sleep
# Create your models here.


class TaskModel(models.Model):
    isGettingTasks = False
    str_repr = models.CharField(max_length=255)
    answer_table = models.CharField(max_length=255, null=True, default=None)
    answer_properties = models.TextField(null=True, default=None)
    difficulty = models.IntegerField(default=0)

    @classmethod
    def get_control_task(cls):
        while cls.isGettingTasks:
            print("got here")
            sleep(1)
        tasks = cls.objects.exclude(studenttaskrel__isnull=False).filter(difficulty=3)
        if len(tasks) < 5:
            cls.isGettingTasks = True
            task_objects = Task.generate_tasks_with_difficulty('hard')
            for task in task_objects:
                cls.objects.create(str_repr=task.to_string(), difficulty=3)
            cls.isGettingTasks = False
            return cls.get_control_task()
        return tasks[randint(0, len(tasks) - 1)]

    @classmethod
    def get_training_task_with_difficulty(cls, difficulty):
        while cls.isGettingTasks:
                print("got here")
        difficulty_num = {'easy': 1, 'medium': 2, 'hard': 3}[difficulty]
        tasks = cls.objects.filter(
            Q(difficulty=difficulty_num) & ((
                Q(studenttaskrel__isTestTask=True) &
                Q(studenttaskrel__isCompleted=True) |
                Q(studenttaskrel__isTestTask=False)) | Q(studenttaskrel__isnull=True))
        )
        if len(tasks) < 5:
            cls.isGettingTasks = True
            object_items = Task.generate_tasks_with_difficulty(difficulty)
            for item in object_items:
                cls.objects.create(str_repr=item.to_string(), difficulty=difficulty_num)
            cls.isGettingTasks = False
            return cls.get_training_task_with_difficulty(difficulty)
        return tasks[randint(0, len(tasks) - 1)]

    def __str__(self):
        return self.str_repr


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
    partial_solve = models.TextField(null=True, default=None)
    isCompleted = models.BooleanField(default=False)
    table_and_props_completed = models.BooleanField(default=False)
    is_topological_sort_completed = models.BooleanField(default=False)
    is_warshall_completed = models.BooleanField(default=False)
    numberOfAttempts = models.IntegerField(default=0)
    dateStarted = models.DateField(auto_created=True)
    dateCompleted = models.DateField(null=True)
