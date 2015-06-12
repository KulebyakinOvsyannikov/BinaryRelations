from enum import Enum


class UnaryRelation(Enum):
    unary_not = ' not '
    unary_neutral = ' '

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

