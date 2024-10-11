import tkinter as tk
from tkmacosx import Button# macos getaround for colours
from tkinter import messagebox
import simulations
from matplotlib import pyplot as plt
import numpy as np
import os
from PIL import Image, ImageTk
from tqdm import tqdm
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
        self.clicked = 0

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
        self.brun = Button(self.root, text="Run Simulation(s)", bg = self.button_col, fg=self.text_col, highlightbackground = self.hover_col, highlightthickness=0.1, command=self.get_settings)
        self.brun.place(x =300,y = 775,anchor = tk.CENTER)

        self.clicked = tk.StringVar()
        self.clicked.set("Select Simulation")

        self.dropdown = tk.OptionMenu(self.root, self.clicked,*self.options)
        self.dropdown.configure(background=self.button_col, activebackground=self.button_col)
        self.dropdown.place(x =300,y = 25,anchor = tk.CENTER)

        self.simulation_label = tk.Label(self.root, text="Selected Simulation: ", fg = self.text_col, bg =self.button_col)
        self.simulation_label.place(x =150,y = 25,anchor = tk.CENTER)

        self.n_label = tk.Label(self.root, text="Amount N: ", fg=self.text_col, bg=self.button_col)
        self.n_label.place(x=180, y=75, anchor=tk.CENTER)

        self.n_text = tk.Entry(self.root, bg=self.button_col)
        self.n_text.place(x = 300, y = 75, anchor = tk.CENTER, width = 150, height = 25)

        self.dt_lable = tk.Label(self.root, text="Timestep (dt): ", fg=self.text_col, bg=self.button_col)
        self.dt_lable.place(x=170, y=100, anchor=tk.CENTER)

        self.dt_text = tk.Entry(self.root, bg=self.button_col)
        self.dt_text.place(x=300, y=100, anchor=tk.CENTER, width=150, height=25)

        self.g_lable = tk.Label(self.root, text="Gravity (G): ", fg=self.text_col, bg=self.button_col)
        self.g_lable.place(x=180, y=125, anchor=tk.CENTER)

        self.g_text = tk.Entry(self.root, bg=self.button_col)
        self.g_text.place(x=300, y=125, anchor=tk.CENTER, width=150, height=25)

        self.min_dist_lable = tk.Label(self.root, text="Min Distance (Default 1): ", fg=self.text_col, bg=self.button_col)
        self.min_dist_lable.place(x=140, y=175, anchor=tk.CENTER)

        self.min_dist_text = tk.Entry(self.root, bg=self.button_col)
        self.min_dist_text.place(x=300, y=175, anchor=tk.CENTER, width=150, height=25)

        self.bgen = Button(self.root, text="Generate Positions", bg=self.button_col, fg=self.text_col,
                      highlightbackground=self.hover_col, highlightthickness=0.1, command=self.position_get)
        self.bgen.place(x=300, y=300, anchor=tk.CENTER)

        # self.position_area = tk.Frame(self.root ,bg = "black", highlightbackground=self.hover_col, highlightthickness=1)
        # self.position_area.place(x = 300, y = 500, anchor=tk.CENTER, width = 300, height = 300 )

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg= "black", highlightbackground=self.hover_col, highlightthickness=1)
        self.canvas.place(x=300, y=500, anchor=tk.CENTER)

        self.bqueue = Button(self.root, text="Add To Queue", bg=self.button_col, fg=self.text_col,
                      highlightbackground=self.green_col, highlightthickness=0.1)
        self.bqueue.place(x=300, y=700, anchor=tk.CENTER)

        self.bremove = Button(self.root, text="Remove From Queue", bg=self.button_col, fg=self.text_col,
                        highlightbackground=self.red_col, highlightthickness=0.1)
        self.bremove.place(x=300, y=730, anchor=tk.CENTER)


    def get_settings(self):
        sim = self.clicked.get() if self.clicked.get() != "Select Simulation" else None
        n = self.n_text.get() if self.n_text.get() != "" and self.float_val(self.n_text.get()) else None
        dt = self.dt_text.get() if self.dt_text.get() != "" and self.float_val(self.dt_text.get()) else None
        g = self.g_text.get() if self.g_text.get() != "" and self.float_val(self.g_text.get()) else None
        min_dist = self.min_dist_text.get() if self.min_dist_text.get() != "" and self.float_val(self.min_dist_text.get()) else None
        vals = [["sim", sim],["n", n],["dt",dt],["g",g],["min_Dist", min_dist]]
        for val in vals:
            if val[1] == None:
                messagebox.showerror("Missing Value", f"Error, Incorrect Value at {val[0]}")

    def float_val(self, var):
        return isinstance(var, float)

    def position_get(self):
        """
            "Square Random",
            "Square Uniform",
            "Circle"
        """
        sim = self.clicked.get() if self.clicked.get() != "Select Simulation" else None
        n = int(self.n_text.get()) if self.n_text.get() != "" else None
        vals = [["sim", sim], ["n", n]]
        for val in vals:
            if val[1] == None:
                messagebox.showerror("Missing Value", f"Error, Incorrect Value at {val[0]}")
        if sim == "Square Random":
            pos,vel = simulations.square(n)
        elif sim == "Square Uniform":
            pos, vel = simulations.uniform_square(n)
        elif sim == "Circle":
            pos,vel = simulations.circle(n)
        else:
            messagebox.showerror("WTF","how did you do that")

        self.position_draw(pos)

    def position_draw(self, pos):
        x_arr = []
        y_arr = []
        fig = plt.figure(frameon=False,figsize=(3,3))
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        with tqdm(total=len(pos)) as pbar:
            for position in pos:
                x = (position[0] * 150) + 150
                y = (position[1] * 150) + 150
                x_arr.append(x)
                y_arr.append(y)
                pbar.update(1)
        x = np.array(x_arr)
        y = np.array(y_arr)
        plt.scatter(x,y,s=1,color='white')
        plt.gca().set_facecolor("black")
        fig.savefig("cache/figure.png")
        print("Generated Figure")

        if os.path.isfile("cache/figure.png"):
            global image
            image = ImageTk.PhotoImage(Image.open("cache/figure.png"))
            self.image = tk.Label(self.root, image = image,bg= "black", highlightbackground=self.hover_col, highlightthickness=1)
            self.image.place(x=300,y=500,anchor=tk.CENTER)
        # (x * 150) + 150


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


# data is from -1 to 1 x and y
# position is 1,1 top left