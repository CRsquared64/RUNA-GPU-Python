import tkinter as tk
from tkmacosx import Button # macos getaround for colours
width = 800
height = 800




class RuneGUI:
    def __init__(self, WIDTH, HEIGHT):
        self.root = tk.Tk()

        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.minsize(WIDTH,HEIGHT)
        self.root.maxsize(WIDTH,HEIGHT)

        self.theme_data = None

    def load_theme(self,theme):
        with open(f"themes/{theme}.theme", "r") as file:
            self.theme_data = eval(file.read())
        print(self.theme_data)
        self.root["bg"] = self.theme_data[0]
        self.button_col = self.theme_data[1]
        self.text_col = self.theme_data[2]
        self.hover_col = self.theme_data[3]

    def screen_setup(self):
        brun = Button(self.root, text="Run Simulation", bg = self.button_col, fg=self.text_col, highlightbackground = self.hover_col, highlightthickness=0.1)
        brun.place(x =400,y = 775,anchor = tk.CENTER)


    def __call__(self, *args, **kwargs):
        self.load_theme("darkMode")
        self.screen_setup()
        self.root.mainloop()

if __name__ == "__main__":
    runeGui = RuneGUI(width,height)
    runeGui()