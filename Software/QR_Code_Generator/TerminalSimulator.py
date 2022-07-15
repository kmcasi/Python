# // This project require:
# // - Python 3.x
# // - colorama  (I used 0.4.3)

#// IMPORT
import os, msvcrt
try:
    from colorama import init
    from colorama import Fore as FG
except ModuleNotFoundError as e:
    import sys
    if e.path is None:
        message = "Looks like you do not have '{0}' library. " \
                  "On windows you can install it via pip: 'pip install {0}'".format("colorama")
        raise ModuleNotFoundError(message).with_traceback(sys.exc_info()[2])

#// GLOBAL VAR's
hint = f"""{FG.LIGHTCYAN_EX}>>{FG.CYAN} Type QR Code CMD {FG.GREEN}file path {FG.CYAN}or {FG.GREEN}drag and drop {FG.CYAN}it.
{FG.LIGHTCYAN_EX}>>{FG.CYAN} Type {FG.RED}help {FG.CYAN}for more informations.
"""

exceptMessage: str = f"""
{FG.LIGHTCYAN_EX}>>{FG.RED} ERROR {FG.BLUE}//{FG.YELLOW} Code nr. {FG.MAGENTA} %s {FG.LIGHTCYAN_EX}<<
>>{FG.CYAN} %s{FG.RESET}
"""

#// LOGIC
class Main:
    # Create a minimal and helpfully commands
    def Command(command:str) -> None:
        # Check starting command with out white spaces before and after the line (if they are for some strange reasons)
        check = command.strip().lower()

        # If the command is an quit wish then we will close it
        for end in ["quit", "exit"]: exit() if check == end else None

        # If is "cls" we clear the screen
        if check == "cls": os.system("CLS"); print(hint)

        # If is "help" display informations
        elif check == "help":
            dec = f"{FG.LIGHTCYAN_EX}>>"
            print(f"\n{dec}{FG.RED} INFO\n{dec}")
            print(f"{dec}{FG.MAGENTA} CLS \t\t{FG.RESET}->{FG.CYAN} Clears the screen.")
            print(f"{dec}{FG.MAGENTA} EXIT{FG.RESET}/{FG.MAGENTA}QUIT \t{FG.RESET}->{FG.CYAN} Quits the terminal.")
            print(f"{dec}{FG.MAGENTA} HELP \t{FG.RESET}->{FG.CYAN} Provides this informations.\n")

        # Otherwise try as a file
        else:
            # Check if is a file
            if os.path.isfile(command.strip()):
                # Get the base name of the file for checks
                name = os.path.basename(command.strip()).lower()
                # Check if is a CMD or BAT file
                if name.endswith(".cmd") or name.endswith(".bat"):
                    os.system("CLS")    # 1st we clear the screen
                    Main.Read(command)  # than we simulate the file content
                # Otherwise if is a file but not cmd or bat, than open that file
                else: os.system(f"START {command}")

            # If is not a file than print an error message
            else:
                msg = f"No such file or directory: {FG.MAGENTA}\"{FG.GREEN}{command}{FG.MAGENTA}\""
                print(exceptMessage % ("2", msg))


    # Read CMD/BAT file
    def Read(path:str) -> None:
        # Read the file line by line and simulate the terminal output of that line
        try:
            with open(path, "r") as file:
                line = file.readline()
                while line:
                    Main.__simulate__(line)
                    line = file.readline()
        # If file was not founded, let us to know
        except OSError as error:
            sp = str(error).split("] ")
            des = sp[1].split(": '")
            code = sp[0].split(" ")[1]
            message = f"{des[0]}: {FG.MAGENTA}\"{FG.GREEN}{des[1][:-1]}{FG.MAGENTA}\""
            print(exceptMessage % (code, message))


    # PORE terminal simulation... Just for minimal QR terminal render in case OS terminal do not support ANSI
    def __simulate__(content:str) -> None:
        # Get a temporary content
        tmp = content

        # Get just the part before input/output file
        for _ in [">", "<"]: tmp = tmp.split(_)[0].rstrip() if _ in tmp else tmp

        # Check starting command with out white spaces before and after the line
        check = tmp.strip().lower()
        # If line start with "echo" meaning will be an std::cout and now are two scenarios
        # If echo is fallowed by " " print what is after that space otherwise print a blank line
        if check.startswith("echo"): print(tmp[5:].rstrip() if tmp[4] == " " else "")
        # In case a title is provided change the terminal title
        elif check.startswith("title"): os.system(f"TITLE Simulate // {content[6:].strip()}")
        # In case the line start with "pause"
        elif check.startswith("pause"):
            # We will print default OS message in case a null point was not specified ("> NUL")
            # Pause fallowed by a null pointer cause erasing the default message (short-long story)
            print("" if ">" in content[6:] and "nul" in content[6:].lower() else "Press any key to continue...", end="")
            # And we will wait any key to be pressed
            msvcrt.getch()
        # If the line start with "exit" command, make the wish...
        elif check.startswith("exit"): exit()


#// RUN if this is the main opened file
if __name__ == "__main__":
    # Provide a default terminal title
    os.system("TITLE QR TERMINAL")

    # From windows XP and later ANSI in not included any more
    # Initialize the ANSI color support from colorama
    init(False, None, None, True)

    # Provide a hint message for the user and display it (print)
    print(hint)

    # Make a while loop
    while True:
        # For every new input make a nice and small decoration... Because why not
        print(f"{FG.LIGHTCYAN_EX}>>{FG.RESET} ", end="")
        # Check commands
        Main.Command(input())
