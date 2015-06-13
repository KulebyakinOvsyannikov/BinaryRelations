from .RelationTriplet import RelationTriplet
from .UnaryRelation import UnaryRelation
from .BinaryRelation import BinaryRelation
from.OrderType import OrderType


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

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, task_string):
        """
        :rtype : Task
        :param task_string: String in
                            "[12,14,15,26]$[%10%3| <= |/10%3]@[/10%3| >= |%10%3]$[ not ]$[ and ]$[(0, 1)]" format
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
            readable_string += '(' + self.triplets[trip_index].convert_triplet_to_human_readable() + ')'
            if parentheses_index < len(self.parenthesis):
                if trip_index == self.parenthesis[parentheses_index][1]:
                    readable_string += ')'
                    block_mod_index += 1
                    parentheses_index += 1
            if rel_index < len(self.triplets_triplets_rel):
                readable_string += self.triplets_triplets_rel[rel_index].value
                rel_index += 1
        return readable_string

    def solve(self):
        """
        :rtype: list
        :return: two-dimensional array of booleans with answers for Adjacency matrix of current Binary relation
        """
        self.results = self.check_using_human_readable()
        return self.results

    def solve_string(self):
        """
        :rtype: str
        :returns: String with a matrix of answers (+/-)
        """
        if self.results is None:
            self.solve()
        return ' '.join(["".join(['1' if item else '0' for item in row]) for row in self.results])

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
            ("order-linearity", "linear" if self.is_of_order().is_linear() else "partial")
        ]

        if checkboxes_array[7][1] == 'not-of-order':
            checkboxes_array[8] = ("order-strict", "none")
            checkboxes_array[9] = ("order-linearity", "none")

        res = []
        for item in checkboxes_array:
            res.append(item[0] + '=' + item[1])
        return ' '.join(res)

    def is_reflexive(self):
        """
        :rtype: bool
        :return: True, if binary relation is reflexive
        """
        if self.results is None:
            used_str = self.to_human_readable()
            for elem in self.elements:
                if not self.check_for_elements_human_readable(elem, elem, used_str[:]):
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
            used_str = self.to_human_readable()
            for elem in self.elements:
                if self.check_for_elements_human_readable(elem, elem, used_str[:]):
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
                    if not self.results[u][v] and self.results[u][w] and self.results[w][v]:
                        return False
        return True

    def generate_warshalls_answers_string(self):
        if self.results is None:
            self.solve()
        temp_res = list(self.results)
        for i in range(len(temp_res)):
            temp_res[i] = temp_res[i][:]

        for w in range(0, len(self.elements)):
            for u in range(0, len(self.elements)):
                for v in range(0, len(self.elements)):
                    temp_res[u][v] = temp_res[u][v] or (temp_res[u][w] and temp_res[w][v])
        res = []
        for i in range(0, len(self.elements)):
            res_row = []
            for j in range(0, len(self.elements)):
                res_row.append('+' if temp_res[i][j] else '-')
            res.append(' '.join(res_row))
        return '$'.join(res)

    def generate_warshalls_strings(self):
        res = []
        if self.results is None:
            self.solve()
        temp_res = self.results[:]
        for i in range(len(self.results)):
            temp_res[i] = temp_res[i][:]

        for w in range(0, len(self.elements)):
            step_res = ""
            for u in range(0, len(self.elements)):
                for v in range(0, len(self.elements)):
                    temp_res[u][v] = temp_res[u][v] or (temp_res[u][w] and temp_res[w][v])

                    step_res += '1' if temp_res[u][v] else '0'
                step_res += ' '
            res.append(step_res[0:-1])
        return '@'.join(res)

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
        :type sort: str
        :param sort: users sort attempt
        :return: true, is sort is a correct list of sorted indexes
        """

        if self.results is None:
            self.solve()

        sort = sort.split(' ')
        rel_array = []
        for i in range(len(sort)):
            rel_array.append([True if el=='1' else False for el in sort[i]])

        for i in range(len(self.elements)):
            for j in range(len(self.elements)):
                if self.results[i][j] and not rel_array[i][j]:
                    return False

        def find_minimal(ar):
            for fmi in range(len(ar)):
                found = True
                for fmj in range(len(ar)):
                    if rel_array[fmi][fmj] and fmi != fmj:
                        found = False
                if found:
                    return fmi
            return -1

        def delete_element(ar, dind):
            """
            :type ar: list
            """
            ar.remove(ar[dind])
            for dei in range(len(ar)):
                ar[dei].remove(ar[dei][dind])
            return ar

        while len(rel_array) > 0:
            ind = find_minimal(rel_array)
            if ind == -1:
                return False
            for i in range(len(rel_array)):
                if not (rel_array[i][ind] or i == ind):
                    return False
            rel_array = delete_element(rel_array, ind)
            print(rel_array)
        return True

    def reflexivity_highlights(self):
        highlights = {}
        if self.results is None:
            self.solve()
        for i in range(len(self.elements)):
            if self.results[i][i]:
                highlights[str(i)+'-'+str(i)] = True
            else:
                highlights[str(i)+'-'+str(i)] = False
        return highlights

    def antireflexivity_highlights(self):
        highlights = {}
        if self.results is None:
            self.solve()
        for i in range(len(self.elements)):
            if not self.results[i][i]:
                highlights[str(i)+'-'+str(i)] = True
            else:
                highlights[str(i)+'-'+str(i)] = False
        return highlights

    def symmetry_highlights(self):
        highlights = {}
        if self.results is None:
            self.solve()
        for i in range(len(self.elements)):
            for j in range(i,len(self.elements)):
                if self.results[i][j] != self.results[j][i]:
                    highlights[str(i)+'-'+str(j)] = False
                    highlights[str(j)+'-'+str(i)] = False
        return highlights

    def asymmetry_highlights(self):
        highlights = self.antisymmetry_highlights()
        for i in range(len(self.elements)):
            if self.results[i][i]:
                highlights[str(i)+'-'+str(i)] = False
        return highlights

    def antisymmetry_highlights(self):
        highlights = {}
        if self.results is None:
            self.solve()
        for i in range(len(self.elements)):
            for j in range(i+1, len(self.elements)):
                if self.results[i][j] and self.results[j][i]:
                    highlights[str(i)+'-'+str(j)] = False
                    highlights[str(j)+'-'+str(i)] = False
        return highlights

    def transitivity_highlights(self):
        highlights = {}
        if self.results is None:
            self.solve()
        for w in range(len(self.elements)):
            for i in range(len(self.elements)):
                for j in range(len(self.elements)):
                    if self.results[i][w] and self.results[w][j] and not self.results[i][j]:
                        highlights[str(i)+'-'+str(j)] = False
        return highlights

    def order_linear_highlights(self):
        highlights = {}
        if self.results is None:
            self.solve()
        for e1 in range(len(self.elements)):
            for e2 in range(e1+1,len(self.elements)):
                if not self.results[e1][e2] and not self.results[e2][e1]:
                    highlights[str(e1)+'-'+str(e2)] = False
                    highlights[str(e2)+'-'+str(e1)] = False
        return highlights

    def generate_highlights_for_demo(self):
        highlights = [self.reflexivity_highlights(),
                      self.antireflexivity_highlights(),
                      self.symmetry_highlights(),
                      self.asymmetry_highlights(),
                      self.antisymmetry_highlights(),
                      self.transitivity_highlights(),
                      [],
                      [],
                      [],
                      self.order_linear_highlights()]

        return highlights

    def warshalls_demo_strings(self):
        if self.results is None:
            self.solve()

        used_res = self.results[:]

        for i in range(len(used_res)):
            used_res[i] = used_res[i][:]

        strings = []

        for w in range(len(self.elements)):
            step_strings = []
            step = False
            for i in range(len(self.elements)):
                for j in range(len(self.elements)):
                    new_val = used_res[i][j] or (used_res[i][w] and used_res[w][j])
                    if new_val != used_res[i][j]:
                        used_res[i][j] = new_val
                        step = True
                        step_strings.append("<div style='block'>Существует отношение между элементами {e1} и {through}, {through} и {e2}, "
                                       "но не существует отношения между элементами {e1} и {e2}, поэтому ставим 1 в "
                                       "матрице смежности между этими элементами</div>".format(e1=self.elements[i],
                                                                                         e2=self.elements[j],
                                                                                         through=self.elements[w]))
            if not step:
                step_strings.append("<div style='block'>Нет таких элементов, отношение между которыми существовало бы через элемент {}, но не"
                               "существовало бы прямого отношения.</div>".format(self.elements[w]))
            strings.append(''.join(step_strings))
        return strings

    def generate_topological_tips(self):
        tips = []
        solve = self.topological_sort()
        if solve is not None:
            for i in range(len(solve)):
                tip = "<div style='display:block'>Находим, что {0} является минимальным элементом.</div> " \
                      "<div style='display:block'>Выделяем строку и столбец данного элемента в матрице.</div>" \
                      "<div style='display:block'>Отмечаем отношения от всех невычекнутых элементов к выделенному</div>" \
                      "<div style='display:block'>Вычеркиваем элемент {0}.".format(self.elements[solve[i]])
                tips.append(tip)
        return tips

    def generate_demo_strings(self):
        res = []
        human_readable = self.to_human_readable()
        for elem in self.elements:
            for elem2 in self.elements:
                if self.check_for_elements_human_readable(elem, elem2, human_readable[:]):
                    #append_str = self.string_for_elements(human_readable, elem, elem2)
                    append_str = "\nВидим, что они состоят в отношении R. Ставим единицу в соответствующий элемент матрицы."
                else:
                    #append_str = self.string_for_elements(human_readable, elem, elem2)
                    append_str = "\nВидим, что они не состоят в отношении R. Оставляем соответствующий элемент " \
                                 "матрицы нетронутым."
                res.append("Подставляем элементы {} и {} в отношение.\n {} \n {}".format(
                    elem, elem2, self.string_for_elements(human_readable, elem, elem2), append_str
                ))
        checkboxes_array = [
            ("Рефлексивность", "из заполненной матрицы смежности видим, что отношение"
                               " рефлексивно." if self.is_reflexive() else "из заполненной матрицы смежности видим, "
                                                                           "что отношение нерефлексивно."),
            ("Антирефлексивность", "при этом оно антирефлексивно." if self.is_antireflexive() else
                                    "при этом оно не антирефлексивно."),
            ("Симметричность", "из симметричности матрицы видим, что отношение симметрично."
                    if self.is_symmetric() else "из несимметричности матрицы видим, что отношение несимметрично"),
            ("Асимметрия", "видно, что ни одна пара элементов не входит."
                           " в отношение с симметричной ей; значит, отношение асимметрично."
                             if self.is_asymmetric() else "видим, что по крайней мере одна пара входит в отношение с "
                                                        "симметричной ей, следственно, отношение не асимметрично."),
            ("Антисимметричность", "если и выолняется условие xRy и yRx, это значит"
                                   ", что x=y, следственно, отношение антисимметрично."
                        if self.is_antisymmetric() else "по крайней мере одна пара состоит в отношении с "
                                                        "симметричной ей, следственно, отношение не антисимметрично."),
            ("Транзитивность", "выолняется условие xRy, yRc => xRc, что значит - отношение транзитивно."
                                if self.is_transitive() else "не выолняется условие xRy, yRc => xRc, что значит - "
                                                             "отношение не транзитивно."),
            ("Эквивалентность", "так как выполняются условия рефлексивности, симметричности и транзитивности"
                                ", делаем вывод, что отношение является отношением эквивалентности"
                if self.is_of_equivalence() else "так как не выполняется по крайней мере одно из условий "
                                        "(рефлексивность, симметричность, транзитивность), делаем вывод, что"
                                        " отношение не является отношением эквивалентности."),
            ("Отношение порядка", "данное отношение -- отношение порядка"
                if self.is_of_order() != OrderType.not_of_order else "данное отношение не является отношением порядка."),
            ("Строгость порядок", "отношение является отношением строгого порядка"
                                ", так как выполняются условия (асимметричности и транзитивности."
            if self.is_of_order().is_strict() else "отношение является отношением нестрогого порядка, так как "
                                            "выполняются условия рефлексивности, антисимметричности и транзитивноси"),
            ("Линейность порядка", "отношение является отношением линейного порядка, "
                                   "так как для каждого xRy не выполняется yRx"
                if self.is_of_order().is_linear() else "отношение является отношением частичного порядка, так как "
                                                       "по крайней мере для одной пары элементов не выполняется ни "
                                                       "xRy, ни yRx.")
        ]

        if checkboxes_array[7][1] == 'данное отношение не является отношением порядка.':
            checkboxes_array.pop()
            checkboxes_array.pop()

        for elem in checkboxes_array:
            res.append(elem[0]+' : '+elem[1])

        for elem in self.warshalls_demo_strings():
            res.append(elem)

        for item in self.generate_topological_tips():
            res.append(item)

        return res, self.generate_highlights_for_demo()


    def task_text(self):
        """
        :rtype: str
        :return: string containing the text of the task
        """
        task_str = 'Дано множество M: '
        task_str += str(self.elements)
        task_str += ' и отношение R: '
        task_str += self.to_human_readable()
        task_str += '. Постройте матрицу смежности отношения R на множестве M.'
        return task_str

    def properties_text(self):
        return 'Отметьте свойсва, присущеие отношению {} на множетстве {}'.format(self.to_human_readable(),
                                                                                  self.elements)

    def warshalls_text(self):
        return 'Произведите транзитивное замыкание отношения {} на множестве {}'.format(self.to_human_readable(),
                                                                                        self.elements)

    def topological_text(self):
        return 'Проследуйте по шагам топологической сортировки для отношения {} на множетсве {}'.format(
            self.to_human_readable(),
            self.elements
        )

    def is_interesting_task(self):
        if self.results is None:
            self.solve()
        nice_count = 0
        for row in self.results:
            for item in row:
                if item:
                    nice_count += 1

        if not 0.15 <= nice_count / (len(self.results) ** 2) <= 0.8:
            return False

        nice_count = 0

        if self.is_reflexive():
            nice_count += 1
        if self.is_antireflexive():
            nice_count += 1
        if self.is_symmetric():
            nice_count += 1
        if self.is_asymmetric():
            nice_count += 1
        if self.is_antisymmetric():
            nice_count += 1
        if self.is_transitive():
            nice_count += 1
        if self.is_of_equivalence():
            nice_count += 1
        if self.is_of_order() != OrderType.not_of_order:
            nice_count += 1

        if nice_count >= 2:
            return True
        return False

    def check_for_elements_human_readable(self, e1, e2, string=None):
        if string is None:
            string = self.to_human_readable()
        return eval(self.string_for_elements(string[:], e1, e2))

    def check_using_human_readable(self):
        strin = self.to_human_readable()
        result = []
        for elem1 in self.elements:
            row_result = []
            for elem2 in self.elements:
                row_result.append(self.check_for_elements_human_readable(elem1, elem2, strin))
            result.append(row_result)
        return result

    @staticmethod
    def string_for_elements(used_str, e1, e2):
        used_str = used_str.replace('ab', e1.__str__())
        used_str = used_str.replace('cd', e2.__str__())
        used_str = used_str.replace('mod', '%')
        used_str = used_str.replace('b', (e1 % 10).__str__())
        used_str = used_str.replace('c', (e2 // 10).__str__())
        i = 0
        while i < len(used_str) - 1:
            if used_str[i] == 'a' and used_str[i+1] != 'n':
                used_str = used_str[0:i] + (e1 // 10).__str__() + used_str[i+1:]
            if used_str[i] == 'd' and used_str[i-1] != 'n':
                used_str = used_str[0:i] + (e2 % 10).__str__() + used_str[i+1:]
            if used_str[i] == '!' and used_str[i+1] != '=':
                used_str = used_str[0:i] + 'not ' + used_str[i+1:]
            i += 1

        return used_str
