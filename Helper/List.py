#// IMPORT
from typing import Final
from builtins import property, abs
from logging import error, warning
from sys import exit, _getframe


#// LOGIC
class List:
    def __init__(self, size:int=4, _type:type=int) -> None:
        # Private Variables
        self.size:Final[int] = size
        self.type:Final[type] = _type

        # Protected Variables
        self.__items:list[_type] = []
        self.__supportedType:list[type] = [int, float]
        self.__supportedType_text:str = ""
        self.__arrow:str = "\u279C"

        for sample in [f", {tp.__name__}" for tp in self.__supportedType]: self.__supportedType_text += sample
        tmp = self.__supportedType_text.rsplit(", ", 1)
        self.__supportedType_text = tmp[0][2:] + " or " + tmp[1]

    @property
    def value(self) -> list: return self.__items

    @value.deleter
    def value(self) -> None: self.__items.clear()

    @value.setter
    def value(self, values:list|tuple) -> None:
        self.__check_for_valid_type(self.type, "return")

        keep:bool = True
        while keep:
            for index in range(values.size if type(values) == self.__class__ else len(values)):
                value = values.value[index] if type(values) == self.__class__ else values[index]
                self.__check_for_valid_type(type(value))

                try:
                    self.__items.append(self.type(value))

                    if len(self.__items) == self.size:
                        keep = False
                        break
                except Exception as exception:
                    error(f"{self.__class__.__name__}:[{_getframe().f_code.co_name}] {self.__arrow} {exception}")

    def __len__(self) -> int: return self.size
    def __getitem__(self, index): return self.value[index]
    def __setitem__(self, index, value): self.value[index] = value

    def __contains__(self, other:list|tuple|int|float):
        if type(other) in [list, tuple]:
            for item in other:
                if item not in self.value: return False
        else:
            if other not in self.value: return False
        return True

    def __add__(self, other:list|tuple|int|float): self.__math("+=", other, "addition"); return self
    def __sub__(self, other:list|tuple|int|float): self.__math("-=", other, "subtraction"); return self
    def __mul__(self, other:list|tuple|int|float): self.__math("*=", other, "multiplication"); return self
    def __truediv__(self, other:list|tuple|int|float): self.__math("/=", other, "division"); return self
    def __floordiv__(self, other:list|tuple|int|float): self.__math("//=", other, "floor division"); return self
    def __mod__(self, other:list|tuple|int|float): self.__math("%=", other, "module"); return self

    def __pow__(self, power, modulo=None):
        try:
            for index in range(self.size):
                self.value[index] = pow(self.value[index], power, modulo)
            return self
        except ValueError as ve:
            modulus:str = ""
            if ve.args[0].endswith(" modulus"): modulus = f" ({str(modulo)})"
            warning(f"{self.__class__.__name__}:[Power] {self.__arrow} {ve.args[0].capitalize()}{modulus}.")

    def __neg__(self): return [-v for v in self.value]
    def __pos__(self): return [+v for v in self.value]
    def __abs__(self): return [abs(v) for v in self.value]
    def __floor__(self): return [self.type(float(v).__floor__()) for v in self.value]
    def __ceil__(self): return [self.type(float(v).__ceil__()) for v in self.value]
    def __trunc__(self): return [self.type(float(v).__trunc__()) for v in self.value]
    def __round__(self, n:int|None=None): return [self.type(float(v).__round__(n)) for v in self.value]
    def __reversed__(self): return [self[self.size - index - 1] for index in range(self.size)]

    def __lt__(self, other:list|tuple):
        for index in range(self.size):
            if other[index] < self.value[index]: return False
        return True

    def __gt__(self, other:list|tuple):
        for index in range(self.size):
            if other[index] > self.value[index]: return False
        return True

    def __le__(self, other:list|tuple): return self < other or self == other
    def __ge__(self, other:list|tuple): return self > other or self == other

    def __eq__(self, other:list|tuple):
        for index in range(self.size):
            if other[index] != self.value[index]: return False
        return True

    def __math(self, operation:str, other:any, info:str) -> None:
        exec(f"""
try:
    if type(other) in self._{self.__class__.__name__}__supportedType:
        for index in range(self.size): self.value[index] {operation} other
    
    else:
        size_other:int = len(other)
        
        for index in range(self.size):
            self.value[index] {operation} other[index % size_other]

except TypeError: error(f"{self.__class__.__name__}:[{info.capitalize()}] {self.__arrow} Can operate only with "
                        f"{self.__supportedType_text}.")
        """, {"self": self,
              "other": other,
              "error": error}
             )

    def __check_for_valid_type(self, value:type, prefix:str="value") -> None:
        """
        The **_check_for_valid_type** function purpose is how the name is saying, to check if value is a valid type.

        :param prefix:  Word used to describe the checked value.
        :param value:   Value type to check for.

        :raise TypeError: If the condition is not met.
        """
        if value not in self.__supportedType:
            message:str = f"The {prefix} type must be one of: {self.__supportedType_text}."
            error(f"{self.__class__.__name__}: {message}")
            exit()
