from .RelationTriplet import RelationTriplet
from .UnaryRelation import UnaryRelation
from .BinaryRelation import BinaryRelation
import os


class Task:
    def __init__(self, elements, triplets, block_modifiers, triplets_triplets_rel, parenthesis):
        """
        :rtype: Task
        :param elements: Array of ints
        :param triplets: Array of RelationTriplet
        :param block_modifiers: Array of UnaryRelation
        :param triplets_triplets_rel: Array of BinaryRelation (logic)
        :type elements: list [int]
        :type triplets: list [RelationTriplet]
        :type block_modifiers: list [UnaryRelation]
        :type triplets_triplets_rel: list [BinaryRelation]
        :type parenthesis: list [(int,int)]
        :return: instance of Task
        """

        self.elements = elements
        self.triplets = triplets
        self.block_modifiers = block_modifiers
        self.triplets_triplets_rel = triplets_triplets_rel
        self.parenthesis = parenthesis
        self.results = None
        """type : list [list [bool]] | None"""

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, task_string):
        """
        :rtype : Task
        :param task_string: String in
                            "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and ]$[(0, 1)]" format
        :return: initialized instance of Task
        """
        task_elements = task_string.split('$')

        elements = []
        if len(task_elements[0]) > 0:
            elements = [int(int_str) for int_str in task_elements[0][1:-1].split(',')]

        triplets = []
        if len(task_elements[1]) > 0:
            triplets = [RelationTriplet(*arg_tuple)
                        for arg_tuple in [(rel_elements[0][1:], BinaryRelation(rel_elements[1]), rel_elements[2][:-1])
                                          for rel_elements in [single_rel.split('|')
                                                               for single_rel in task_elements[1].split('@')]]]

        parenthesis = eval(task_elements[4])

        block_modifiers = []
        if len(parenthesis) > 0:
            block_modifiers = [UnaryRelation(mod) for mod in task_elements[2][1:-1].split('@')]

        triplets_triplets_rel = []
        if len(triplets) > 1:
            triplets_triplets_rel = [BinaryRelation(mod) for mod in task_elements[3][1:-1].split('@')]



        return Task(elements, triplets, block_modifiers, triplets_triplets_rel, parenthesis)

    def to_string(self):
        """
        :rtype: str
        :param self
        :return: String in "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not @ ]$[ and ]$[(0, 1)]" format
        """
        elem_str = str(self.elements)
        str_triplets_list = '@'.join(['[' + tri.mod1 + '|' + tri.relation.value + '|' + tri.mod2 + ']'
                                      for tri in self.triplets])
        trip_mod_list = '[' + '@'.join(mod.value for mod in self.block_modifiers) + ']'
        trip_rel_list = '[' + '@'.join(rel.value for rel in self.triplets_triplets_rel) + ']'
        parenthesis = str(self.parenthesis)
        return '$'.join([elem_str, str_triplets_list, trip_mod_list, trip_rel_list, parenthesis])

    def solve_for_xy(self, e1, e2):
        """
        Returns True, if e1 and e2 are in a binary relation. (Nested parenthesis are not supported).
        :rtype: bool
        :param e1: First element of relation (ab)
        :param e2: Second element of relation (cd)
        :return: abRcd (True/ False)
        """
        triplets = [elem.check(e1, e2) for elem in self.triplets]

        if len(triplets) == 0:
            return None

        def is_in_parenthesis(ind):
            for parenthesis_pair in self.parenthesis:
                if parenthesis_pair[0] <= ind < parenthesis_pair[1]:
                    return True
                return False

        for i in range(0, min(len(self.block_modifiers), len(self.parenthesis))):
            par_pair = self.parenthesis[i]
            res = triplets[par_pair[0]]
            for j in range(par_pair[0], par_pair[1]):
                res = self.triplets_triplets_rel[j].apply_binary_relation(res, triplets[j+1])
            triplets[par_pair[0]] = self.block_modifiers[i].apply_unary_relation(res)

        res = triplets[0]
        for i in range(0, len(self.triplets_triplets_rel)):
            if not is_in_parenthesis(i):
                res = self.triplets_triplets_rel[i].apply_binary_relation(res, triplets[i+1])

        return res

    def solve(self):
        """
        :rtype: list
        :return: two-dimensional array of booleans with answers for Adjacency matrix of current Binary relation
        """
        results = []
        for e1 in self.elements:
            results_row = []
            for e2 in self.elements:
                results_row.append(self.solve_for_xy(e1, e2))
            results.append(results_row)
        self.results = results
        return results

    def print_solve(self):
        """
        :rtype: str
        :returns: String with a matrix of answers (+/-)
        """
        res = ""
        if self.results is not None:
            # noinspection PyTypeChecker
            for row in self.results:
                for item in row:
                    if item:
                        res += '+ '
                    else:
                        res += '- '
                res = res[:-1] + os.linesep
            return res
        else:
            self.solve()
            self.print_solve()

    def is_reflexive(self):
        if self.results is None:
            for elem in self.elements:
                if not self.solve_for_xy(elem, elem):
                    return False
            return True
        else:
            # noinspection PyTypeChecker
            for i in range(0, len(self.results)):
                if not self.results[i][i]:
                    return False
            return True

    # noinspection PyTypeChecker
    def is_antisymmetric(self):
        if self.results is None:
            self.solve()
        for i in range(1, len(self.results)):
            for j in range(i + 1, len(self.results)):
                if i == j: continue
                if self.results[i][j] != self.results[j][i]:
                    return False
        return True


