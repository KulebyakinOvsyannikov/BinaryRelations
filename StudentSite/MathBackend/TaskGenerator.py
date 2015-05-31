__author__ = 'ilyakulebyakin'
from .RelationTriplet import RelationTriplet
from .Task import Task
from .BinaryRelation import BinaryRelation
from .UnaryRelation import UnaryRelation
import random
from ..models import TaskModel
import time

class TaskGenerator:
    logic_relations = [' and ', ' or ', ' ^ ']
    block_modofiers_choice = [' not ', ' ', ' ']
    digit_takers = ['', '/10', '%10']
    modifiers = ['%3', '%4', '%5', '%6', '+1', '+2', '+3', '+4', '-1', '-2', '-3', '-4',
                     '','','','','']
    relations = [' < ', ' > ', ' <= ', ' >= ', ' != ', ' == ']

    @classmethod
    def generate_task_with_difficulty(cls, difficulty):
        num_of_elements = 5 if difficulty == 'easy' else 6 if difficulty == 'medium' else 7
        elements = []

        while len(set(elements)) < 5:
            elements = random.sample(range(10, 100), num_of_elements)

        triplets = []
        if difficulty == 'easy':
            triplets = [cls.generate_triplet() for _ in range(0, 2)]
        if difficulty == 'medium':
            triplets = [cls.generate_triplet() for _ in range(0, 3)]
        if difficulty == 'hard':
            triplets = [cls.generate_triplet() for _ in range(0, 4)]

        tr_tr_rels = [BinaryRelation(random.choice(cls.logic_relations)) for _ in range(0, len(triplets) - 1)]
        parenthesis = []
        parenthesis_part = None
        for x in range(0, len(tr_tr_rels)):
            if random.randint(0, 100) > 75:
                if parenthesis_part is not None and x > parenthesis_part + 1:
                    parenthesis.append((parenthesis_part, x))
                else:
                    parenthesis_part = x

        if parenthesis_part is not None and parenthesis_part < len(tr_tr_rels) - 2:
            parenthesis.append((parenthesis_part, len(tr_tr_rels) - 1))

        block_modifiers = [UnaryRelation(random.choice(cls.block_modofiers_choice)) for x in range(0, len(parenthesis))]

        task = Task(elements=elements,
                    triplets=triplets,
                    block_modifiers=block_modifiers,
                    triplets_triplets_rel=tr_tr_rels,
                    parenthesis=parenthesis)
        if task.is_interesting_task():
            if len(TaskModel.objects.filter(str_repr=task.to_string())) == 0:
                return task
            else:
                print("DUPLICATE")
        return TaskGenerator.generate_task_with_difficulty(difficulty)

    @classmethod
    def generate_triplet(cls):

        mod11 = random.choice(cls.digit_takers)
        mod12 = random.choice(cls.modifiers)

        mod21 = random.choice(cls.digit_takers)
        mod22 = random.choice(cls.modifiers)
        if mod11 != '' or mod12.startswith('%'):
            while mod21 == '' and not mod22.startswith('%'):
                mod21 = random.choice(cls.digit_takers)
                mod22 = random.choice(cls.modifiers)
        else:
            mod21 = ''
            while mod22.startswith('%'):
                mod22 = random.choice(cls.modifiers)

        return RelationTriplet(mod1=mod11 + mod12,
                               mod2=mod21 + mod22,
                               rel=BinaryRelation(random.choice(cls.relations)))

    @classmethod
    def generate_tasks_with_difficulty(cls, difficulty):
        return [cls.generate_task_with_difficulty(difficulty)]

    @classmethod
    def stress_test_tasks_generator(cls):
        number_of_tasks = 0
        total_time_easy = 0
        total_time_medium = 0
        total_time_hard = 0
        last_easy = 0
        last_medium = 0
        last_hard = 0
        while True:
            st_time = time.time()
            TaskModel.objects.create(str_repr=cls.generate_task_with_difficulty('easy').to_string(), difficulty=1)
            last_easy = time.time() - st_time
            total_time_easy += last_easy

            st_time = time.time()
            TaskModel.objects.create(str_repr=cls.generate_task_with_difficulty('medium').to_string(), difficulty=2)
            last_medium = time.time() - st_time
            total_time_medium += last_medium

            easy_st_time = time.time()
            TaskModel.objects.create(str_repr=cls.generate_task_with_difficulty('hard').to_string(), difficulty=3)
            last_hard = time.time() - st_time
            total_time_hard += last_hard

            number_of_tasks += 1

            print("%s generated. Easy: (total : %s average : %s) "
                  "Medium: (total : %s average : %s) "
                  "Hard: (total : %s average : %s)" % (number_of_tasks,
                                                       total_time_easy, total_time_easy/number_of_tasks,
                                                       total_time_medium, total_time_medium/number_of_tasks,
                                                       total_time_hard, total_time_hard/number_of_tasks))



