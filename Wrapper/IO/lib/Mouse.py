#// IMPORT
from builtins import staticmethod
try:
    import pynput
except ModuleNotFoundError as e:
    import sys
    if e.path is None:
        message = "Looks like you do not have '{0}' library. " \
                  "On windows you can install it via pip: 'pip install {0}'".format("pynput")
        raise ModuleNotFoundError(message).with_traceback(sys.exc_info()[2])


# // LOGIC
class Mouse:
    # Local variables
    Self = pynput.mouse
    Controller = Self.Controller()
    Button = Self.Button
    Activity = Self.Listener
    DebugAvoid:bool = True
    GetPosition:list = [0, 0]

    @staticmethod
    def Action(**kwargs:any) -> None:
        """Set some actions\n
        **Examples of usage**:
            >>> Mouse.Action(press="right", release="right")
            >>> Mouse.Action(move=(10, 30))
            >>> Mouse.Action(position=(128, 256), click="left")
        :param kwargs:  Keywords and arguments.
        :return:        Nothing. Is just an execution function."""
        # Set a dictionary of some special cases
        mb:str = "Mouse.Button."
        special:dict = {
            "position": (0, "="),
            "press": (1, mb),
            "release": (1, mb),
            "click": (2, mb)
        }

        # For every keyword and his argument
        for k, a in kwargs.items():
            # Sample the argument as most default usage of his
            _this:str = f"{a}"

            # Check if the keyword is one of the mentioned special case
            if k in special:
                # If special case type is not 0 (zero) than we need to have an prefix and suffix
                context:str = "%s" if special[k][0] == 0 else "(%s)"

                # If the special case type is 2 we expect to have multiple arguments for the same keyword
                if special[k][0] == 2:
                    # In case arguments was provided as a tuple we will convert it in a list
                    # (for the seek of API consistency)
                    if type(a) == tuple: a = list(a)

                    # In this case just the first argument needs that addition as an prefix
                    a[0] = f"{special[k][1]}{a[0]}"
                    # Feed the "context" arguments as a string and remove the [] and all '
                    _this = context % str(a)[1:-1].replace("'", "")

                # Otherwise feed the "context" with special case addition before the arguments
                else: _this = context % f"{special[k][1]}{a}"

            # Than execute the keyword base on the sampled argument
            exec(f"Mouse.Controller.{k}{_this}")

    @staticmethod
    def Move(x:int, y:int, offset:bool = False) -> None:
        """Move the cursor\n
        **Examples of usage**:
            >>> Mouse.Move(256, 512)
            >>> Mouse.Move(128, 256, True)
        :param x:       The horizontal position.
        :param y:       The vertical position.
        :param offset:  Specify if is and absolute position or an offset base on the current cursor position.
        :return:        Nothing. Is just an execution function.
        """
        index:int = 0
        for i in [x, y]:
            exec(f"Mouse.GetPosition[index] {'+' if offset else ''}= i")
            index += 1
        Mouse.Action(position=tuple(Mouse.GetPosition))

    @staticmethod
    def MoveX(amount:int, offset:bool = False) -> None:
        """Move the cursor horizontally\n
        **Examples of usage**:
            >>> Mouse.MoveX(256)
            >>> Mouse.MoveX(256, True)
        :param amount:  The amount steps.
        :param offset:  Specify if is and absolute position or an offset base on the current cursor position.
        :return:        Nothing. Is just an execution function.
        """
        exec(f"Mouse.GetPosition[0] {'+' if offset else ''}= amount")
        Mouse.Action(position=tuple(Mouse.GetPosition))

    @staticmethod
    def MoveY(amount:int, offset:bool = False) -> None:
        """Move the cursor vertically\n
        **Examples of usage**:
            >>> Mouse.MoveY(256)
            >>> Mouse.MoveY(256, True)
        :param amount:  The amount steps.
        :param offset:  Specify if is and absolute position or an offset base on the current cursor position.
        :return:        Nothing. Is just an execution function.
        """
        exec(f"Mouse.GetPosition[1] {'+' if offset else ''}= amount")
        Mouse.Action(position=tuple(Mouse.GetPosition))

    @staticmethod
    def Scroll(x:int = 0, y:int = 0) -> None:
        """Set scroll amount\n
        **Examples of usage**:
            >>> Mouse.Scroll()      # Will scroll vertically 2 steps by default
            >>> Mouse.Scroll(2)     # Will scroll horizontally 2 steps
            >>> Mouse.Scroll(y=4)   # Will scroll vertically 4 steps
            >>> Mouse.Scroll(2, 4)  # Will scroll horizontally 2 steps and vertically 4 steps
        :param x:   The horizontal amount.
        :param y:   The vertical amount.
        :return:    Nothing. Is just an execution function.
        """
        Mouse.Action(scroll=(x, 2 if x==y==0 else y))

    @staticmethod
    def ScrollX(amount:int = 2) -> None:
        """Set horizontally scroll amount\n
        **Examples of usage**:
            >>> Mouse.ScrollX()      # Will scroll horizontally 2 steps by default
            >>> Mouse.ScrollX(4)     # Will scroll horizontally 4 steps
        :param amount:  The amount steps.
        :return:        Nothing. Is just an execution function.
        """
        Mouse.Action(scroll=(amount, 0))

    @staticmethod
    def ScrollY(amount:int = 2) -> None:
        """Set vertically scroll amount\n
        **Examples of usage**:
            >>> Mouse.ScrollY()      # Will scroll vertically 2 steps by default
            >>> Mouse.ScrollY(4)     # Will scroll vertically 4 steps
        :param amount:  The amount steps.
        :return:        Nothing. Is just an execution function.
        """
        Mouse.Action(scroll=(0, amount))

    @staticmethod
    def Press(button:str) -> None:
        """Press a button\n
        **Examples of usage**:
            >>> Mouse.Press("left")
        :param button:  The button as a string.
        :return:        Nothing. Is just an execution function.
        """
        Mouse.Action(press=button)

    @staticmethod
    def Release(button:str) -> None:
        """Release a button\n
        **Examples of usage**:
            >>> Mouse.Release("left")
        :param button:  The button as a string.
        :return:        Nothing. Is just an execution function.
        """
        Mouse.Action(release=button)

    @staticmethod
    def Click(button:str, count:int = 1) -> None:
        """Click a button\n
        **Examples of usage**:
            >>> Mouse.Click("left")     # Will click the left mouse button
            >>> Mouse.Click("left", 3)  # Will click the left mouse button 3 times
        :param button:  The button as a string.
        :param count:   How many times.
        :return:        Nothing. Is just an execution function.
        """
        Mouse.Action(click=[button, count])

    @staticmethod
    def DoubleClick(button:str) -> None:
        """Double click a button\n
        **Examples of usage**:
            >>> Mouse.DoubleClick("left")     # Will click the left mouse button 2 times
        :param button:  The button as a string.
        :return:        Nothing. Is just an execution function.
        """
        Mouse.Click(button, 2)

    @staticmethod
    def Start() -> None:
        """Start mouse listener\n
        **Examples of usage**:
            >>> Mouse.Start()
        :return:    Nothing. Is just an execution function.
        :exception  TypeError: If Mouse.Listen() was not call it before."""
        try: Mouse.Activity.start()
        except TypeError: raise TypeError("Maybe you forgot to use Mouse.Listen()...")
        except RuntimeError as err:
            if Mouse.DebugAvoid and str(err) == "threads can only be started once":
                print("Warning Mouse >> Listen process was already started. This one is ignored...")
            else: raise RuntimeError(err)

    @staticmethod
    def Stop() -> None:
        """Stop mouse listener\n
        **Examples of usage**:
            >>> Mouse.Stop()
        :return:    Nothing. Is just an execution function.
        :exception  TypeError: If Mouse.Listen() was not call it before."""
        try:
            if Mouse.IsRunning(): Mouse.Activity.stop()
        except TypeError: raise TypeError("Maybe you forgot to use Mouse.Listen()...")

    @staticmethod
    def Wait() -> None:
        """Wait mouse listener to become ready\n
        **Examples of usage**:
            >>> try:
            >>>     Mouse.Wait()
            >>>     print("Mouse %s listening." % "is" if Mouse.IsRunning() else "is not")
            >>> except BaseException as _BE_:
            >>>     print("Mouse exception:", _BE_)
        :return:    Nothing. Is just an execution function.
        :exception  TypeError: If Mouse.Listen() was not call it before."""
        try: Mouse.Activity.wait()
        except TypeError: raise TypeError("Maybe you forgot to use Mouse.Listen()...")

    @staticmethod
    def IsRunning() -> bool:
        """Check if the listener is running\n
        **Examples of usage**:
            >>> run_stat: str = "is" if Mouse.IsRunning() else "is not"
            >>> print(f"Mouse {run_stat} listening.")
        :return: True or False base on the case."""
        return Mouse.Activity.running

    @staticmethod
    def KeyPlus(button:Button) -> str:
        """**Examples of usage**:
            >>> def OnClick(x, y, button, pressed) -> None:
            >>>     if Mouse.KeyPlus(button) == "middle" and pressed == 1:
            >>>         print("Mouse middle button was pressed.")
            >>>     else:
            >>>         press_stat: str = "pressed" if pressed else "released"
            >>>         print(f"Mouse {press_stat}: {Mouse.KeyPlus(button)}")
        :return: The button name as string."""
        # Just for the seek of consisting API we will implement this and on mouse
        # We will use keyboard for this because "KeyCode" is a keyboard speciality.
        sample = pynput.keyboard.KeyCode(char=button).__repr__()[1:-1]

        # I'm not shore about gaming mouse's or that ones with 12-15 buttons. So will do it more safe.
        if sample.find("Button.") == 0: return sample[7:len(sample)]

        # Otherwise return the string version of the key
        return sample

    @staticmethod
    def Listen(move:object = None, click:object = None, scroll:object = None, auto_start:bool = True) -> None:
        """Provide which functions to be triggered when mouse is listen for the events\n
        **Examples of usage**:
            >>> Mouse.Listen(click=OnClick_funtion_name)
        :param move:        Function pointer of moved logic.
        :param click:       Function pointer of clicked logic.
        :param scroll:      Function pointer of scrolled logic.
        :param auto_start:  Start automatically to listen the mouse events.
        :return:            Nothing. Is just an execution function."""
        listener = pynput.mouse.Listener(on_move=move, on_click=click, on_scroll=scroll)
        Mouse.Activity = listener
        if auto_start: Mouse.Start()

