import tkinter as tk
from tkmacosx import Button # macos getaround for colours
width = 600
height = 800




class RuneGUI:
    def __init__(self, WIDTH, HEIGHT):
        self.root = tk.Tk()

        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.minsize(WIDTH,HEIGHT)
        self.root.maxsize(WIDTH,HEIGHT)

        self.theme_data = None

        self.options = [
            "Square Random",
            "Square Uniform",
            "Circle"


        ]
    def load_theme(self,theme):
        with open(f"themes/{theme}.theme", "r") as file:
            self.theme_data = eval(file.read())
        self.root["bg"] = self.theme_data[0]
        self.button_col = self.theme_data[1]
        self.text_col = self.theme_data[2]
        self.hover_col = self.theme_data[3]
        self.green_col = self.theme_data[4]
        self.yellow_col = self.theme_data[5]
        self.red_col = self.theme_data[6]

        self.root.title("RUNE")

    def show(self, label, clicked):
        label.config(text=clicked.get())

    def screen_setup(self):
        brun = Button(self.root, text="Run Simulation", bg = self.button_col, fg=self.text_col, highlightbackground = self.hover_col, highlightthickness=0.1)
        brun.place(x =300,y = 775,anchor = tk.CENTER)

        clicked = tk.StringVar()
        clicked.set("Select Simulation")

        dropdown = tk.OptionMenu(self.root, clicked,*self.options)
        dropdown.configure(background=self.button_col, activebackground=self.button_col)
        dropdown.place(x =300,y = 25,anchor = tk.CENTER)

        simulation_label = tk.Label(self.root, text="Selected Simulation: ", fg = self.text_col, bg =self.button_col)
        simulation_label.place(x =150,y = 25,anchor = tk.CENTER)

        n_label = tk.Label(self.root, text="Amount N: ", fg=self.text_col, bg=self.button_col)
        n_label.place(x=180, y=50, anchor=tk.CENTER)

        n_text = tk.Entry(self.root, bg=self.button_col)
        n_text.place(x = 300, y = 50, anchor = tk.CENTER, width = 150, height = 25)

        dt_lable = tk.Label(self.root, text="Timestep (dt): ", fg=self.text_col, bg=self.button_col)
        dt_lable.place(x=170, y=75, anchor=tk.CENTER)

        dt_text = tk.Entry(self.root, bg=self.button_col)
        dt_text.place(x=300, y=75, anchor=tk.CENTER, width=150, height=25)

        g_lable = tk.Label(self.root, text="Gravity (G): ", fg=self.text_col, bg=self.button_col)
        g_lable.place(x=180, y=100, anchor=tk.CENTER)

        g_text = tk.Entry(self.root, bg=self.button_col)
        g_text.place(x=300, y=100, anchor=tk.CENTER, width=150, height=25)

        min_dist_lable = tk.Label(self.root, text="Min Distance (Default 1): ", fg=self.text_col, bg=self.button_col)
        min_dist_lable.place(x=140, y=150, anchor=tk.CENTER)

        min_dist_lable = tk.Entry(self.root, bg=self.button_col)
        min_dist_lable.place(x=300, y=150, anchor=tk.CENTER, width=150, height=25)

        bgen = Button(self.root, text="Generate Positions", bg=self.button_col, fg=self.text_col,
                      highlightbackground=self.hover_col, highlightthickness=0.1)
        bgen.place(x=300, y=300, anchor=tk.CENTER)

        position_area = tk.Frame(self.root ,bg = "black", highlightbackground=self.hover_col, highlightthickness=1)
        position_area.place(x = 300, y = 500, anchor=tk.CENTER, width = 300, height = 300 )

        bqueue = Button(self.root, text="Add To Queue", bg=self.button_col, fg=self.text_col,
                      highlightbackground=self.green_col, highlightthickness=0.1)
        bqueue.place(x=300, y=700, anchor=tk.CENTER)

        bremove = Button(self.root, text="Remove From Queue", bg=self.button_col, fg=self.text_col,
                        highlightbackground=self.red_col, highlightthickness=0.1)
        bremove.place(x=300, y=730, anchor=tk.CENTER)

    def __call__(self, *args, **kwargs):
        self.load_theme("darkMode")
        self.screen_setup()
        self.root.mainloop()

if __name__ == "__main__":
    runeGui = RuneGUI(width,height)
    runeGui()

def linear(arr, ell):
    for element in arr:
        if element == ell:
            return True


