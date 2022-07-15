#// This is an example for both use of I/O Keyboard and Mouse

#// IMPORT
try:
    from lib.Keyboard import Keyboard
    from lib.Mouse import Mouse
except ModuleNotFoundError as e:
    import sys
    if e.path is None:
        file = str(e.name).rsplit(".", 1)[1]
        message = f"If you downloaded the '{file}.py' from github then, " \
                  f"modify the path '{e.name}' to match your project structure.\n" \
                  f"Otherwise you can find it on: https://github.com/kmcasi/Python/blob/main/Wrapper/IO/lib/{file}.py"
        raise ModuleNotFoundError(message).with_traceback(sys.exc_info()[2])


#// LOGIC
class Example:
    def __init__(self):
        self.InputEvent()

    @staticmethod
    def OnPress(key) -> None:
        """Debugging pressed event\n
        :param key: The pressed key.
        :return:    Nothing. Is just an execution function."""
        print(f"Keyboard {Keyboard.KeyPlus(key)} was pressed.")

        # Will use a try block to avoid errors for other keys what has not attribute char (eg: ctrl, esc, left,...)
        # If you want to not use try block than "key.char" need to be replaced with "Keyboard.KeyPlus(key)"
        amount: int = 2
        try:
            # Trigger mouse scroll event with w,a,s,d key press
            if key.char == "w":
                Mouse.ScrollY(amount)
            elif key.char == "s":
                Mouse.ScrollY(-amount)
            elif key.char == "a":
                Mouse.ScrollX(-amount)
            elif key.char == "d":
                Mouse.ScrollX(amount)

            # NumPad Test
            if Keyboard.KeyPlus(key) == "NumPad .": print("Dot :P")
            elif Keyboard.KeyPlus(key) == "NumPad 5": print(">> Right in center <<")
            elif Keyboard.IsNumPad(key):
                print(f"You got an {Keyboard.Self.KeyCode(char=key).__repr__()[2:-2]} just like this :))")

        # Will ignore all exceptions in this scenario
        except BaseException: pass

    @staticmethod
    def OnRelease(key) -> None:
        """Debugging pressed event\n
        :param key: The pressed key.
        :return:    Nothing. Is just an execution function."""
        print(f"Keyboard {Keyboard.KeyPlus(key)} was released.")

        # Releasing ESC will stop the listener for the keyboard and mouse as well.
        if key == Keyboard.Key.esc:
            Keyboard.Stop()
            Mouse.Stop()

    @staticmethod
    def OnMove(x, y) -> None:
        """Debugging move event\n
        :param x: The horizontal position of the cursor.
        :param y: The vertical position of the cursor.
        :return:  Nothing. Is just an execution function."""
        print(f"Mouse moved to {x}x{y}")

    @staticmethod
    def OnScroll(x, y, h, v) -> None:
        """Debugging move event\n
        :param x: The horizontal position of the cursor.
        :param y: The vertical position of the cursor.
        :param h: The horizontal amount of scroll.
        :param v: The vertical amount of scroll.
        :return:  Nothing. Is just an execution function."""
        where = "down" if v < 0 else ("left" if h < 0 else ("up" if v > 0 else "right"))
        print(f"Mouse scrolled {where}.")

    @staticmethod
    def OnClick(x, y, button, pressed) -> None:
        """Debugging move event\n
        :param x:       The horizontal position of the cursor.
        :param y:       The vertical position of the cursor.
        :param button:  The button what triggered the action.
        :param pressed: The action what was triggered by the button.
        :return:        Nothing. Is just an execution function."""
        action = "pressed" if pressed else "released"
        print(f"Mouse {Mouse.KeyPlus(button)} button was {action}.")

    def InputEvent(self) -> None:
        Keyboard.Listen(self.OnPress, self.OnRelease)
        Mouse.Listen(self.OnMove, self.OnClick, self.OnScroll)

    @staticmethod
    def IsRunning() -> bool:
        return Keyboard.IsRunning() or Mouse.IsRunning()


# Run if main file is this one
if __name__ == "__main__":
    test = Example()
    # Wait until no any events are listening
    while test.IsRunning(): pass
    print("Input events are not listened any more.")
