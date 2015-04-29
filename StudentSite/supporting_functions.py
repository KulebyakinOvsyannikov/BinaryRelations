from .math_backend import BinaryRelation, RelationTriplet

def convert_triplet(triplet):
    """
    :rtype: str
    :param triplet:
    :return: easy-to-read triplet string in "a(mod 2) < c(mod 2)" format
    """
    rt_string =''
    if triplet.mod1.startswith('/10'):
        rt_string+= 'a'
        aux_str = triplet.mod1[3:]
        if aux_str.startswith('%'):
            rt_string = rt_string + '(mod ' + aux_str[-1] + ')'
    else:
        if triplet.mod1.startswith('%10'):
            rt_string+='b'
            aux_str = triplet.mod1[3:]
            if aux_str.startswith('%'):
                rt_string = rt_string + '(mod ' + aux_str[-1] + ')'
        else:
            rt_string+='ab'

    rt_string+=triplet.relation.value
    if triplet.mod2.startswith('/10'):
        rt_string+= 'c'
        aux_str = triplet.mod2[3:]
        if aux_str.startswith('%'):
            rt_string = rt_string + '(mod ' + aux_str[-1] + ')'
    else:
        if triplet.mod2.startswith('%10'):
            rt_string+='d'
            aux_str = triplet.mod2[3:]
            if aux_str.startswith('%'):
                rt_string = rt_string + '(mod ' + aux_str[-1] + ')'
        else:
            rt_string+='cd'
    return rt_string
