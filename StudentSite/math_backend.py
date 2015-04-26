from enum import Enum
from .decorators import requires_int_or_bool, is_bool
import math

#   Example: "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and @...]"
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


class UnaryRelation(Enum):
    unary_not = ' not '
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
        print("gaw")
        elem1 = RelationElement(val1, self.mod1).get_modified()
        elem2 = RelationElement(val2, self.mod2).get_modified()
        return self.relation.apply_binary_relation(elem1, elem2)

    def __str__(self):
        res = self.mod1 + self.relation.value + self.mod2
        return res

    def __repr__(self):
        return self.__str__()


class Task:
    def __init__(self, elements, triplets, triplet_modifiers, triplets_triplets_rel):
        """
        :rtype: Task
        :param elements: Array of ints
        :param triplets: Array of RelationTriplet
        :param triplet_modifiers: Array of UnaryRelation
        :param triplets_triplets_rel: Array of BinaryRelation (logic)
        :return: instance of Task
        """
        self.elements = elements
        self.triplets = triplets
        self.triplet_modifiers = triplet_modifiers
        self.triplets_triplets_rel = triplets_triplets_rel

    @classmethod
    def from_string(cls, task_string):
        """
            :rtype : Task
            :param task_string: String in "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and @...]" format
            :return: initialized instance of Task
            """
        task_elements = task_string.split('$')
        elements = [int(int_str) for int_str in task_elements[0][1:-1].split(',')]
        triplets = [RelationTriplet(*arg_tuple)
                    for arg_tuple in [(rel_elements[0][1:], BinaryRelation(rel_elements[1]), rel_elements[2][:-1])
                                      for rel_elements in [single_rel.split('|')
                                                           for single_rel in task_elements[1].split('@')]]]
        triplet_modifiers = [UnaryRelation(mod) for mod in task_elements[2][1:-1].split('@')]
        triplets_triplets_rel = [BinaryRelation(mod) for mod in task_elements[3][1:-1].split('@')]
        return Task(elements, triplets, triplet_modifiers, triplets_triplets_rel)
    
    def obj_to_str(self):
        """
        :rtype: str
        :param self
        :return: String in "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and @...]" format
        """
        elem_str = str(self.elements)
        str_triplets_list = []
        for tri in self.triplets:
            trip_part = '[' + tri.mod1 + '| ' + tri.relation.value() + ' |' + tri.mod2 + ']'
            str_triplets_list.append(trip_part)
        str_triplets_list = '@'.join(str_triplets_list)
        trip_mod_list = []
        for mod in self.triplet_modifiers:
            indent_mod = ' ' + mod + ' '
            trip_mod_list.append(indent_mod)
        trip_mod_list = '[' + '@'.join(trip_mod_list) + ']'
        trip_rel_list = []
        for rel in self.triplets_triplets_rel:
            indent_rel = ' ' + rel + ' '
            trip_rel_list.append(indent_rel)
        trip_rel_list = '[' + '@'.join(trip_rel_list) + ']'
        return '$'.join([elem_str, str_triplets_list, trip_mod_list, trip_rel_list])