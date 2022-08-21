# Python: Helper
Mixt python helper libraries.

Helper libraries base on my personal needs. Other projects of mine may rely on this libraries.

<!-- Color -->
## [Color](Color.py)
Color is a helper to convert colors. For now is supporting only RGB and HEX. If you specified just one value, that will be treated as gray scale.
[rgb2hex](Color.py#L15) accepts 1, 3 or 4 integers (RGBA).

    Color.rgb2hex(255)                  # FFFFFFFF
    Color.rgb2hex(255, alpha=False)     # FFFFFF
    Color.rgb2hex(255, 192, 64, 128)    # FFC04080

[hex2rgb](Color.py#L38) accepts 1 to 4, 6 or 8 characters (# is optional).

    Color.hex2rgb("FFF")                # (255, 255, 255, 255)
    Color.hex2rgb("FFF", alpha=False)   # (255, 255, 255)
    Color.hex2rgb("FFC04080")           # (255, 192, 64, 128)

<!-- Font -->
## [Font](Font.py)
Font main purpose is to measure the size of a font single letter. But you can measure and an entire message(string) on multi lines.

The size will have different resoults base on founded libraries. What I mean is, font size will be measured by [kivy](https://kivy.org), if you do not have it then will pe measured with [pillow](https://pillow.readthedocs.io/en/stable/), if you do not have it to, then with tkinter witch is come with python by default. Pillow is the only one who really measure the height base on the provided sample.

    myFont = Font("comic", 18)
    myFont.get_width_of("AQj")    # kivy:36, pillow:35, tkinter:40
    myFont.get_height_of("AQj")   # kivy:26, pillow:25, tkinter:27
    myFont.get_size_of("AQj")     # tuple(width, height) with the values from above

Just if is necessary you can get and change the main values of it.

    myFont._name     # 'comic'
    myFont._size     # 18

<!-- List -->
## [List](List.py)
```python3
    myList = List(*values:int|float, size:int=4, _type:type=int)
```
List purpose is to help on list common mathematical operations and comparison. 

You can provide and unpair values like from 3 values get out 4. Are no any restriction for the amount provided values and the output ones.

The mathematical operations and comparison can be done only with `int` and `float`.

It also accept `list`, `tuple`, `set` and `dict`, but the values of them must be `float` or `int`.

- Supported mathematical operations: `+`, `-`, `*`, `/`, `//`, `**`, `%`, `+=`, `-=`, `*=`, `/=`, `//=`, `**=` and `%=`.
- Supported comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`, `in` and `not in`.
- Supported extra: `len()`, `round()`, `str()`, `__int__()`, `__float__()`, `abs()`, `pow()`, `floor()`, `ceil()`, `trunc()`, `reversed()`, `-List` and `+List`.

Examples:
```python3
myList = List(3, -5, size=4, _type=int)

standard_list:list = [1, 2, 3, 4]
standard_tuple:tuple = (1, 2, 3, 4)
standard_set:set = {1, 2, 3, 4}
standard_dict:dict[str, int] = {"x":1, "y":2, "z":3, "w":4}
one_value:int = 3

print(myList)                   # [3, -5, 3, -5]
print(-myList)                  # [-3, -5, -3, -5]
print(+myList)                  # [3, 5, 3, 5]

print(myList + one_value)       # [6, -2, 6, -2]
print(myList - standard_list)   # [2, -7, 0, -9]
print(myList * standard_tuple)  # [3, -10, 9, -20]
print(myList // standard_set)   # [3, -3, 1, -2]
print(myList ** standard_dict)  # [3, 25, 27, 625]

print(myList < one_value)      # True

# Find which values are intersecting.
print(myList.intersect(standard_list))  # [3]
```
