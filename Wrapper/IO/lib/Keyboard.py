#// IMPORT
from builtins import staticmethod
import time
try:  
    import pynput, pyperclip
except ModuleNotFoundError as e:
    import sys
    if e.path is None:
        library = str(e.name).split(".", 1)[0] if "." in e.name else e.name
        message = "Looks like you do not have '{0}' library. " \
                  "On windows you can install it via pip: 'pip install {0}'".format(library)
        raise ModuleNotFoundError(message).with_traceback(sys.exc_info()[2])


# // LOGIC
class Keyboard:
    # Local variables
    Self = pynput.keyboard
    Controller = Self.Controller()
    Key = Self.Key
    Activity = Self.Listener
    DebugAvoid:bool = True

    @staticmethod
    def Action(**kwargs:str) -> None:
        """Set some actions\n
        **Examples of usage**:
            >>> Keyboard.Action(type="Hello World!", tap="enter")
            >>> Keyboard.Action(press="a", release="a")
            >>> Keyboard.Action(tap="enter")
        :param kwargs:  Keywords and arguments.
        :return:        Nothing. Is just an execution function."""
        # Set a list of some special cases
        special:list = ["press", "release", "tap"]
        control:dict = {
            "\n": "enter",
            "\r": "enter",
            "\t": "tab"
        }

        # For every keyword and his argument
        for k, a in kwargs.items():
            # Sample the argument as most default usage of his
            _this:str = f"'{a}'"

            # Check if the keyword is one of the mentioned special case
            if k in special:
                # If the provided argument is a name of a key than sample it as key (eg: alt, cmd, ctrl_r, tab,...)
                if len(a) > 1: _this = f"Keyboard.Key.{a}"
                else:
                    if a in control.keys(): _this = f"Keyboard.Key.{control[a]}"

            # Than execute the keyword base on the sampled argument
            exec(f"Keyboard.Controller.{k}({_this})")

    @staticmethod
    def Press(key:str) -> None:
        """Press a key\n
        **Examples of usage**:
            >>> Keyboard.Press("enter")
        :param key:     The key as a string.
        :return:        Nothing. Is just an execution function."""
        Keyboard.Action(press=key)

    @staticmethod
    def Release(key:str) -> None:
        """Release a key\n
        **Examples of usage**:
            >>> Keyboard.Release("enter")
        :param key:     The key as a string.
        :return:        Nothing. Is just an execution function."""
        Keyboard.Action(release=key)

    @staticmethod
    def Tap(key:str) -> None:
        """Tap a key (pressing and after that releasing)\n
        **Examples of usage**:
            >>> Keyboard.Tap("enter")
        :param key:     The key as a string.
        :return:        Nothing. Is just an execution function."""
        Keyboard.Action(tap=key)

    @staticmethod
    def Write(message:str, delay:float = 0) -> None:
        """Write a message\n
        .. NOTE::
            > backslash followed by 'n' or 'r' will be replacet with enter key\n
            > backslash followed by 't' will be replacet with tab key
        **Examples of usage**:
            >>> Keyboard.Write("Hello World!")
            >>> Keyboard.Write("Message:\\n\\tHello\\n\\tWorld!\\r")
        :param message:  The content to be written.
        :param delay:    Delay per character in seconds.
        :return:        Nothing. Is just an execution function."""
        # If the delay is equal with 0 (zero) we type as fast as possible (base on pynput speed amount)
        if delay == 0:
            Keyboard.Action(type=f"''{message}''")

        # If the delay is bigger then 0 (zero) we wait that amount of time before to tap another character
        elif delay > 0:
            for letter in message:
                time.sleep(delay)
                Keyboard.Tap(letter)

        # Other wise delay is negative amount so we consider is instant and we use clipboard as a short cut (CTRL+C/V)
        else:
            pyperclip.copy(message)
            Keyboard.Action(press="ctrl_r", tap="v", release="ctrl_r")

    @staticmethod
    def Start() -> None:
        """Start keyboard listener\n
        **Examples of usage**:
            >>> Keyboard.Start()
        :return:    Nothing. Is just an execution function.
        :exception  TypeError: If Keyboard.Listen() was not call it before."""
        try: Keyboard.Activity.start()
        except TypeError: raise TypeError("Maybe you forgot to use Keyboard.Listen()...")
        except RuntimeError as err:
            if Keyboard.DebugAvoid and str(err) == "threads can only be started once":
                print("Warning Keyboard >> Listen process was already started. This one is ignored...")
            else: raise RuntimeError(err)

    @staticmethod
    def Stop() -> None:
        """Stop keyboard listener\n
        **Examples of usage**:
            >>> Keyboard.Stop()
        :return:    Nothing. Is just an execution function.
        :exception  TypeError: If Keyboard.Listen() was not call it before."""
        try:
            if Keyboard.IsRunning(): Keyboard.Activity.stop()
        except TypeError: raise TypeError("Maybe you forgot to use Keyboard.Listen()...")

    @staticmethod
    def Wait() -> None:
        """Wait keyboard listener to become ready\n
        **Examples of usage**:
            >>> try:
            >>>     Keyboard.Wait()
            >>>     print("Keyboard %s listening." % "is" if Keyboard.IsRunning() else "is not")
            >>> except BaseException as _BE_:
            >>>     print("Keyboard exception:", _BE_)
        :return:    Nothing. Is just an execution function.
        :exception  TypeError: If Keyboard.Listen() was not call it before."""
        try: Keyboard.Activity.wait()
        except TypeError: raise TypeError("Maybe you forgot to use Keyboard.Listen()...")

    @staticmethod
    def IsRunning() -> bool:
        """Check if the listener is running\n
        **Examples of usage**:
            >>> run_stat: str = "is" if Keyboard.IsRunning() else "is not"
            >>> print(f"Keyboard {run_stat} listening.")
        :return: True or False base on the case."""
        return Keyboard.Activity.running

    @staticmethod
    def IsNumPad(key:Key) -> bool:
        """Check if the key is a NumPad one\n
        **Examples of usage**:
            >>> def OnPress(key) -> None:
            >>>     if Keyboard.IsNumPad(key):
            >>>         print(f"NumPad key was pressed: {Keyboard.KeyPlus(key)}")
        :return: True or False base on the case."""
        # Get the string version of the key
        sample = Keyboard.Self.KeyCode(char=key).__repr__()[1:-1]

        # If the sample is starting with <
        if sample.find("<") == 0:
            # Remove first and last character and update the sample as an integer
            sample = int(sample[1:-1])
            # Return if sample is one of the NumPad key code
            return sample in range(96, 106) or sample == 110

        # Otherwise is not a NumPad key so return false
        return False

    @staticmethod
    def KeyPlus(key:Key) -> str:
        """.. NOTE::
            > Is also checking if the key is a NamPad one.\n
            > You will need to be explicit about keys name if you have two versions of it.\n
            eg: "ctrl" is nor recognized. Need to be "ctrl_l" or "ctrl_r".
        **Examples of usage**:
            >>> def OnPress(key) -> None:
            >>>     if Keyboard.KeyPlus(key) == "enter":
            >>>         Keyboard.Write("Hello World!\\n")
            >>>     else:
            >>>         print(f"Keyboard pressed: {Keyboard.KeyPlus(key)}")
        :return: The key name as string."""
        # Set a list of some special cases
        nk:str = "NumPad "
        special:dict = {
            "96": f"{nk}0",    "97": f"{nk}1",
            "98": f"{nk}2",    "99": f"{nk}3",
            "100": f"{nk}4",   "101": f"{nk}5",
            "102": f"{nk}6",   "103": f"{nk}7",
            "104": f"{nk}8",   "105": f"{nk}9",
            "110": f"{nk}.",
            "\"\\'\"": "\'",
            "\\'\"\\'": "\"",
            "'\\\\\\\\'": "\\"
        }
        # Get the string version of the key
        sample = Keyboard.Self.KeyCode(char=key).__repr__()[1:-1]

        # If the sample is starting with < remove it (also from the back)
        if sample.find("<") == 0: sample = sample[1:-1]

        # Return the value if sample is one of the special keys
        if sample in special.keys(): return special[sample]

        # Remove also some other string additions
        elif sample.find("'\\\\x") == 0: return sample[2:-1]
        elif sample.find("'") == 0: return sample[1:-1]
        elif sample.find("Key.") == 0: return sample[4:]

        # Otherwise return the string version of the key
        return sample

    @staticmethod
    def Listen(press:object = None, release:object = None, auto_start:bool = True) -> None:
        """Provide which functions to be triggered when keyboard is listen for the events\n
        **Examples of usage**:
            >>> Keyboard.Listen(release=OnRelease_funtion_name)
        :param press:       Function pointer of pressed logic.
        :param release:     Function pointer of released logic.
        :param auto_start:  Start automatically to listen the keyboard events.
        :return:            Nothing. Is just an execution function."""
        listener = Keyboard.Self.Listener(on_press=press, on_release=release)
        Keyboard.Activity = listener
        if auto_start: Keyboard.Start()

