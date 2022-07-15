# // IMPORT
import os, io
import tkinter as tk
import tkinter.ttk as ttk
from pyqrcode import QRCode
from res.lib.Convert import Color


# // LOGIC
class QRinfo:
    def __init__(self, format_: str):
        self.format = format_.lower()

    def Title(self) -> str:
        out = self.format.upper()

        if self.format == "png": out = "Portable Network Graphic"
        elif self.format == "svg": out = "Scalable Vector Graphic"
        elif self.format == "html": out = "Hyper Text Markup Language"
        elif self.format == "eps": out = "Encapsulated PostScript"
        elif self.format == "xbm": out = "X BitMap"
        elif self.format == "txt": out = "Text Based"
        elif self.format == "cmd": out = "Command"
        return out

    def Description(self) -> str:
        out = ""

        if self.format == "png": out = "This will export the QR code as a portable network graphic file (image)."
        elif self.format == "svg": out = "This will export the QR code as a scalable vector using a set of paths."
        elif self.format == "html": out = "This will export the QR code as a HTML document using the PNG image " \
                                          "encoded as base64."
        elif self.format == "eps": out = "This will export the QR code an encapsulated PostScript document using " \
                                         "lines of contiguous modules." \
                                         "\n\nScale of 1 equates to a module being drawn at 1 point (1/72 of an inch)."
        elif self.format == "xbm": out = "This will export the QR code as a plain text binary image format."
        elif self.format == "txt": out = "This will export the QR code as a text file of 1’s and 0’s, with each row " \
                                         "of the code on a new line.\nThe purpose of this is to allow users to " \
                                         "create their own renderer." \
                                         "\n\n1 → represent the data module\n0 → represent the background"
        elif self.format == "cmd": out = "This will export the QR code as a command file using ANSI color escape.\n\n" \
                                         "It consists of a series of commands to be executed by the command-line " \
                                         "interpreter, stored in a plain text file."
        return out


class Common:
    def __init__(self):
        # Variables for the file destination.
        self.path: str = ""
        self.fileName: str = ""
        self.fileNameDefault: str = "QR_{TYPE}_Export"
        self.destination: str = ""
        # Variables for the QR code configuration.
        self.scale: int = 5
        self.margin: int = 4
        self.fg: str = "#000"
        self.bg: str = "#FFF"
        self.error: str = '30%'
        self.version: int = None
        self.mode: str = None
        self.encoding: str = None
        self.code: QRCode = None

    @staticmethod
    def Content(message: object) -> str:
        """Content is get any object and will return a converted string.

        .. NOTE:: If object is a tkinter **Text** or **Entry** than the content of that one will be extracted.
        """
        # Get the class type of the message object
        check = message.__class__
        # If the class type is tkinter Text/Entry than extract the content of it
        if check == tk.Text: out: str = message.get("1.0", "end")
        elif check in [tk.Entry, ttk.Entry]: out: str = message.get()
        # If is not one of that, convert it in a string (in case is not)
        else: out: str = str(message)
        # Return the string version of the message with out white spaces before and after the content
        return out.strip()


class Export(Common):
    def __init__(self):
        super().__init__()
        self.signature: str = "QRCode <https://github.com/kmcasi/Python/tree/main/Software/QR_Code_Generator>"

    def PNG(self, file: str = "", show: bool = False, alpha: int = 0) -> None:
        """**Portable Network Graphic** (PNG)

        This will export the QR code as a portable network graphic file (image).
        """
        self.__dynamic__(file, "png")
        try:
            _fg_ = (0, 0, 0, 0) if alpha == 1 else Color.hex2rgb(self.fg)
            _bg_ = (0, 0, 0, 0) if alpha == 2 else Color.hex2rgb(self.bg)
            self.code.png(self.destination, self.scale, _fg_, _bg_, self.margin)
        except Exception as e: print(e)
        finally: self.__pop_up__(show)

    def SVG(self, file: str = "", show: bool = False,
            svgClass: str = "QR", lineClass: str = "QRLine", xmlDecl: bool = True) -> None:
        """**Scalable Vector Graphic** (SVG)

        This will export the QR code as a scalable vector using a set of paths.
        """
        self.__dynamic__(file, "svg")
        try: self.code.svg(self.destination,
                           scale=self.scale, module_color=self.fg, background=self.bg, quiet_zone=self.margin,
                           svgclass=svgClass, lineclass=lineClass, xmldecl=xmlDecl, svgns=True, omithw=False)
        except Exception as e: print(e)
        finally: self.__pop_up__(show)

    def HTML(self, file: str = "", show: bool = False, alpha: int = 0) -> None:
        """**Hyper Text Markup Language** (HTML)

        This will export the QR code as a HTML document using the PNG image encoded as base64.\n
        .. NOTE:: This method depends on the **pypng** module to actually create the PNG image.
        """
        self.__dynamic__(file, "html")
        try:
            _fg_ = (0, 0, 0, 0) if alpha == 1 else Color.hex2rgb(self.fg)
            _bg_ = (0, 0, 0, 0) if alpha == 2 else Color.hex2rgb(self.bg)
            data: str = self.code.png_as_base64_str(self.scale, _fg_, _bg_, self.margin)
            with open(self.destination, "w") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head>\n\t<!-- META's -->\n\t<meta charset=\"UTF-8\" />")
                f.write("\n\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />")
                f.write(f"\n\t<meta name=\"author\" content=\"{self.signature}\" />")
                f.write("\n\t<meta name=\"description\" content=\"The QRCode in the HTML format.\" />")
                f.write("\n\t\n\t<!-- CSS Style -->\n\t<style>\n\t\timg {\n\t\t\tposition: absolute;")
                f.write("\n\t\t\ttop: 50%;\n\t\t\tleft: 50%;\n\t\t\ttransform: translate(-50%, -50%);\n\t\t}")
                f.write("\n\t</style>\n\t\n\t<title>QR HTML Preview</title>\n</head>\n\n<body>")
                f.write(f"\n\t<img src=\"data:image/png;base64,{data}\">\n\n</body>\n</html>")
        except Exception as e: print(e)
        finally: self.__pop_up__(show)

    def EPS(self, file: str = "", show: bool = False) -> None:
        """**Encapsulated PostScript** (EPS)

        This will export the QR code an encapsulated PostScript document using lines of contiguous modules.

        .. NOTE:: Scale of 1 equates to a module being drawn at 1 point (1/72 of an inch).
        """
        self.__dynamic__(file, "eps")
        try:
            epsFrom: str = "%%Creator: PyQRCode <https://pypi.python.org/pypi/PyQRCode/>"
            epsTo: str = f"%%Creator: {self.signature}"
            fileOut = io.StringIO()
            self.code.eps(fileOut, self.scale, self.fg, self.bg, self.margin)
            open(self.destination, "w").write(fileOut.getvalue().replace(epsFrom, epsTo))
        except Exception as e: print(e)
        finally: self.__pop_up__(show)

    def XBM(self, file: str = "", show: bool = False) -> None:
        """**X BitMap** (XBM)

        This will export the QR code as a plain text binary image format.
        """
        self.__dynamic__(file, "xbm")
        try: open(self.destination, "w").write(self.code.xbm(self.scale, self.margin))
        except Exception as e: print(e)
        finally: self.__pop_up__(show)

    def TXT(self, file: str = "", show: bool = False) -> None:
        """**Text Based** (TXT)

        This will export the QR code as a text file of 1’s and 0’s, with each row of the code on a new line.\n
        A data module in the QR Code is represented by a 1. Likewise, 0 is used to represent the background of the code.
        \nThe purpose of this is to allow users to create their own renderer.
        """
        self.__dynamic__(file, "txt")
        try: open(self.destination, "w").write(self.code.text(self.margin)[:-1])
        except Exception as e: print(e)
        finally: self.__pop_up__(show)

    def CMD(self, file: str = "", show: bool = False, color: list = ["black", "white"]) -> None:
        """**Command** (CMD)

        This will export the QR code as a command file using ANSI color escape.\n
        It consists of a series of commands to be executed by the command-line interpreter, stored in a plain text file.
        """
        self.__dynamic__(file, "bat" if file.lower().endswith(".bat") else "cmd")
        try:
            title: str = "QRCode Terminal Preview"
            with open(self.destination, "w") as f:
                f.write(f"@ECHO OFF\n\n:: Script created with {self.signature}\n\nTITLE {title}\n\nECHO.\nECHO ")
                f.write(self.code.terminal(color[0], color[1], self.margin)[1:-1].replace("\n", "\nECHO "))
                f.write("\nECHO.\n\nECHO Press any key to exit...\nPAUSE >NUL\nEXIT\n")
        except Exception as e: print(e)
        finally: self.__pop_up__(show)

    def __dynamic__(self, file: str, extension: str) -> None:
        """Update dynamic the destination file."""
        # If the file name is not provided than use the default one.
        self.fileName = self.fileNameDefault if file == "" else file
        # In case the name contain {TYPE}, replace that with the extension uppercase.
        if "{TYPE}" in self.fileName: self.fileName = self.fileName.replace("{TYPE}", extension.upper())
        # If the path is provided than join it otherwise destination fill be just the file name.
        self.destination = self.fileName if self.path == "" else fr"{self.path}/{self.fileName}"
        # Make shore the provided extension is the right one. Also force lower case for the extension.
        # Most of file extensions are lower case so we fallow the standard pattern.
        ext = os.path.splitext(self.destination.lower())[1]
        if ext == "" or ext != f".{extension.lower()}": self.destination += f".{extension.lower()}"

    def __pop_up__(self, explicit: bool = False) -> None:
        """Open the file exported after was created."""
        if explicit:
            if "~" in self.destination: absPath = os.path.realpath(os.path.expanduser(self.destination))
            else: absPath = os.path.realpath(self.destination)
            if os.path.isfile(absPath): os.system(f"start {absPath}")


class QR(Export):
    def __init__(self, master: tk):
        super().__init__()
        self.master = master
        self.bitmap = tk.BitmapImage()
        self.image = tk.Label(self.master)

    def update(self, message: object, preview: bool = True) -> None:
        """Update the QR code data.

        The **preview** is used to define if the preview will be updated or not.\n
        If **message** it is a class of tkinter Text/Entry, the content will be extracted,
        otherwise will be converted into a string.

        Example:
            >>> root = tkinter.Tk()
            >>> text = tkinter.Text(root)
            >>> code = QR(root)
            >>> button = tkinter.Button(root, text="Update", command=lambda:code.update(text))
            >>> code.pack()
            >>> button.pack(fill="x", side="bottom")
            >>> text.pack(expand=True, fill="both")
            >>> root.mainloop()
        """
        # Get the string version of the message
        text = self.Content(message)
        # Generate the QR code
        self.code = QRCode(text, self.error, self.version, self.mode, self.encoding)
        # Update and the preview if is wanted
        if preview: self.preview()

    def preview(self) -> None:
        """Preview is take care of update the QR preview image.

        Is used by default in **QR.update()**.

        .. NOTE:: To prevent crashes an exception message will be printed on console.
        """
        # Get the QR data as XBM type
        xbm = self.code.xbm(self.scale, self.margin)
        # Configure the bitmap
        self.bitmap.configure(data=xbm, background=self.bg, foreground=self.fg)
        # Is possible the image data type to be changed with something what do not have/support image functionality
        try: self.image.configure(image=self.bitmap)
        except Exception as e: print(e)

    def pack(self, **kwargs) -> None:
        """Pack the QR preview image in the parent/master widget.

        By default image is an **tkinter.Label**. If you want to change the image type use **QR.config()**.

        If you changed the image type, you can still use it to pack your image type or you can
        pack it externally/manually.

        .. NOTE:: To prevent crashes an exception message will be printed on console.

        Example:
            >>> root = tkinter.Tk()
            >>> code = QR(root)
            >>> button = tkinter.Button(code.master)
            >>> code.config(image=button)
            >>> code.pack(fill="x", side="top", padx=5, pady=5)
            >>> root.mainloop()
        """
        try: self.image.pack(kwargs)
        except Exception as e: print(e)

    def configure(self, **kwargs) -> None:
        """Configure the QR attributes.

        .. NOTE:: To prevent crashes an exception message will be printed on console."""
        # For all arguments provided
        for arg in kwargs:
            try:
                # Check to se if exist
                self.__getattribute__(arg)
                # And if it is, than set/change the value
                self.__setattr__(arg, kwargs[arg])
            except Exception as e: print(e)

    def get(self, attr: str) -> any:
        """Get the QR attributes."""
        return self.__getattribute__(attr)
