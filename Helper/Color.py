#// LOGIC
class Color:
    """**Color** is a helper to convert colors. For now is supporting only RGB and HEX.
    
    Example of usage:
    
    >>> Color.rgb2hex(255)                  #FFFFFFFF
    >>> Color.rgb2hex(255, alpha=False)     #FFFFFF
    >>> Color.hex2rgb("FFF")                #(255, 255, 255, 255)
    >>> Color.hex2rgb("FFC04080")           #(255, 192, 64, 128)
    >>> Color.hex2rgb("FFF", alpha=False)   #(255, 255, 255)
    """
    @staticmethod
    def rgb2hex(*color: int, alpha: bool = True) -> str:
        """Convert RGB(A) decimal in hexadecimal.
        .. NOTE:: If you specified just one value, that will be treated as gray scale."""
        out: str = "#"
        # If it is just one value, use it as gray scale. (Use same value for all channels)
        if len(color) == 1: out += ("%02x" % int(color[0])) * (4 if alpha else 3)

        # If provided values are 3 or 4
        elif len(color) in [3, 4]:
            # Convert it
            for index in color: out += "%02x" % int(index)
            # In case the values are just RGB and alpha was wanted, than add it manually
            if len(color) == 3 and alpha: out += "FF"
            # In case the values contain and alpha and this was not wanted, than remove the alpha
            elif len(color) == 4 and not alpha: out = out[:-2]

        # If the statements was not reached, than raise and error message
        else: raise ValueError(f"{color} must have 1, 3 or 4 integers.")

        # Return the conversion in upper case
        return out.upper()

    @staticmethod
    def hex2rgb(color: str, alpha: bool = True) -> tuple:
        """Convert RGB(A) hexadecimal in decimal
        .. NOTE:: If you specified just one or two values, that will be treated as gray scale."""
        # Get the value with out # if is provided
        value: str = color.strip("#")
        # If alpha is wanted and not provided than add it
        if alpha: value += "F" if len(value) == 3 else "FF" if len(value) == 6 else ""
        # Size of the value
        sz = len(value)
        # Error message
        vError: str = f"Input \"#{value}\" must contain only integers and letters from A to F. (# is optional)"

        # If size is 1 or 2
        if sz in [1, 2]:
            # Convert it and multiplied 3 times (4 in case the alpha is wanted)
            try: out: tuple = tuple(int(value * (2 if sz == 1 else 1), 16) for _ in range(0, (4 if alpha else 3)))
            # Otherwise raise an error message
            except Exception: raise ValueError(vError)

        # If size of the value is 3 or 6 (4 or 8 with the alpha included)
        elif sz in [3, 4, 6, 8]:
            # If size is 3 (4 with the alpha included), duplicate the value and convert it.
            # FFF will be transformed in FFFFFF because F=15 and FF=255
            try: out: tuple = tuple(int(value[i:i + sz//3] * (2 if sz in [3, 4] else 1), 16) for i in range(0,sz,sz//3))
            # Otherwise raise an error message
            except Exception: raise ValueError(vError)

        # If the statements was not reached, than raise and error message
        else: raise IndexError(f"\"{color}\" it have {sz} characters and it must have 1 to 4, 6 or 8. (# is optional)")
        # In case the output have and the alpha included but is not wanted, than remove it
        if len(out) == 4 and not alpha: return out[:-1]
        # Otherwise return the conversion
        else: return out

