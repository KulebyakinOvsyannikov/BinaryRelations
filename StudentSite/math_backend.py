from enum import Enum
from .decorators import requires_int_or_bool
import math


# "[12,14,15,26]$[%10%3|<=|/10%3]@[/10%3|>=|%10%3]$[!@ ]$[and@...]"
#   Elements: 12, 14, 15, 26
#   Triplets: ab%10%3 <= cd/10%3
#             ab/10%3 >= cd%10%3
#   UnaryMods: not ab%10%3 <= cd/10%3; ab/10%3 >= cd%10%3
#   BinaryRel: and
#   $ between Elements, Triplets, UnaryMods, BinaryRels
#   @ between elements of array of triplets, unaryMods, BinaryRels
#   | between parts of each triplet
#   Object to ^
#   Object to human-readable
#   ^ to object

class UnaryRelation(Enum):
    unary_not = 'not'
    unary_neutral = ' '

    def apply_unary_relation(self, argument):
        if self == UnaryRelation.unary_not:
            return not argument
        else:
            return argument


class BinaryRelation(Enum):
    equal = ' == '
    less_than = ' < '
    greater_than = ' > '
    less_than_or_equal = ' <= '
    greater_than_or_equal = ' >= '
    not_equal = ' != '
    logic_or = ' or '
    logic_and = ' and '
    logic_xor = ' ^ '


    @requires_int_or_bool
    def apply_binary_relation(self, value1, value2):
        expression = str(value1) + self.value + str(value2)
        return eval(expression)


class RelationElement:
    def __init__(self, element, modifier):
        self.element = element
        self.modifier = modifier

    def get_modified(self):
        expression = str(self.element) + self.modifier
        return math.trunc(eval(expression))


class RelationTriplet:
    def __init__(self, mod1, rel, mod2):
        self.mod1 = mod1  # String
        self.relation = rel  # BinaryRelation
        self.mod2 = mod2  # String

    def check(self, val1, val2):
        elem1 = RelationElement(val1, self.mod1).get_modified()
        elem2 = RelationElement(val2, self.mod2).get_modified()
        return self.relation.apply_binary_relation(elem1, elem2)


class Task:
    def __init__(self, elements, triplets, triplet_modifiers, triplets_triplets_rel):
        self.elements = elements  # Array on ints
        self.triplets = triplets  # Array of RelationTriplet
        self.triplet_modifiers = triplet_modifiers  # Array of UnaryRelation
        self.triplets_triplets_rel = triplets_triplets_rel  # Array of BinaryRelation (logic)

    def Obj_to_str(self):
        pass


# "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and @...]"
#   Elements: 12, 14, 15, 26
#   Triplets: ab%10%3 <= cd/10%3
#             ab/10%3 >= cd%10%3
#   UnaryMods: not ab%10%3 <= cd/10%3; ab/10%3 >= cd%10%3
#   BinaryRel: and
#   $ between Elements, Triplets, UnaryMods, BinaryRels
#   @ between elements of array of triplets, unaryMods, BinaryRels
#   | between parts of each triplet
#   Object to ^
#   Object to human-readable
#   ^ to object

#db_string = str(self.elements) +'$'
#        for tri in self.triplets:
#            db_string=db_string+'['+tri.mod1+'| '+str(tri.rel)+' |'+