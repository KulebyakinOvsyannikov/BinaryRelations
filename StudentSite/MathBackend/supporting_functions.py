from math import trunc


def modify_element(element, modifier):
    """
    :rtype: int
    :param element: integer to be modified
    :param modifier: string with modifying expression (e.g. "/10 % 3")
    :return: modified integer
    """
    expression = str(element) + modifier
    return trunc(eval(expression))