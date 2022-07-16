#// LOGIC
class Font:
    def __init__(self, font_name:str, font_size:int):
        """**Font** main purpose is to measure the size of a font single letter.
        But you can measure and an entire message(string) on multi lines.

        Example usage:

        >>> myFont = Font("comic", 18)
        >>> myFont.get_width_of("Z")    # 13
        >>> myFont.get_height_of("Z")   # 26
        >>> myFont.get_size_of("Z")     # (13, 26)

        :param font_name:   Font name as a string
        :param font_size:   Font size as an integer
        """
        # Local variables
        self._name:str = font_name
        self._size:int = font_size

    def get_size_of(self, sample:str="W") -> tuple[int, int]:
        """Measuring the sample size.

        :param sample:  The sample as a string. Default is "W", usually is the bigger character.
        :return:        A tuple of two integers, width and height.
        """
        return self._measuring(sample)

    def get_width_of(self, sample:str="W") -> int:
        """Measuring the sample width.

        :param sample:  The sample as a string. Default is "W", usually is the bigger character.
        :return:        An integer.
        """
        return self._measuring(sample)[0]

    def get_height_of(self, sample:str="W") -> int:
        """Measuring the sample height.

        :param sample:  The sample as a string. Default is "W", usually is the bigger character.
        :return:        An integer.
        """
        return self._measuring(sample)[1]

    def _measuring(self, sample:str) -> tuple[int, int]:
        """Used internally for measuring purpose.

        Is recommended to not be used directly. Instead, use one of: get_size_of, get_width_of or get_height_of"""
        try:
            # Using kivy Label to render the sample and extracting the size of it.
            from kivy.uix.label import Label
            font = Label(text=sample, font_name=self._name, font_size=self._size)
            font.texture_update()
            return tuple(font.texture_size)
        except ModuleNotFoundError:
            try:
                # Using pillow to extract the size of it.
                from PIL import ImageFont
                font = ImageFont.truetype(self._name, self._size)
                _, descent = font.getmetrics()
                width = font.getmask(sample).getbbox()[2]
                height = font.getmask(sample).getbbox()[3] + descent
                return tuple((width, height))
            except ModuleNotFoundError:
                # Using tkinter Font to extract the size of it.
                from tkinter import Tk, Label
                from tkinter.font import Font
                root = Tk()
                font = Font(root, family=self._name, size=self._size)
                width = font.measure(sample)
                height = font.metrics("linespace", displayof=root)
                root.destroy()
                return tuple((width, height))
            except Exception as e:
                import sys
                raise Exception(e).with_traceback(sys.exc_info()[2])

