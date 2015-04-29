from enum import Enum
from .decorators import requires_int_or_bool

class BinaryRelation(Enum):
    equal = ' == '
    less_than = ' < '
    greater_than = ' > '
    less_than_or_equal = ' <= '
    greater_than_or_equal = ' >= '
    not_equal = ' != '
    logic_or = ' or '
    logic_and = ' and '
    logic_xor = ' ^ '

    @requires_int_or_bool
    def apply_binary_relation(self, value1, value2):
        """
        :rtype: bool
        :return: relation between value1 and value2 via self.value
        """
        expression = str(value1) + self.value + str(value2)
        return eval(expression)

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()