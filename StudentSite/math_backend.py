from enum import Enum
from .decorators import requires_int_or_bool
import math

debug = True


class RelationBetweenNumbers(Enum):
    eq = '=='
    lt = '<'
    gt = '>'
    lte = '<='
    gte = '>='
    ne = '!='
    lor = 'or'
    land = 'and'
    lxor = '^'
    lnot = 'not'
    lntr = ' '

    #@requires_int_or_bool
    def apply_function(self, value1, value2=None):
        expression = str(value1) + self.value
        if value2 is not None:
            expression += str(value2)
        return eval(expression)


class RelationElement:
    def __init__(self, element, modifier):
        self.element = element
        self.modifier = modifier

    def get_modified(self):
        expression = str(self.element) + self.modifier
        return math.trunc(eval(expression))


class Relation:
    def __init__(self, mod1, rel, mod2):
        self.mod1 = mod1
        self.relation = rel
        self.mod2 = mod2

    def check(self, val1, val2):
        elem1 = RelationElement(val1, self.mod1).get_modified()
        elem2 = RelationElement(val2, self.mod2).get_modified()
        return self.relation.apply_function(elem1, elem2)


class Task:
    def __init__(self, elements, triplets, modifiers):
        self.elements = elements
        self.triplets = triplets
        self.modifiers = modifiers

    def print_some(self):
        num_of_triplets = len(self.modifiers)
        for e1 in self.elements:
            for e2 in self.elements:
                if debug:
                    print(self.modifiers[0].value, end='((')
                    print(e1, end=' ')
                    print(self.triplets[0].mod1, end=' )')
                    print(self.triplets[0].relation.value, end='(')
                    print(e2, end=' ')
                    print(self.triplets[0].mod2, end=') ')

                res = self.modifiers[0].apply_function(self.triplets[0].check(e1,e2))
                for i in range(1, num_of_triplets-1):
                    if debug:
                        print(self.modifiers[num_of_triplets+i-2].value, end=' (')
                        print(e1, end=' ')
                        print(self.triplets[i].mod1, end=' )')
                        print(self.triplets[i].relation.value, end='(')
                        print(e2, end=' ')
                        print(self.triplets[i].mod2, end=') ')
                    arg2 = self.modifiers[i].apply_function(self.triplets[i].check(e1,e2))
                    res = self.modifiers[num_of_triplets+i-2].apply_function(res, arg2)
                print(')', end=' : ')
                print(res)