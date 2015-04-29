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

    def __str__(self):
        res = self.mod1 + str(self.relation) + self.mod2
        return res

    def __repr__(self):
        return self.__str__()