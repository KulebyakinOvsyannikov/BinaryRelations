from .RelationTriplet import RelationTriplet
from .UnaryRelation import UnaryRelation
from .BinaryRelation import BinaryRelation


class Task:
    def __init__(self, elements, triplets, triplet_modifiers, triplets_triplets_rel, parenthesis):
        """
        :rtype: Task
        :param elements: Array of ints
        :param triplets: Array of RelationTriplet
        :param triplet_modifiers: Array of UnaryRelation
        :param triplets_triplets_rel: Array of BinaryRelation (logic)
        :type elements: list [int]
        :type triplets: list [RelationTriplet]
        :type triplet_modifiers: list [UnaryRelation]
        :type parenthesis: list [(int,int)]
        :return: instance of Task
        """

        self.elements = elements
        self.triplets = triplets
        self.triplet_modifiers = triplet_modifiers
        self.triplets_triplets_rel = triplets_triplets_rel
        self.parenthesis = parenthesis
        self.results = None
        """type : list [list [bool]] or None"""

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, task_string):
        """
        :rtype : Task
        :param task_string: String in
                            "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and @...]$[(1, 2)]" format
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
        parenthesis = eval(task_elements[4])
        return Task(elements, triplets, triplet_modifiers, triplets_triplets_rel, parenthesis)

    def to_string(self):
        """
        :rtype: str
        :param self
        :return: String in "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and @...]$[(1, 2)]" format
        """
        elem_str = str(self.elements)
        str_triplets_list = '@'.join(['[' + tri.mod1 + '|' + tri.relation.value + '|' + tri.mod2 + ']'
                                      for tri in self.triplets])
        trip_mod_list = '[' + '@'.join(mod.value for mod in self.triplet_modifiers) + ']'
        trip_rel_list = '[' + '@'.join(rel.value for rel in self.triplets_triplets_rel) + ']'
        parenthesis = str(self.parenthesis)
        return '$'.join([elem_str, str_triplets_list, trip_mod_list, trip_rel_list, parenthesis])