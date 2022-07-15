#// This project require:
#// - Python 3.x
#// - PyQRCode  (I used 1.2.1)
#// - pypng     (I used 0.0.20)

#// I worked on this small project on an old laptop and tkinter is what I can get to work on it for the UI.
#// believe me... intel pentium dual core (2.0 GHz) and hd graphics with not version number

#// IMPORT
from res.lib.Render import Render, tk, os

class Main:
    def __init__(self, master, relativ:os.path):
        self.master = master
        Render(self.master, relativ)


#// RUN
if __name__ == "__main__":
    root = tk.Tk()
    Main(root, os.path.dirname(os.path.realpath(__file__)))
    root.mainloop()
