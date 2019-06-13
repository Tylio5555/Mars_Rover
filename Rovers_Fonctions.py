# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:32:55 2019

@author: mmelkowski
"""


import random
import time


class Rover:
    def __init__(self, grid, x, y, o, i):
        self.grid_obj = grid
        self.grid = grid.grid
        self.x = int(x)
        self.y = int(y)

        self.orientation = o
        self.instruction = i

        self.right_dict = {"N": "NE", "NE": "E", "E": "SE", "SE": "S",
                           "S": "SW", "SW": "W", "W": "NW", "NW": "N"}

        self.left_dict = {"N": "NW", "NW": "W", "W": "SW", "SW": "S",
                          "S": "SE", "SE": "E", "E": "NE", "NE": "N"}

        self.movement_dict = {"N":(0,1), "S":(0,-1), "E":(1,0), "W":(-1,0),
                              "NW":(-1,1), "NE":(1,1), "SW":(-1,-1), "SE":(1,-1)}

        #for printing
        self.rover_look_dict = {"N": "↑", "NE": "↗", "E": "→", "SE": "↘",
                                "S": "↓", "SW": "↙", "W": "←", "NW": "↖"}
        self.rover_look = self.rover_look_dict[self.orientation]

        self.block = "░"
        self.rock = "▄"

        self.block_dict = {"O": self.block,
                           "R": self.rock,
                           "P": self.rover_look_dict[self.orientation],
                           "E": "Ω",
                           "A": "α"}

        self.instruction_dict = {"L": self.turn_left,
                                 "R": self.turn_right,
                                 "M": self.move_forward,
                                 "B": self.move_backward,
                                 "A": self.strafe_left,
                                 "E": self.strafe_right}

        self.has_alpha = False
        self.has_omega = False

    def turn_right(self):
        # commande = R
        self.orientation = self.right_dict[self.orientation]
        self.rover_look = self.rover_look_dict[self.orientation]

    def turn_left(self):
        # commande = L
        self.orientation = self.left_dict[self.orientation]
        self.rover_look = self.rover_look_dict[self.orientation]

    def move_direct(self, vector_x, vector_y):
        old = (self.x, self.y)
        self.x += vector_x
        self.y += vector_y
        new = (self.x, self.y)
        if (new[1], new[0]) in self.grid_obj.list_rocks:
            return True
        elif (new[1], new[0]) == self.grid_obj.pos_alpha:
            self.has_alpha = True
            self.actualise_grid_player_pos(old, new)
        elif (new[1], new[0]) == self.grid_obj.pos_omega:
            self.has_omega = True
            self.actualise_grid_player_pos(old, new)
        else:
            self.actualise_grid_player_pos(old, new)
        return False

    def move_forward(self):
        # commande = M
        vector_x, vector_y = self.movement_dict[self.orientation]
        return self.move_direct(vector_x, vector_y)

    def move_backward(self):
        # commande = B
        vector_x, vector_y = self.movement_dict[self.orientation]
        return self.move_direct(vector_x*-1, vector_y*-1)

    def strafe_left(self):
        # commande = A
        orient = self.left_dict[self.left_dict[self.orientation]]
        vector_x, vector_y = self.movement_dict[orient]
        return self.move_direct(vector_x, vector_y)

    def strafe_right(self):
        # commande = E
        orient = self.right_dict[self.right_dict[self.orientation]]
        vector_x, vector_y = self.movement_dict[orient]
        return self.move_direct(vector_x, vector_y)

    def actualise_grid_player_pos(self, old, new):
        self.grid[old[1]][old[0]] = "O"
        self.grid[new[1]][new[0]] = "P"

    def generate_text_to_pr(self):
        # https://en.wikipedia.org/wiki/Box-drawing_character

        pr_grid = []
        block_dict = {"O": self.block,
                      "R": self.rock,
                      "P": self.rover_look_dict[self.orientation],
                      "E": "Ω",
                      "A": "α"}

        pr_grid = []
        for line in self.grid[::-1]:  # need to reverse since python count
            for elt in line:
                pr_grid.append(block_dict[elt])
            pr_grid.append("\n")

        return "".join(pr_grid)

    def print_grid(self):
        print(self.generate_text_to_pr())
        time.sleep(0.8)

    def print_position(self):
        print (self.x, self.y, self.orientation)

    def execute_instruction(self):
        #path = []
        if self.instruction:
            for elt in self.instruction:
                elt = elt.upper()

                try:
                    to_end = self.instruction_dict[elt]()
                except KeyError:
                    print ("Incorrect instruction value in",
                           self.instruction,":",elt)

                if to_end:
                    yield  ("\n\n   ERROR: Transmission Failed.   "
                            "\n\n       Rover has crashed.     \n\n")

                elif (self.has_alpha and self.has_omega):
                    yield("\n\n   Rover passed both stations.   "
                          "\n\n    The mission is a success!   \n\n")

                else:
                    yield self.generate_text_to_pr()


class Grid():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.list_block = []
        self.list_rocks = []
        self.pos_alpha = []
        self.pos_omega = []

        self.generate_grid()

    def generate_grid(self):
        block = "O"
        grid = []
        for i in range (self.x):
            line = []
            for j in range(self.y):
                line.append(block)
            grid.append(line)
        self.grid = grid

    def place_char(self, x, y, char):
        if (x,y) not in self.list_block:
            self.grid[x][y] = char
            self.list_block.append((x,y))
        else: print("Block already in this position")

    def choose_random_pos(self):
        pos = (random.randint(0,self.x-1),
               random.randint(0,self.y-1))
        while pos in self.list_block:
            pos = (random.randint(0,self.x-1),
                   random.randint(0,self.y-1))
        return pos

    def generate_level(self, nb_rocks):
        # Pos Omega
        self.pos_omega = self.choose_random_pos()
        self.place_char(self.pos_omega[0], self.pos_omega[1], "E")

        # Pos Alpha
        self.pos_alpha = self.choose_random_pos()
        self.place_char(self.pos_alpha[0], self.pos_alpha[1], "A")

        # Pos Rocks
        for _ in range(nb_rocks):
            pos_rock = self.choose_random_pos()
            self.list_rocks.append(pos_rock)
            self.place_char(pos_rock[0], pos_rock[1], "R")

        # Pos Player
        self.pos_player = self.choose_random_pos()
        orient_player = random.choice(["N", "E", "S", "W"])
        self.place_char(self.pos_player[0], self.pos_player[1], "P")

        #self.player is meant to be passed in rover class
        self.player = (self.pos_player[0],
                       self.pos_player[1],
                       orient_player)

    def return_grid(self):
        return self.grid


def gen_grid(grid, orient):
    grid = grid.grid
    rover_look_dict = {"N": "↑", "NE": "↗", "E": "→", "SE": "↘",
                       "S": "↓", "SW": "↙", "W": "←", "NW": "↖"}
    block = "░"
    rock = "▄"

    block_dict = {"O": block, "R": rock, "P": rover_look_dict[orient],
                  "E": "Ω", "A": "α"}

    pr_grid = []
    for line in grid[::-1]:  # need to reverse since python count
        for elt in line:
            pr_grid.append(block_dict[elt])
        pr_grid.append("\n")

    return "".join(pr_grid)
