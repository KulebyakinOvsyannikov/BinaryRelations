def requires_int_or_bool(func):
    def ints_checked(cls, arg1, arg2):
        if (type(arg1) != int and type(arg1) != bool) or \
                (type(arg2) != int and type(arg2) != bool):
            raise ValueError("Arguments are not ints or bools")
        return func(cls,arg1,arg2)
    return ints_checked


def requires_bool(func):
    def bool_checked(cls, arg):
        if type(arg) != bool:
            raise ValueError("Argument is not a boolean")
        else:
            return func(cls, arg)
    return bool_checked