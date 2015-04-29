from .decorators import requires_bool
from enum import Enum


class UnaryRelation(Enum):
    unary_not = ' not '
    unary_neutral = ' '

    @requires_bool
    def apply_unary_relation(self, argument):
        """
        :rtype: bool
        :param argument: boolean to apply unary operation to
        :return: argument itself
        """
        if self == UnaryRelation.unary_not:
            return not argument
        else:
            return argument

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

