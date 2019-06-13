# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:32:55 2019
trololo
@author: mmelkowski
"""

import tkinter as tk
import Rovers_Fonctions as RF
import time


# Start UI
# https://pythonprogramming.net/converting-tkinter-to-exe-with-cx-freeze/


class Rover_UI():
    def __init__(self):
        # Creation of main frame
        self.root = tk.Tk()
        self.root.title("Mars Rover")

        ################################# 
        #            TITLE
        ################################# 
        i = 0
        
        # Label for Title, need install lobster font
        label_Nom = tk.Label(self.root,
                             text="Mars Rover Exploration",
                             font=("Consolas", 16))
        label_Nom.grid(row=i, column=1)
        
        ################################# 
        #           START GRID
        ################################# 
        i += 1
        
        # Button for the random grid generation
        button_Gen_Grid = tk.Button(self.root,
                                    text="Press to\ngenerate a level",
                                    command=self.gen_level)
        button_Gen_Grid.grid(row=i, column=0)
        
        # Pre creation, need to now if usefull
        self.grid = []

        # Label in place of the grid to show an introduction to the player
        intro = ("\n  The Goal is send the Rover (→)  \n"
                 "  into Alpha and  Omega station  \n"
                 "  (α & Ω)\n\n"
                 "  Avoid crashing in the rocks (▄)\n"
                 "  by sending it the correct\n"
                 "  input commands (ex: MMLLM).\n")
        self.label_command = tk.Label(self.root,
                                      justify=tk.LEFT,
                                      text=intro,
                                      font=("Consolas", 10))
        self.label_command.grid(row=i, column=1)
        
        #Label containing command legend for user
        legend = ("↑: Rover - α, Ω: Stations\n"
                  "M: Forward - B: Backward\n"
                  "L: Left - R: Right\n"
                  "A: Strafe Left - E: Strafe Right\n"
                  "/!\: Rover turn in 8 directions")
        label_legend = tk.Label(self.root, text=legend)
        label_legend.grid(row=i, column=2)

        ################################# 
        #        LINE FOR COMMAND
        #################################
        i += 1
        
        # Label in front of command input
        label_command = tk.Label(self.root, text="Command Input:")
        label_command.grid(row=i, column=0)
        
        # Entry widget to store command input
        self.entree_command = tk.Entry(self.root, textvariable="", width=30)
        self.entree_command.grid(row=i, column=1)

        # Button launch rover command execution
        button_Launch = tk.Button(self.root,
                                  text=" → Launch Rover ",
                                  command=self.launch)
        button_Launch.grid(row=i, column=2)
        

        ################################# 
        #           MAINLOOP
        #################################
        self.root.mainloop()
        
    def gen_level(self, size_grid_x=7, size_grid_y=9, nb_rocks=10):
        """
        Fonction of button: button_Gen_Grid
        """
        # Create Grid
        self.grid = RF.Grid(size_grid_x, size_grid_y)
        
        self.grid.generate_level(nb_rocks)
        
        # Update the label with the generated level
        self.label_command.destroy()
        intro = RF.gen_grid(self.grid, self.grid.player[2])
        self.label_command = tk.Label(self.root,
                                      justify=tk.LEFT,
                                      text=intro,
                                      font=("Consolas", 18))
        self.label_command.grid(row=1, column=1)
        
    def launch(self):
        """
        Fonction of button: button_Gen_Grid
        """
        # Get player input command
        move = self.entree_command.get()
        
        # Init Rover
        rover = RF.Rover(self.grid,
                         self.grid.player[1],
                         self.grid.player[0],
                         self.grid.player[2],
                         move)
        
        # Execute player input command - return a list of ASCII str to print
        movement = rover.execute_instruction()
        
        # Show in label all input command
        for elt in movement:
            time.sleep(0.4)
            self.label_command.configure(text=elt)
            self.root.update_idletasks()


if __name__ == "__main__":
    Rover_UI()
        
        