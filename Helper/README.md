# Python: Helper
Mixt python helper libraries.

Helper libraries base on my personal needs. Other projects of mine may rely on this libraries.

<!-- Color -->
## [Color](Color.py)
Color is a helper to convert colors. For now is supporting only RGB and HEX.
If you specified just one value, that will be treated as gray scale.
[rgb2hex](Color.py#L15) accepts 1, 3 or 4 integers (RGBA).

    Color.rgb2hex(255)                  # FFFFFFFF
    Color.rgb2hex(255, alpha=False)     # FFFFFF
    Color.rgb2hex(255, 192, 64, 128)    # FFC04080

[hex2rgb](Color.py#L38) accepts 1 to 4, 6 or 8 characters (# is optional).

    Color.hex2rgb("FFF")                # (255, 255, 255, 255)
    Color.hex2rgb("FFF", alpha=False)   # (255, 255, 255)
    Color.hex2rgb("FFC04080")           # (255, 192, 64, 128)

