from .supporting_functions import modify_element
from .BinaryRelation import BinaryRelation


class RelationTriplet:
    def __init__(self, mod1, rel, mod2):
        """
        :type mod1: str
        :type rel: BinaryRelation
        :type mod2: str
        :param mod1: Modifier for first relation member
        :param rel: Relation between relation members
        :param mod2: Modifier for second relation member
        :return:
        """
        self.mod1 = mod1
        self.relation = rel
        self.mod2 = mod2

    def check(self, val1, val2):
        """
        :rtype: bool
        :type val1: int
        :type val2: int
        :param val1: first element of relation
        :param val2: second argument of relation
        :return: True, if relation between modified elements exists
        """
        elem1 = modify_element(val1, self.mod1)
        elem2 = modify_element(val2, self.mod2)
        return self.relation.apply_binary_relation(elem1, elem2)

    def convert_triplet(self):
        """
        :rtype: str
        :param triplet:
        :return: easy-to-read triplet string in "a(mod 2) < c(mod 2)" format
        """
        rt_string =''
        if self.mod1.startswith('/10'):
            rt_string+= 'a'
            aux_str = self.mod1[3:]
            if aux_str.startswith('%'):
                rt_string = rt_string + '(mod ' + aux_str[1:] + ')'
        else:
            if self.mod1.startswith('%10'):
                rt_string+='b'
                aux_str = self.mod1[3:]
                if aux_str.startswith('%'):
                    rt_string = rt_string + '(mod ' + aux_str[1:] + ')'
            else:
                rt_string+='ab'
                if self.mod1.startswith('%'):
                    rt_string = rt_string + '( ' + self.mod1[1:] + ')'

        rt_string+=self.relation.value
        if self.mod2.startswith('/10'):
            rt_string+= 'c'
            aux_str = self.mod2[3:]
            if aux_str.startswith('%'):
                rt_string = rt_string + '(mod ' + aux_str[1:] + ')'
        else:
            if self.mod2.startswith('%10'):
                rt_string+='d'
                aux_str = self.mod2[3:]
                if aux_str.startswith('%'):
                    rt_string = rt_string + '(mod ' + aux_str[1:] + ')'
            else:
                rt_string+='cd'
                if self.mod2.startswith('%'):
                    rt_string = rt_string + '( ' + self.mod2[1:] + ')'
        return rt_string

    def __str__(self):
        res = self.mod1 + str(self.relation) + self.mod2
        return res

    def __repr__(self):
        return self.__str__()