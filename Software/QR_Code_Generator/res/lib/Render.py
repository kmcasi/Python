#// IMPORT
import os
from res.lib.QrCode import QR, QRinfo, tk, ttk
from tkinter import colorchooser, filedialog

#// GLOBAL VAR'S
appTitle: str = "QR Code Generator"
hintText: str = "Write any message and press enter..."
previewAlpha: tuple = (0.6, 1.0)
winExist: dict = {"edit": None, "export": None, "picker": None}
theColor: list = ["#000", "black"]


#// LOGIC
class Render:
    def __init__(self, master: tk.Tk, relative: os.path):
        self.master = master
        self.cmdColorNameQR: list = ["black", "white"]
        self.cmdColorValueQR: list = ["#000", "#FFF"]
        self.cmdQR = tk.StringVar()
        self.alphaQR = tk.IntVar()
        self.alphaQR.set(0)
        self.showQR = tk.BooleanVar()

        # Main window is just for QR preview
        self.master.wm_overrideredirect(True)
        self.master.wm_geometry("+0+0")
        self.master.wm_attributes("-topmost", True)
        self.master.wm_attributes("-alpha", previewAlpha[0])

        # Initialization of the QR an pack it
        self.qr = QR(self.master)
        self.qr.pack()

        # Window initialization
        self.tool = self.__new_window_configuration__(self.master, protocol=self.__destroy__, asTool=False)

        # Create the menu bar
        self.Menu(self.tool)

        # Initialization of the text box
        self.text = self.TextBox(self.tool)
        # Also make shore the QR preview is updated with any message what is on the text box (as hint message)
        self.qr.update(self.text)

        # Set an icon for the tool window and also for the master
        # master will have an icon just for the filedialog needs...
        # The filedialog is binded with the master, and not with the tool window because will need and extra work to
        # hide the popup window. Because is just a github project I will lived like that.
        for win in [self.master, self.tool]:
            win.iconbitmap(bitmap=os.path.join(relative, "res", "icon", "QrCodeScan.ico"))

        # Final step of window initialization
        self.__new_window_configuration_final__(self.tool, 512, 256)

        # Bind's
        self.text.bind("<Return>", self.__update_qr__)
        self.tool.bind("<Enter>", self.__top_tool_ON__)
        self.tool.bind("<Leave>", self.__top_tool_OFF__)
        self.master.bind("<Enter>", self.__alpha_master_OFF__)
        self.master.bind("<Leave>", self.__alpha_master_ON__)
        self.master.bind("<Button-1>", self.__update_qr_tool__)

    def Menu(self, root: tk.Toplevel) -> None:
        """Initialisation of the menu bare in one place"""
        menuBar = tk.Menu(root)

        # File menu
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New", command=lambda: self.__menu_new__())
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=lambda: self.__destroy__())

        # Export menu
        exportMenu = tk.Menu(menuBar, tearoff=0)
        for type_ in ["PNG", "SVG", "HTML", "EPS", "XBM", "TXT", "CMD"]:
            exportMenu.add_command(label=type_, command=lambda t=type_: self.__menu_export__(t))

        # Menu primary content
        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Export", menu=exportMenu)
        menuBar.add_cascade(label="Edit", command=lambda: self.__menu_edit__())

        # Configure the root with this menu (just to avoid returning because we already asked for the root)
        root.configure(menu=menuBar)

    @staticmethod
    def TextBox(root: tk) -> tk.Text:
        """Create the text box and return a reference of it for future needs.

        Text box also include an scroll bar but we do not need a reference of it."""
        # Initialization of the needed elements for the text box
        frame = tk.Frame(root, relief="groove", bd=3)
        text = tk.Text(frame, wrap="word", bd=0)
        scroll = ttk.Scrollbar(frame, orient="vertical")

        # Pack them in a specific order
        # PS: "text" is packed at the end because will fill the remaining window space
        frame.pack(expand=True, fill="both")
        scroll.pack(fill="y", side="right")
        text.pack(expand=True, fill="both", side="left")

        # Bind the text and scroll bar together
        text.configure(yscrollcommand=scroll.set)
        scroll.configure(command=text.yview)

        # Insert a hint message on the text area
        text.insert("1.0", hintText)

        # Return a reference of the text box for future needs
        return text

    def __update_qr__(self, event) -> None:
        """To make faster the QR preview update will make an event of it.

        .. NOTE:: Will be binded on **enter** press. Technically will be binded on a new line of text."""
        self.qr.update(self.text)

    def __update_qr_tool__(self, event) -> None:
        """This will set back the normal state for the tool window in case is minimized.

        .. NOTE:: Also is calling the **__top_tool_ON__** event!"""
        self.__top_tool_ON__(event)
        if self.tool.state() == "iconic": self.tool.state("normal")

    def __top_tool_ON__(self, event) -> None:
        """Make tool window to be on top in case preview is overlapping with this."""
        self.master.wm_attributes("-topmost", False)
        self.tool.wm_attributes("-topmost", True)
        self.tool.wm_attributes("-topmost", False)

    def __top_tool_OFF__(self, event) -> None:
        """Bring back the preview on top when the user get out of tool window."""
        self.master.wm_attributes("-topmost", True)

    def __alpha_master_ON__(self, event) -> None:
        """Set the master alpha attribute to 1st value of the **previewAlpha: tuple**"""
        self.master.wm_attributes("-alpha", previewAlpha[0])

    def __alpha_master_OFF__(self, event) -> None:
        """Set the master alpha attribute to 2nd value of the **previewAlpha**: tuple."""
        self.master.wm_attributes("-alpha", previewAlpha[1])

    def __menu_new__(self) -> None:
        """This is more like an default reset. Will reset the message hint and the values from the **Edit** menu."""
        self.text.delete("1.0", "end-1c")
        self.text.insert("1.0", hintText)
        self.qr.configure(scale=5, margin=4, fg="#000", bg="#FFF", error="30%", version=None, mode=None, encoding=None)
        self.showQR.set(False)
        self.alphaQR.set(0)
        self.cmdColorNameQR = ["black", "white"]
        self.cmdColorValueQR = ["#000", "#FFF"]
        self.qr.update(self.text)
        if winExist["edit"] is not None:
            winExist["edit"].destroy()
            winExist["edit"] = None
            self.__menu_edit__()

    def __menu_edit__(self) -> None:
        """This will take care of all edit logic.

        Starting from window configuration to live QR configuration update."""
        global winExist

        # We will need a local function to be binded on window protocol when we will need to destroy it
        def _close_() -> None:
            winExist["edit"].destroy()
            winExist["edit"] = None

        # If an edit window already exit, flash it (just to avoid to many popup windows)
        if winExist["edit"] is not None: __flash__("edit")

        # Otherwise create one
        else:
            # Some local variables
            align: int = 13

            # Window initialization
            window = self.__new_window_configuration__(self.master, _close_, "Edit")

            # Window content
            general, special = tk.Frame(window), tk.Frame(window)
            # Provide a title and a separator for each area from above
            for areaName in ["General", "Special"]:
                area = eval(f"{areaName.lower()}")
                tk.Label(area, text=areaName, font=("Arial", 12, "bold")).pack(side="top")
                ttk.Separator(area, orient="horizontal").pack(fill="x", side="top", pady=3)

            # For PNG alpha case
            specialPNG = ttk.Labelframe(special, text=" PNG / HTML Alpha ")
            # Create a radio button and bind selected value to self.alphaQR
            case: list = ["Do not use", "On module", "On background"]
            for i in range(len(case)):
                tk.Radiobutton(specialPNG, text=case[i], anchor="w", value=i, variable=self.alphaQR
                               ).pack(fill="x", side="top")

            # For CMD color case
            specialCMD = ttk.Labelframe(special, text=" CMD Color ")
            self.__menu_edit_color__(specialCMD, "Module", 10, "fg", (1, 0))
            self.__menu_edit_color__(specialCMD, "Background", 10, "bg", (1, 1))

            # For general usage
            self.__menu_edit_color__(general, "Module", align, "fg")
            self.__menu_edit_color__(general, "Background", align, "bg")
            self.__menu_edit_scale__(general, "Scale", align, "scale", (1, 10))
            self.__menu_edit_scale__(general, "Margins", align, "margin", (0, 5))
            self.__menu_edit_option__(general, "Error correction", align, "error", "7%", "15%", "25%", "30%")

            # Window content pack order and configuration
            general.pack(expand=True, fill="both", side="left")
            ttk.Separator(window, orient="vertical").pack(fill="y", side="left", padx=3)
            special.pack(expand=True, fill="both", side="right")
            for sp in [specialCMD, specialPNG]: sp.pack(fill="x", side="top")
            # For showing after export
            tk.Checkbutton(special, text="Show after exporting", anchor="w", variable=self.showQR
                           ).pack(fill="x", side="top")

            # Final step of window initialization
            self.__new_window_configuration_final__(window, 352)

            # We will use this to know witch window we will need to flash if already exist one
            winExist["edit"] = window

    def __menu_edit_color__(self, root: tk, text: str, width: int, qrAttr: str, cmd: tuple = (0, 0)) -> None:
        """Create an option for changing colors.

        .. NOTE::   **text** is for description.\n
                    **qrAttr** need to be a QR self variable name as a string.\n
                    **width** is for providing a fix size because *grid* and *pack* can not be used together."""
        sample = self.qr.get(qrAttr) if cmd[0] == 0 else self.cmdColorNameQR[cmd[1]]
        # Content initialization
        frame = tk.Frame(root)
        label = tk.Label(frame, text=text, width=width, anchor="w")
        button = tk.Button(frame, bd=0, bg=sample,
                           command=lambda: self.__exec_edit_color__(root, f"Change {text} Color", button, qrAttr, cmd))

        # Content pack order and configuration
        frame.pack(fill="x", side="top")
        label.pack(side="left")
        button.pack(expand=True, fill="x", side="right")

    def __menu_edit_scale__(self, root: tk, text: str, width: int, qrAttr: str, between: tuple) -> None:
        """Create an option for changing numerical values from a slider.

        .. NOTE::   **text** is for description.\n
                    **qrAttr** need to be a QR self variable name as a string.\n
                    **between** is used as a range of allowed values.\n
                    **width** is for providing a fix size because *grid* and *pack* can not be used together."""
        # A local event used by the slider (tk.Scale)
        def _exec_(event) -> None: self.__exec_edit_qr__(qrAttr, scale.get())

        # Content initialization
        frame = tk.Frame(root)
        label = tk.Label(frame, text=text, width=width, anchor="w")
        scale = tk.Scale(frame, from_=between[0], to=between[1], orient="horizontal", tickinterval=1, command=_exec_)

        # Set the default value of the slider base of qrAttr
        scale.set(self.qr.get(qrAttr))

        # Content pack order and configuration
        frame.pack(fill="x", side="top")
        label.pack(side="left")
        scale.pack(expand=True, fill="x", side="right")

    def __menu_edit_option__(self, root: tk, text: str, width: int, qrAttr: str, *values) -> None:
        """Create an option for changing numerical values from a slider.

        .. NOTE::   **text** is for description.\n
                    **qrAttr** need to be a QR self variable name as a string.\n
                    **values** is used to fill the available options.\n
                    **width** is for providing a fix size because *grid* and *pack* can not be used together."""
        # Some local variables
        thisValue = tk.StringVar(root)
        thisValue.set(self.qr.get(qrAttr))

        # A local function used by the drop box (tk.OptionMenu)
        def _exec_(*uselessly) -> None: self.__exec_edit_qr__(qrAttr, thisValue.get())

        # Content initialization
        frame = tk.Frame(root)
        label = tk.Label(frame, text=text, width=width, anchor="w")
        option = tk.OptionMenu(frame, thisValue, *values)

        # Trace the selected value and take actions
        thisValue.trace_add("read", _exec_)

        # Content pack order and configuration
        frame.pack(fill="x", side="top")
        label.pack(side="left")
        option.pack(expand=True, fill="x", side="right")

    def __menu_export__(self, format_: str) -> None:
        """This is just a side logic for the menu export command.

        Is take care of new window logic, information and format export."""
        global winExist

        # If an export window already exit, flash it (just to avoid to many popup windows)
        if winExist["export"] is not None: __flash__("export", 2)

        # Otherwise create one
        else:
            # Some local variables
            margin: int = 5
            width: int = 352

            # Window initialization
            window = self.__new_window_configuration__(self.master, self.__menu_export_format__, f"Export as {format_}")

            # Window content
            frame = tk.Frame(window)
            frameButtons = tk.Frame(frame)
            title = tk.Label(frame, text=QRinfo(format_).Title(), font=("Arial", 14, "bold"))
            description = tk.Label(frame, text=QRinfo(format_).Description(), font=("Arial", 12),
                                   wrap=(width - margin), anchor="w", justify="left")

            # Confirmation buttons
            btnConfirm = tk.Button(frameButtons, text="OK", command=lambda: self.__menu_export_format__(format_, True))
            btnAbord = tk.Button(frameButtons, text="Cancel", command=lambda: self.__menu_export_format__())

            # Pack order
            frame.pack(expand=True, fill="both", padx=margin)
            title.pack(fill="x", side="top")
            description.pack(fill="both", side="top", pady=margin)
            frameButtons.pack(fill="x", side="bottom", pady=margin)
            # For the buttons are the same pack configuration so I will use a for loop for this
            for btn in [btnConfirm, btnAbord]: btn.pack(expand=True, fill="x", side="left")

            # Final step of window initialization
            self.__new_window_configuration_final__(window, width)

            # We will use this to know witch window we will need to flash if already exist one
            winExist["export"] = window

    def __menu_export_format__(self, format_: str = "", export: bool = False) -> None:
        """This is just an extension for the **__menu_export__**.

        In this case are 3 way's to close the window and just one of that will export the file so for that reason
        by default will just close the window.

        .. NOTE:: The idea is just to reuse same logic as much is possible."""
        global winExist

        # In case we explicit provide to export and the format is "none...", raise an error to remind about that
        if format_.strip() == "" and export:
            raise ValueError("For exporting you will need to provide and a format also...")

        # This part need to be executed just by the confirm button
        if export:
            # To get the Desktop location this will work fine for Unix, Linux and Windows
            path: os.path = os.path.join(os.path.expanduser("~"), "Desktop")

            # Ask the user where to export the QR file and under what name
            # The format asked here is the extension of the file
            # I used the "QRinfo" class just to get the name of the file
            file = filedialog.SaveAs(parent=self.master, title=f"{appTitle} // Exporting...",
                                     defaultextension=f".{format_.lower()}",
                                     filetypes=[(QRinfo(format_).Title(), f"*.{format_.lower()}")],
                                     initialdir=path, initialfil=f"QR_{format_.upper()}_Export").show()

            # Because QRCode export class have names base on extension I will let the python to execute the pattern
            if format_.lower() in ["png", "html"]: optional: str = f", {self.alphaQR.get()}"
            elif format_.lower() == "cmd": optional: str = f", [\"{self.cmdColorNameQR[0]}\", \"{self.cmdColorNameQR[1]}\"]"
            else: optional: str = ""

            if file.strip() != "": exec(f"self.qr.{format_.upper()}(\"{file}\", {self.showQR.get()}{optional})")

        # This part is common, we will need to destroy the window at the end.
        # Is same logic as on edit menu. There was just one way to close the window, here are more than one...
        winExist["export"].destroy()
        winExist["export"] = None

        # Set the tool window back on focus
        self.tool.focus_set()

    def __exec_edit_color__(self, root: tk, title: str, targetPreview: tk.Widget, qrAttr: str, cmd: tuple) -> None:
        """Function used for asking a color and updating the color on the widget.

        .. NOTE:: This is using **__exec_edit_qr__** to update the QR preview."""
        if cmd[0] == 1:
            self.__color_pick_cmd__(root, title, cmd[1])
            targetPreview.wait_variable(self.cmdQR)
            color = self.cmdQR.get()
        else:
            # Ask for the color and get just the hexadecimal value of it
            # Looks like decimal values is not so accurate, for that reason I created own conversion logic
            color = colorchooser.Chooser(parent=root, title=f"{appTitle} // {title}",
                                         initialcolor=self.qr.get(qrAttr)).show()[1]

        # If the color was provided
        if color is not None:
            # Update the target visual configuration as a sample color
            try: targetPreview.configure(bg=color)
            except Exception: pass
            # Also update the QR preview
            if cmd[0] == 0: self.__exec_edit_qr__(qrAttr, color)

    def __exec_edit_qr__(self, qrAttr: str, qrVal: type) -> None:
        """Function used for live QR preview update."""
        # Execute a configuration for the QR
        exec("self.qr.configure({}={})".format(qrAttr, f"\"{qrVal}\"" if type(qrVal) == str else qrVal))
        # And than update the QR preview
        self.qr.update(self.text)

    @staticmethod
    def __new_window_configuration__(root: tk.Tk, protocol: object, title: str = "", asTool: bool = True
                                     ) -> tk.Toplevel:
        """New window configuration splited in two parts. Created to avoid repetition.

        .. NOTE::   **protocol** need to be a function what will be used when the window is destroyed.\n
                    You need to use **__new_window_configuration_final__** after you set the window content.
        """
        # We will hide this from the beginning to avoid that python window flash glitch on random location
        window = tk.Toplevel(root)
        window.wm_attributes("-alpha", 0.0)
        window.wm_title(appTitle if title.strip() == "" else f"{appTitle} // {title}")
        window.wm_attributes("-toolwindow", asTool)
        window.wm_attributes("-topmost", True)
        window.protocol("WM_DELETE_WINDOW", protocol)
        return window

    def __new_window_configuration_final__(self, window: tk.Toplevel, width: int = 0, height: int = 0) -> None:
        """Final step for the new window configuration.

        .. NOTE::   Use this after you used **__new_window_configuration__**
                    and the window content was provided.
        """
        # After all was created, update the position to be on center, disable resize option and show the window
        window.update()
        width: int = window.winfo_width() if width <= 0 else width
        height: int = window.winfo_height() if height <= 0 else height
        center: tuple = ((self.master.winfo_screenwidth() - width) // 2,
                         (self.master.winfo_screenheight() - height) // 2)
        window.geometry(f"{width}x{height}+{center[0]}+{center[1]}")
        window.resizable(False, False)
        window.wm_attributes("-alpha", 1.0)

        # After all is done set the focus on the window (is not so important, but is a nice touch)
        window.focus_set()

    def __color_pick_cmd__(self, root: tk, title: str, index: int) -> None:
        """Color picker for CMD supported colors."""
        global winExist, theColor

        # Sample a backup color in case the selected color was not confirmed
        backupColor = self.cmdColorValueQR[index]

        # We will need a local function to be binded on window protocol when we will need to destroy it
        def _close_(final: bool = False) -> None:
            winExist["picker"].destroy()
            winExist["picker"] = None
            self.cmdQR.set(theColor[0] if final else backupColor)

        # A local function just for the buttons
        # The selected color will all ways be sampled
        def _update_(color: str = "", name: str = "", final: bool = False) -> None:
            # In case the confirmation was provided for the sample color
            if final:
                # Override the old color data with the new ones
                self.cmdColorValueQR[index] = theColor[0]
                self.cmdColorNameQR[index] = theColor[1]
                # Than close the window
                _close_(final)

            # If is not the case
            else:
                # Sample the color
                theColor[0] = color
                theColor[1] = name
                # And update the preview of selected color
                sample.configure(bg=color)

        # If an picker window already exit, flash it (just to avoid to many popup windows)
        if winExist["picker"] is not None: __flash__("picker", 2)

        # Otherwise create one
        else:
            # Some local variables
            margin: int = 3
            # For some reason blue and yellow (light ones) are inversed in terminal simulator...
            # So... Lazy fix will be to switch the names
            colorsLight: dict = {
                "light yellow": "#00F",
                "light green": "#0F0",
                "light cyan": "#0FF",
                "light red": "#F00",
                "light magenta": "#F0F",
                "light blue": "#FF0"}
            colors: dict = {
                "blue": "#000080",
                "green": "#008000",
                "cyan": "#008080",
                "red": "#800000",
                "magenta": "#800080",
                "yellow": "#808000"}
            colorsNon: dict = {
                "black": "#000",
                "dark gray": "#808080",
                "light gray": "#C0C0C0",
                "white": "#FFF"}

            # Window initioalization
            window = self.__new_window_configuration__(root, _close_, title)

            # Window content
            frameButtons = tk.Frame(window)
            buttonConfirm = tk.Button(frameButtons, text="OK", width=7, command=lambda: _update_(final=True))
            buttonAbord = tk.Button(frameButtons, text="Cancel", width=7, command=lambda: _close_())
            sample = tk.Label(frameButtons, bg=backupColor)

            # For every dictionary
            for list_ in [colorsLight, colors, colorsNon]:
                # Create a frame (every dictionary will be on one row)
                frame = tk.Frame(window)
                # For avary color name and value for the dictionary
                for name, color in list_.items():
                    # Create a button what will contain a sample of the color name and value
                    b = tk.Button(frame, width=5, bg=color, bd=0, command=lambda c=color,n=name: _update_(c, n))
                    # Configure the button
                    b.pack(side="left")
                    b.configure(height=b.winfo_width(), activebackground="tomato")
                # When one dictionary is done pack the frame
                frame.pack(fill="x", side="top")

            # Add an line separator after we finished with the colors
            ttk.Separator(window, orient="horizontal").pack(fill="x")
            # After that pack the buttons frame nad the buttons them self
            frameButtons.pack(expand=True, fill="x", side="bottom", padx=margin, pady=margin)
            for button in [buttonConfirm, sample, buttonAbord]: button.pack(expand=True, fill="x", side="left")

            # Final step of window initialization
            self.__new_window_configuration_final__(window)

            # We will use this to know witch window we will need to flash if already exist one
            winExist["picker"] = window

    def __destroy__(self) -> None:
        """For window delete protocol."""
        # In case is forced to exit and we still wait for a variable value, to prevent the background tasking we will
        # provide and value before to exit
        # self.cmdQR.set("black")
        self.cmdQR.set(self.cmdQR.get())
        self.master.destroy()


def __flash__(target: str, times: int = 1) -> None:
    """Just a flash window animation.

     .. NOTE::  **target** need to be a key of the *winExist* dictionary.\n
                **times** provide how many flash's to be."""
    # Just to make shore we will lower case the provided target... And also to avoid that ".lower()" repetition
    case = target.lower()

    # First of all we will focus the window... "focus()" and "focus_set()" is the same.
    # Even I typed more, is much more understandable of what I try to do here.
    winExist[case].focus_set()

    # Depends of how many times we want to flash the window
    for _ in range(times):
        # hide the window
        winExist[case].wm_attributes("-alpha", 0)
        # wait 100 ms
        winExist[case].after(100)
        # show the window
        winExist[case].wm_attributes("-alpha", 1)
        # and provide and sound effect also (because way not)
        winExist[case].bell()
        # and at the end wait another 50 ms before to make another flash (in case times is bigger than 1)
        winExist[case].after(50)
