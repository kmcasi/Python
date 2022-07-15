#// This is an real example how I use it.
#//
#// So my click event of the middle mouse button is not working so I
#// set an virtual click event for that when dot key from NumPad is pressed
#// and NumPad 9 key will stop mouse and keyboard listening events.
#// 
#// On Apex Legends game, middle mouse button is hard coded to mark as favorite
#// some skins, wallpapers, music etc. So this script is running on background
#// as standalone executable when I play that game -_(*_*)_-
#// 
#// Also that is the reason why I created Keyboard and Mouse classes.
#// 
#// pynput is requred
#//     pip install pynput
#// pyperclip is required
#//     pip install pyperclip
#// 
#// colorama and progress are just for visual effects.

#// IMPORT
import time

try:
    from lib.Keyboard import Keyboard
    from lib.Mouse import Mouse
except ModuleNotFoundError as e:
    import sys
    if e.path is None:
        file = str(e.name).rsplit(".", 1)[1]
        message = f"If you downloaded the '{file}.py' from github then, " \
                  f"modify the path '{e.name}' to match your project structure.\n" \
                  f"Otherwise you can find it on: https://github.com/kmcasi/Python_Mix/blob/main/IO/lib/{file}.py"
        raise ModuleNotFoundError(message).with_traceback(sys.exc_info()[2])

try:
    from colorama import Fore as fg
    from colorama import init as cinit
    from progress.bar import IncrementalBar
except ModuleNotFoundError as e:
    import sys
    if e.path is None:
        library = str(e.name).split(".", 1)[0] if "." in e.name else e.name
        message = "Looks like you do not have '{0}' library. " \
                  "On windows you can install it via pip: 'pip install {0}'".format(library)
        raise ModuleNotFoundError(message).with_traceback(sys.exc_info()[2])


#// LOGIC
class Example:
    # Local variables
    CountFake:int = 0

    def __init__(self):
        cinit()
        self.InputEvent()

    @staticmethod
    def OnPress(key) -> None:
        if Keyboard.KeyPlus(key) == "NumPad .": Mouse.Click("middle")

    @staticmethod
    def OnRelease(key) -> None:
        if Keyboard.KeyPlus(key) == "NumPad 9":
            Keyboard.Stop()
            Mouse.Stop()

    @staticmethod
    def OnClick(x, y, button, pressed) -> None:
        if Mouse.KeyPlus(button) == "middle" and pressed == 1:
            Example.CountFake += 1
            print(f"{fg.CYAN}[ {fg.RED}FAKE {fg.YELLOW}%3s {fg.CYAN}] {fg.MAGENTA}>> {fg.WHITE}Mouse middle button "
                  f"was pressed at {fg.GREEN}{x}{fg.WHITE}x{fg.GREEN}{y}{fg.WHITE} coordinates." % Example.CountFake)

    def InputEvent(self) -> None:
        Keyboard.Listen(self.OnPress, self.OnRelease)
        Mouse.Listen(click=self.OnClick)

        try:
            Keyboard.Wait()
            Mouse.Wait()
            if self.IsRunning(): print(f"{fg.CYAN}[ {fg.YELLOW}Input is now listened {fg.CYAN}]\n")
        except Exception as ex:
            print(ex)
            time.sleep(5)

    @staticmethod
    def IsRunning() -> bool:
        return Keyboard.IsRunning() and Mouse.IsRunning()


# RUN
if __name__ == "__main__":
    test = Example()
    # Wait until no any events are listening
    while test.IsRunning(): pass

    print(f"\n{fg.CYAN}[ {fg.YELLOW}Input is {fg.RED}not {fg.YELLOW}listened any more {fg.CYAN}]{fg.LIGHTBLACK_EX}\n")

    wait:int = 5
    with IncrementalBar(f'Closing', suffix='%(remaining)ds', max=wait) as bar:
        for i in range(wait+1):
            bar.next()
            time.sleep(1)
