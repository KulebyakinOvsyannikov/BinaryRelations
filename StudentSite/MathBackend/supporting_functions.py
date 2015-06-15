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

def find_minimal_element_index(fm_array, ignore=[][:]):
    for fmi in range(len(fm_array)):
        if fmi in ignore: continue
        found = True
        for fmj in range(len(fm_array)):
            if fmj in ignore: continue
            if fm_array[fmi][fmj] and fmi != fmj:
                found = False
        if found:
            return fmi
    return -1

def delete_element(ar, dind):
    ar = ar[:dind] + ar[dind + 1:]
    for dei in range(len(ar)):
        ar[dei] = ar[dei][:dind] + ar[dei][dind + 1:]
    return ar