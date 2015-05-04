from .RelationTriplet import RelationTriplet
from .UnaryRelation import UnaryRelation
from .BinaryRelation import BinaryRelation
from.OrderType import OrderType
from time import sleep
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
        :return: String in "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not ]$[ and ]$[(0, 1)]" format
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

    def solve_string(self):
        """
        :rtype: str
        :returns: String with a matrix of answers (+/-)
        """
        if self.results is None:
            self.solve()
        return '$'.join([" ".join(['+' if item else '-' for item in row]) for row in self.results])

    def solve_properties(self):
        """
        :rtype: str
        :return: String with property=value answers for task
        """
        checkboxes_array = [
            ("reflexivity", "reflexive" if self.is_reflexive() else "non-reflexive"),
            ("anti-reflexivity", "anti-reflexive" if self.is_antireflexive() else "non-anti-reflexive"),
            ("symmetry", "symmetric" if self.is_symmetric() else "non-symmetric"),
            ("asymmetry", "asymmetric" if self.is_asymmetric() else "non-asymmetric"),
            ("antisymmetry", "antisymmetric" if self.is_antisymmetric() else "non-antisymmetric"),
            ("transitivity", "transitive" if self.is_transitive() else "non-transitive"),
            ("equivalency", "equivalent" if self.is_of_equivalence() else "non-equivalent"),
            ("order", "of-order" if self.is_of_order() != OrderType.not_of_order else "not-of-order"),
            ("order-strict", "strict" if self.is_of_order().is_strict() else "not-strict"),
            ("order-linearity", "linear" if self.is_of_order().is_partial() else "partial")
        ]

        if checkboxes_array[7][1] == 'not-of-order':
            checkboxes_array[8] = ("order-strict", "none")
            checkboxes_array[9] = ("order-linearity", "none")
        print(checkboxes_array)

        res = []
        for item in checkboxes_array:
            res.append(item[0] + '=' + item[1])
        return '$'.join(res)

    def is_reflexive(self):
        """
        :rtype: bool
        :return: True, if binary relation is reflexive
        """
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

    def is_antireflexive(self):
        """
        :rtype: bool
        :return: True, if the relation is antireflexive
        """
        if self.results is None:
            for elem in self.elements:
                if self.solve_for_elements(elem, elem):
                    return False
            return True
        else:
            for i in range(0,len(self.results)):
                if self.results[i][i]:
                    return False
            return True

    def is_symmetric(self):
        """
        :rtype: bool
        :return: True, if the relation is symmetric
        """
        if self.results is None:
            self.solve()
        for i in range(0,len(self.results)):
            for j in range(i+1,len(self.results)):
                if self.results[i][j] != self.results[j][i]:
                    return False
        return True

    def is_asymmetric(self):
        """
        :rtype: bool
        :return: True, if the relation is asymmetric
        """
        if self.results is None:
            self.solve()
        for i in range(0, len(self.results)):
            for j in range(i, len(self.results)):
                if self.results[i][j] and self.results[j][i]:
                    return False
        return True

    # noinspection PyTypeChecker
    def is_antisymmetric(self):
        """
        :rtype: bool
        :return: True, is binary relation is antisymmetric
        """
        if self.results is None:
            self.solve()
        for i in range(0, len(self.results)):
            for j in range(i + 1, len(self.results)):
                if self.results[i][j] and self.results[j][i]:
                    return False
        return True

    # noinspection PyTypeChecker
    def is_transitive(self):
        """
        :rtype: bool
        :return: True, if binary relation is transitive (Warshall's algorithm)
        """
        if self.results is None:
            self.solve()
        for w in range(0, len(self.results)):
            for u in range(0, len(self.results)):
                for v in range(0, len(self.results)):
                    if not self.results[u][v] and (self.results[u][v] or (self.results[u][w] and self.results[w][v])):
                        return False
        return True

    def generate_warshalls_strings(self):
        res = []
        if self.results is None:
            self.solve()
        temp_res = self.results[:]
        print(temp_res)
        for w in range(0, len(self.elements)):
            step_res = ""
            for u in range(0, len(self.elements)):
                for v in range(0, len(self.elements)):
                    should_modify = not temp_res[u][v] and (temp_res[u][v] or (temp_res[u][w] and temp_res[w][v]))

                    step_res += '+' if should_modify else '-'
                    if should_modify:
                        temp_res[u][v] = True
                    if should_modify:
                        print('%s %s through %s' % (u, v, w))
            res.append(step_res)
        return res

    def is_of_equivalence(self):
        """
        :rtype: bool
        :return: True, if the relation is equivalent
        """
        if self.is_reflexive() and self.is_symmetric() and self.is_transitive():
            return True
        return False

    def is_of_order(self):
        """
        :rtype: OrderType
        :return: corresponding value of OrderType enum class, depending on the type of the relation
        """

        def is_linear(results):
            """
            :rtype: bool
            :return: True, if the order is linear, otherwise False
            """
            for i in range(0, len(results)):
                for j in range(i + 1, len(results)):
                    if self.results[i][j] == self.results[j][i]:
                        return False
            return True

        if self.is_asymmetric() and self.is_transitive():
            if self.results is None:
                self.solve()
            if is_linear(self.results):
                return OrderType.strict_and_linear
            return OrderType.strict_and_partial
        if self.is_reflexive() and self.is_antisymmetric() and self.is_transitive():
            if self.results is None:
                self.solve()
            if is_linear(self.results):
                return OrderType.not_strict_and_linear
            return OrderType.not_strict_and_partial
        return OrderType.not_of_order

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

    @classmethod
    def generate_tasks_with_difficulty(cls, difficulty):
        sleep(5)
        return [Task.from_string("[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not ]$[ and ]$[(0, 1)]")
                for i in range(1, 10)]

    def generate_demo_strings(self):
        res = []
        for elem in self.elements:
            for elem2 in self.elements:
                res.append("%s - %s" % (elem, elem2))
        checkboxes_array = [
            ("reflexivity", "reflexive" if self.is_reflexive() else "non-reflexive"),
            ("anti-reflexivity", "anti-reflexive" if self.is_antireflexive() else "non-anti-reflexive"),
            ("symmetry", "symmetric" if self.is_symmetric() else "non-symmetric"),
            ("asymmetry", "asymmetric" if self.is_asymmetric() else "non-asymmetric"),
            ("antisymmetry", "antisymmetric" if self.is_antisymmetric() else "non-antisymmetric"),
            ("transitivity", "transitive" if self.is_transitive() else "non-transitive"),
            ("equivalency", "equivalent" if self.is_of_equivalence() else "non-equivalent"),
            ("order", "of-order" if self.is_of_order() != OrderType.not_of_order else "not-of-order"),
            ("order-strict", "strict" if self.is_of_order().is_strict() else "not-strict"),
            ("order-linearity", "linear" if self.is_of_order().is_partial() else "partial")
        ]

        if checkboxes_array[7][1] == 'not-of-order':
            checkboxes_array[8] = ("order-strict", "none")
            checkboxes_array[9] = ("order-linearity", "none")

        for item in checkboxes_array:
            res.append("%s - %s" % (item[0], item[1]))

        return res

    def task_text(self):
        """
        :rtype: str
        :return: string containing the text of the task
        """
        task_str = 'Дано множество M: '
        task_str += str(self.elements)
        task_str += ' и отношение R: '
        task_str += self.to_human_readable()
        task_str += '. Постройте матрицу смежности отношения R на множестве M и определите свойства этого отношения.'
        return task_str