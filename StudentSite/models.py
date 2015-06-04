from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import random
from random import randint

# Create your models here.


class TaskModel(models.Model):
    str_repr = models.CharField(max_length=255)
    difficulty = models.IntegerField(default=0)
    answer_matrix = models.CharField(max_length=255, null=True, default=None)
    answer_properties = models.TextField(null=True, default=None)
    answer_warshalls = models.TextField(null=True, default=None)

    @classmethod
    def get_control_task(cls):
        tasks = cls.objects.exclude(studenttaskrel__isnull=False).filter(difficulty=3)
        if len(tasks) < 20:
            from .MathBackend.TaskGenerator import TaskGenerator
            task_objects = TaskGenerator.generate_tasks_with_difficulty('hard')
            for task in task_objects:
                cls.objects.create(str_repr=task.to_string(), difficulty=3)
        return random.choice(tasks)

    @classmethod
    def get_training_task_with_difficulty(cls, difficulty):
        difficulty_num = {'easy': 1, 'medium': 2, 'hard': 3}[difficulty]
        tasks = cls.objects.filter(
            Q(difficulty=difficulty_num) & ((
                Q(studenttaskrel__isTestTask=True) &
                Q(studenttaskrel__isCompleted=True) |
                Q(studenttaskrel__isTestTask=False)) | Q(studenttaskrel__isnull=True))
        )
        if len(tasks) < 20:
            from .MathBackend.TaskGenerator import TaskGenerator
            object_items = TaskGenerator.generate_tasks_with_difficulty(difficulty)
            for item in object_items:
                cls.objects.create(str_repr=item.to_string(), difficulty=difficulty_num)
        return random.choice(tasks)

    @classmethod
    def get_demo_task(cls):
        """
        :rtype: TaskModel
        :return:
        """
        tasks = cls.objects.filter(difficulty=1)

        if len(tasks) < 20:
            from .MathBackend.TaskGenerator import TaskGenerator
            object_items = TaskGenerator.generate_tasks_with_difficulty('easy')
            for item in object_items:
                cls.objects.create(str_repr=item.to_string(), difficulty=1)

        return random.choice(tasks)

    def __str__(self):
        return self.str_repr


class StudentModel(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(null=True)
    group = models.CharField(max_length=8)
    tasks = models.ManyToManyField(TaskModel, through='StudentTaskRel')


class StudentTaskRel(models.Model):
    task = models.ForeignKey(TaskModel)
    student = models.ForeignKey(StudentModel)
    isTestTask = models.BooleanField()
    dateStarted = models.DateTimeField(auto_created=True)
    isCompleted = models.BooleanField(default=False)
    numberOfAttempts = models.IntegerField(default=0)
    dateCompleted = models.DateTimeField(null=True)

    matrix_completed = models.BooleanField(default=False)
    properties_completed = models.BooleanField(default=False)
    is_warshall_completed = models.BooleanField(default=False)
    is_topological_sort_completed = models.BooleanField(default=False)

    partial_solve_matrix = models.TextField(null=True, default=None)
    partial_solve_properties = models.TextField(null=True, default=None)
    partial_solve_warshalls = models.TextField(null=True, default=None)
    partial_solve_topological_sort = models.TextField(null=True, default=None)






