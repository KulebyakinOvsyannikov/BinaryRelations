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

        elements = [] if len(task_elements[0]) == 0 else [int(int_str) for int_str in task_elements[0][1:-1].split(',')]

        triplets = [] if len(task_elements[1]) == 0 \
            else [RelationTriplet(*arg_tuple)
                  for arg_tuple in [(rel_elements[0][1:], BinaryRelation(rel_elements[1]), rel_elements[2][:-1])
                                    for rel_elements in [single_rel.split('|')
                                                         for single_rel in task_elements[1].split('@')]]]
        """:type: list"""
        parenthesis = eval(task_elements[4])

        block_modifiers = [] if len(parenthesis) == 0 \
            else [UnaryRelation(mod) for mod in task_elements[2][1:-1].split('@')]

        triplets_triplets_rel = [] if len(triplets) < 2 \
            else [BinaryRelation(mod) for mod in task_elements[3][1:-1].split('@')]

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

    def to_human_readable(self):
        """
        :rtype: str
        :return: string in easy-to-read "!(a(mod 3) >= d(mod 3) and b(mod 5) != c(mod 5))" format
        """
        readable_string = ''
        block_mod_index = rel_index = parentheses_index = 0
        for trip_index in range(0, len(self.triplets)):
            if parentheses_index < len(self.parenthesis):
                if trip_index == self.parenthesis[parentheses_index][0]:
                    readable_string += '!' if self.block_modifiers[block_mod_index].value == ' not ' \
                        else self.block_modifiers[block_mod_index].value
                    readable_string += '('
            readable_string += self.triplets[trip_index].convert_triplet_to_human_readable()
            if rel_index < len(self.triplets_triplets_rel):
                readable_string += self.triplets_triplets_rel[rel_index].value
                rel_index += 1
            if parentheses_index < len(self.parenthesis):
                if trip_index == self.parenthesis[parentheses_index][1]:
                    readable_string += ')'
                    block_mod_index += 1
                    parentheses_index += 1
        return readable_string

    def solve_for_elements(self, e1, e2):
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
                res = self.triplets_triplets_rel[j].apply_binary_relation(res, triplets[j + 1])
            triplets[par_pair[0]] = self.block_modifiers[i].apply_unary_relation(res)

        res = triplets[0]
        for i in range(0, len(self.triplets_triplets_rel)):
            if not is_in_parenthesis(i):
                res = self.triplets_triplets_rel[i].apply_binary_relation(res, triplets[i + 1])

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
                results_row.append(self.solve_for_elements(e1, e2))
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
                if not self.solve_for_elements(elem, elem):
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
        for i in range(0, len(self.results)):
            for j in range(i + 1, len(self.results)):
                if self.results[i][j] and self.results[j][i]:
                    return False
        return True

    # noinspection PyTypeChecker
    def is_transitive(self):
        if self.results is None:
            self.solve()
        for i in range(0, len(self.results)):
            for j in range(0, len(self.results)):
                for k in range(0, len(self.results)):
                    if not self.results[j][k] and (self.results[j][k] or (self.results[j][i] and self.results[i][k])):
                        return False
        return True

    def topological_sort(self):
        """
        :rtype: list [int] | None
        :return: list of vertex indexes after topological (dfs) sort
        """
        def dfs(ind):
            """
            :rtype: bool
            :type ind: int
            """
            if sort_tree[ind][1] == 1:
                return True
            if sort_tree[ind][1] == 2:
                return False
            sort_tree[ind][1] = 1
            for j in range(0, len(sort_tree[ind][0])):
                if sort_tree[ind][0][j] and j != ind:
                    if dfs(j):
                        return True
            stack.append(ind)
            sort_tree[ind][1] = 2
            return False

        if self.results is None:
            self.solve()
        sort_tree = [[res, 0] for res in self.results]
        stack = []
        for i in range(0, len(sort_tree)):
            if dfs(i):
                return None
        return stack

    def is_correct_topological_sort(self, sort, strict):
        """
        :type sort: list [int]
        :param sort: users sort attempt
        :return: true, is sort is a correct list of sorted indexes
        """
        sort_tree = [[res, False] for res in self.results]
        for i in range(0, len(sort_tree)):
            for k in range(0, len(sort_tree[sort[i]][0])):
                sort_tree[sort[i]][1] = True
                if strict and i == k:
                    if sort_tree[sort[i]][k]:
                        return False
                    else:
                        continue
                if sort_tree[sort[i]][0][k] and not sort_tree[k][1]:
                    print(sort[i], k)
                    return False
        return True