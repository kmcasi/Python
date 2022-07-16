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

The size will have different resoults base on founded libraries. What I mean is, font size will be measured by [kivy](https://kivy.org), if you do not have it then will pe measured with [pillow](https://pillow.readthedocs.io/en/stable/), if you do not have it to, then with tkinter witch is come with python by default. Pillow is the only one who messure the height base on the sample.

    myFont = Font("comic", 18)
    myFont.get_width_of("AQj")    # kivy:36, pillow:35, tkinter:40
    myFont.get_height_of("AQj")   # kivy:26, pillow:25, tkinter:27
    myFont.get_size_of("AQj")     # tuple(width, height) with the values from above

Just if is necessary you can get and change the main values of it.

    myFont._name     # 'comic'
    myFont._size     # 18

<!-- List -->
## [List](List.py)
List purpose is to return a list of elements. You can provide and unpair values like from 3 values get out 4. Are no any restriction for the amount provided values and the output ones.

Accepted values and the return type are: int, float, str, bool.

    List(3)                             # [3, 3, 3, 3]
    List(1, 2.3, _type=float)           # [1.0, 2.3, 1.0, 2.3]
    List(0.6, "a", False, _len=5)       # [1, 97, 0, 1, 97]
    List(0.3, "z", _len=2, _type=bool)  # [False, True]
    List(0.3, 2, True, "a", _type=str)  # ['0.3', '2', 'True', 'a']
