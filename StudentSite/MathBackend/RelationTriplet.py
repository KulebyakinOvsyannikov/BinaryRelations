from .supporting_functions import modify_element

class RelationTriplet:
    def __init__(self, mod1, rel, mod2):
        self.mod1 = mod1  # String
        self.relation = rel  # BinaryRelation
        self.mod2 = mod2  # String

    def check(self, val1, val2):
        elem1 = modify_element(val1, self.mod1)
        elem2 = modify_element(val2, self.mod2)
        return self.relation.apply_binary_relation(elem1, elem2)

    def __str__(self):
        res = self.mod1 + self.relation.value + self.mod2
        return res

    def __repr__(self):
        return self.__str__()