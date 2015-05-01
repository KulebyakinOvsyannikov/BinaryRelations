from enum import Enum


class OrderType(Enum):
    strict_and_linear = 'Strict Linear Order'
    strict_and_partial = 'Strict Partial Order'
    not_strict_and_linear = 'Not Strict Linear Order'
    not_strict_and_partial = 'Not Strict Partial Order'
    not_of_order = 'Not Order'

    def is_strict(self):
        """
        :rtype: bool
        :return: True, if relation is of strict order
        """
        return self == OrderType.strict_and_linear or self == OrderType.strict_and_partial

    def is_not_strict(self):
        """
        :rtype: bool
        :return: True, if relation is not of strict order
        """
        return self == OrderType.not_strict_and_linear or self == OrderType.not_strict_and_partial

    def is_linear(self):
        """
        :rtype: bool
        :return: True, if relation is linear
        """
        return self == OrderType.strict_and_linear or self == OrderType.not_strict_and_linear

    def is_partial(self):
        """
        :rtype: bool
        :return: True, if relation is partial
        """
        return self == OrderType.not_strict_and_partial or self == OrderType.strict_and_partial

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()
