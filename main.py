import gui
import simulations
import queue

WIDTH, HEIGHT = 600, 800
position_queue = queue.Queue()
RuneApp = gui.RuneGUI(WIDTH, HEIGHT, position_queue)
RuneApp()
