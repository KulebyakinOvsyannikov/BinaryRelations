from enum import Enum
class OrderType(Enum):
    strict_and_linear = 'Strict Linear Order'
    strict_and_partial = 'Strict Partial Order'
    not_strict_and_linear = 'Not Strict Linear Order'
    not_strict_and_partial = 'Not Strict Partial Order'
    not_of_order = 'Not Order'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()
