import tkinter
import tkinter as tk
from tkmacosx import Button# macos getaround for colours
from tkinter import messagebox
from tkinter.simpledialog import askinteger
import simulations
from matplotlib import pyplot as plt
import numpy as np
import os
from PIL import Image, ImageTk
from tqdm import tqdm
import pickle

width = 600
height = 800

class RuneGUI:
    def __init__(self, WIDTH, HEIGHT, queue):
        self.root = tk.Tk()

        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.minsize(WIDTH,HEIGHT)
        self.root.maxsize(WIDTH,HEIGHT)

        self.theme_data = None

        self.options = [
            "Square Random",
            "Square Uniform",
            "Circle",
            "Square Rotate",
            "Spiral",
            "System",
            "Galaxy Collision"


        ]
        self.clicked = 0

        self.current_pos = None
        self.current_vel = None
        self.pos_queue = queue

    def load_theme(self,theme):
        """
        :param theme: seperate file containg colours
        :return:
        """
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
        """
        adds all elements to screen
        :return:
        """
        self.brun = Button(self.root, text="Run Simulation(s)", bg = self.button_col, fg=self.text_col, highlightbackground = self.hover_col, highlightthickness=0.1, command=self.prepare_sims)
        self.brun.place(x =300,y = 775,anchor = tk.CENTER)

        self.clicked = tk.StringVar()
        self.clicked.set("Select Simulation")

        self.dropdown = tk.OptionMenu(self.root, self.clicked,*self.options)
        self.dropdown.configure(background=self.button_col, fg=self.text_col, activebackground=self.button_col)
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

        self.soft_lable = tk.Label(self.root, text="Use CPU (Quadtree ): ", fg=self.text_col, bg=self.button_col)
        self.soft_lable.place(x=145, y=175, anchor=tk.CENTER)

        self.check_var = tk.IntVar()
        self.softing_text = tk.Checkbutton(self.root, background=self.theme_data[0], variable=self.check_var)
        self.softing_text.place(x=300, y=175, anchor=tk.CENTER, width=150, height=25)

        self.bgen = Button(self.root, text="Generate Positions", bg=self.button_col, fg=self.text_col,
                      highlightbackground=self.hover_col, highlightthickness=0.1, command=self.position_get)
        self.bgen.place(x=300, y=300, anchor=tk.CENTER)

        # self.position_area = tk.Frame(self.root ,bg = "black", highlightbackground=self.hover_col, highlightthickness=1)
        # self.position_area.place(x = 300, y = 500, anchor=tk.CENTER, width = 300, height = 300 )

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg= "black", highlightbackground=self.hover_col, highlightthickness=1)
        self.canvas.place(x=300, y=500, anchor=tk.CENTER)

        self.bqueue = Button(self.root, text="Add To Queue", bg=self.button_col, fg=self.text_col,
                      highlightbackground=self.green_col, highlightthickness=0.1,command=self.add_queue)
        self.bqueue.place(x=300, y=700, anchor=tk.CENTER)

        self.bremove = Button(self.root, text="Remove From Queue", bg=self.button_col, fg=self.text_col,
                        highlightbackground=self.red_col, highlightthickness=0.1, command=self.remove_queue)
        self.bremove.place(x=300, y=730, anchor=tk.CENTER)

        self.view_queue = Button(self.root, text="View Queue", bg = self.button_col, fg = self.text_col,
                                 highlightbackground=self.red_col, highlightthickness=0.1, command=self.show_and_select_queue)
        self.view_queue.place(x=300,y=250, anchor=tk.CENTER)

    def get_settings(self):
        """
        gets all the data needed for simulation to be ran, however may be obselete with queueu
        :return:
        """
        sim = (self.clicked.get()) if self.clicked.get() != "Select Simulation" else None
        n = int(self.n_text.get()) if self.n_text.get() != "" and (self.int_val(self.n_text.get())) else None
        dt = float(self.dt_text.get()) if self.dt_text.get() != "" and (self.float_val(self.dt_text.get()) or self.int_val(self.dt_text.get())) else None
        g = float(self.g_text.get()) if self.g_text.get() != "" and (self.float_val(self.g_text.get()) or self.int_val(self.g_text.get())) else None
        softening = float(self.check_var.get()) if self.check_var.get() != "" and (self.float_val(self.check_var.get()) or self.int_val(self.check_var.get())) else None
        vals = [["sim", sim],["n", n],["dt",dt],["g",g],["softening", softening]]
        err = 0
        for val in vals:
            if val[1] == None:
                messagebox.showerror("Missing Value", f"Error, Incorrect Value at {val[0]}")
                err += 1
        if err > 0:
            messagebox.showerror(title="Errors",message=f"{err} Errors detected, please fix and try again" )
            return None
        else:
            return vals

    def add_queue(self):
        """
        adds current_position to queue if it exists, queue data is 2d array of pos,name,n, g, dt ,vel
        """
        if self.current_pos is not None and self.get_settings() is not None:
            self.pos_queue.enqueue([self.current_pos, self.clicked.get(), self.n_text.get(), self.g_text.get(), self.dt_text.get(), self.current_vel, self.check_var.get()])
        else:
            messagebox.showerror("No Positions", "No positions loaded avalible to be queued")
    def remove_queue(self):
        """
        checks if current position is in queue, and exists, then removes it using queue.dequeue
        """
        print("Removing")
        if self.current_pos is not None and self.pos_queue.in_queue(self.current_pos):
            self.pos_queue.dequeue(self.current_pos)
        else:
            messagebox.showerror("Error", "Select Positions Actually in queue")

    def show_and_select_queue(self):
        """
        gets dataa from the queue and displays it as seperate window,
        then adjuts the current selected position as nessecary
        """
        queue_data = self.pos_queue.return_full()
        print(queue_data)
        text = ""
        for val in queue_data:
            text += f"{val[0]}: {val[1]}  [n={val[2]}]\n"

        get_queue_value = askinteger(title="Select Queue Item", prompt =text, minvalue=1, maxvalue=len(queue_data))
        if get_queue_value: # user may not input anything
            self.current_pos = self.pos_queue.queue[get_queue_value - 1][0]
    def float_val(self, var):
        try:
            var = float(var)
            return True
        except:
            return False

    def int_val(self, var):
        try:
            if int(var):
                return True
            else: return False
        except:
            return False

    def position_get(self):
        """
            gets the details required for the inital positions to be generated
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
        elif sim =="Square Rotate":
            pos, vel = simulations.square_rotate(n)
        elif sim == "Spiral":
            pos, vel = simulations.spiral(n)
        elif sim == "System":
            pos,vel = simulations.system(n)
        elif sim == "Galaxy Collision":
            pos, vel = simulations.galaxy_collision(n)
        else:
            messagebox.showerror("WTF","how did you do that")
        self.current_pos = pos
        self.current_vel = vel
        self.position_draw(pos)


    def position_draw(self, pos):
        """
        Draws the inital positions using matplotlib, saves file to cache/figure.png

        :param pos: np.array() of the starting x,y,z,padding of the simualation
        :return: saves file at cache/figure.png
        """
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
            global image # tkphoto needs this
            image = ImageTk.PhotoImage(Image.open("cache/figure.png"))
            self.image = tk.Label(self.root, image = image,bg= "black", highlightbackground=self.hover_col, highlightthickness=1)
            self.image.place(x=300,y=500,anchor=tk.CENTER)
        # (x * 150) + 150
    def prepare_sims(self):
        if self.pos_queue.is_empty():
            pass
        else:
            i = 1
            for sim in self.pos_queue.queue:
                with open(f"cache/simulation_{i}.nbody", "wb") as file:
                    pickle.dump(sim, file)
                i+=1
        self.root.quit()
        self.root.destroy()



    def __call__(self, *args, **kwargs):
        self.load_theme("darkMode")
        self.screen_setup()
        self.root.mainloop()

if __name__ == "__main__":
    runeGui = RuneGUI(width,height)
    runeGui()

# data is from -1 to 1 x and y
# position is 1,1 top left