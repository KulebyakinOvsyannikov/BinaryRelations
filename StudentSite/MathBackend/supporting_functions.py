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


def compose_partial_solve(requests_POST, num_of_elements):
    res_table = ""
    for i in range(0, num_of_elements):
        for j in range(0, num_of_elements):
            res_table += '+ ' if "%s-%s" % (i,j) in requests_POST else '- '
        res_table = res_table[:-1] + '$'
    res_table = res_table[:-1]

    property_fields = ["reflexivity",
                       "anti-reflexivity",
                       "symmetry",
                       "asymmetry",
                       "antisymmetry",
                       "transitivity",
                       "equivalency",
                       "order",
                       "order-strict",
                       "order-linearity"]
    res_props = ""
    for field in property_fields:
        res_props += field + '=' + (requests_POST[field] if field in requests_POST else 'none') + '$'
    return '@'.join([res_table, res_props[:-1]])