#// LOGIC
def List(*values:any, _len:int=4, _type:type=int) -> list:
    """**List** purpose is to return a list of elements.
    You can provide and unpair values like from 3 values get out 4.

    Main reason was because kivy *VariableListProperty* had not worked for me for some reasons ``\(-_-)/``.

    Accepted values and the return type are: int, float, str, bool.
    See extreme example below:

    >>> List(3)                             # [3, 3, 3, 3]
    >>> List(1, 2.3, _type=float)           # [1.0, 2.3, 1.0, 2.3]
    >>> List(0.6, "a", False, _len=5)       # [1, 97, 0, 1, 97]
    >>> List(0.3, "z", _len=2, _type=bool)  # [False, True]
    >>> List(0.3, 2, True, "a", _type=str)  # ['0.3', '2', 'True', 'a']

    :param values:  The value(s) provided.
    :param _type:   The type of list elements.
    :param _len:    The amount of list elements.
    """
    out:list = []
    keep:bool = True
    while keep:
        for index in range(len(values)):
            if _type == int and type(values[index]) is str: value = ord(values[index])
            elif _type == float and type(values[index]) is str: value = float(ord(values[index]))
            else: value = values[index]
            try:

                out.append(_type(value))

                if len(out) == _len: keep = False; break
            except Exception as e: raise Exception(e)

    return out
