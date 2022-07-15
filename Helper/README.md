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

    myFont = Font("comic", 18)
    myFont.name     # 'comic'
    myFont.size     # 18

The main usage of it will have different resoults base on founded libraries. What I mean is, font size will be measured by [kivy](https://kivy.org), if you do not have it then will pe measured with [pillow](https://pillow.readthedocs.io/en/stable/), if you do not have it to, then with tkinter witch is come with python by default.

    myFont.get_width_of("Z")    # kivy:13, pillow:13, tkinter:15
    myFont.get_height_of("Z")   # kivy:26, pillow:20, tkinter:27
    myFont.get_size_of("Z")     # tuple(width, height) with the values from above
