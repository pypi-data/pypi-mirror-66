#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implémentation du jeu Tetris

    Usage:

    >>> from tetris_game import TetrisGame
    >>> TetrisGame()
"""

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

import random
import time
import csv
import os.path

from tetris_game.constantes import *

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

__all__ = ['Square', 'Line', 'Shape', 'Menu', 'TetrisFrame', 'TetrisGame']

class Square:
    photo_name = BRICK_IMG

    def __init__(self, col, line, canvas, parent):
        self.canvas = canvas
        self.parent = parent
        self.x = col
        self.y = line
        if self.x == 0 or self.x == 11 or self.y == 20:
            self.color = "red"
            self.is_occuped = True
            self.img = PhotoImage(file=Square.photo_name)
            self.dessin = self.canvas.create_image(40*col+1,
                                                   40*line+1,
                                                   anchor='nw',
                                                   image=self.img)
        else:
            self.color = "gray"
            self.is_occuped = False
            self.dessin = self.canvas.create_rectangle(40*col + 1,
                                                       40*line + 1,
                                                       40+(40*col)-1,
                                                       40+(40*line)-1,
                                                       fill=self.color)
            self.img = None

        # self.temp_coord_label = self.canvas.create_text((40*col + 21 , 40*line + 21 ), text="({},{})".format(self.x,self.y))

    def __repr__(self):
        return "{}".format('*' if self.is_occuped else '0')

    def toogleColor(self, occupied=True, color="gray"):
        self.canvas.itemconfig(self.dessin, fill = color)
        self.is_occuped = occupied
        return True

    def updateLabel(self):
        self.canvas.itemconfigure(self.temp_coord_label, text="({},{})".format(self.x,self.y))

    def clean(self):
        self.canvas.delete(self.parent, self.dessin)
        #self.canvas.delete(self.parent, self.temp_coord_label)
        del self.img

    def moveSquare(self, dY):
        self.y += dY
        self.canvas.move(self.dessin, 0, 40 * dY)
        #self.canvas.move(self.temp_coord_label, 0, 40 * dY)
        #self.updateLabel()

class Line:
    def __init__(self, y, canvas, parent, is_protected = False):
        self.canvas = canvas
        self.parent = parent
        self.y = y
        self.square_list = []
        self.is_protected = is_protected
        for x in range(0,12,1):
            self.square_list.append(Square(x, self.y, self.canvas, self.parent))

    def __repr__(self):
        return str([(1 if x.is_occuped else 0) for x in self.square_list]) + str(self.y)

    def binLine(self):
        #Return the int representation of the list
        bin = 0
        for index, x in enumerate(self.square_list[::-1]):
            bin += (2**index if x.is_occuped else 0)
        return bin

    def isLoose(self):
        start, *line, end = [x.is_occuped for x in self.square_list]
        return any(line)

    def lineFull(self):
        return all([x.is_occuped for x in self.square_list])

    def moveLine(self, dY):
        self.y += dY
        for square in self.square_list:
            square.moveSquare(dY)

    def clean(self):
        for square in self.square_list :
            square.clean()
            del(square)

class Shape:
    def __init__(self, shape, rotation, shape_color, col, line):
        self.shape_type = shape
        self.shape_rotation = rotation
        self.shape = SHAPES[shape][rotation]
        self.color = shape_color
        self.col = col
        self.line = line

    def canMoveShape(self, dX, dY, playground, rotate = False):
        #catching the shape :
        if not rotate :
            shape = self.shape
        else :
            shape = SHAPES[self.shape_type][(self.shape_rotation +1)%4]
        #Vérifier que l'on peut descendre
        #Construire les 4 lignes correspondantes au shape, et leur index
        table = []
        for y_temp in range(0,4):
            line = []
            for x_temp in range(0,12):
                line.append(0)
            table.append(line)

        for y_temp in range(len(shape)):
            for x_temp in range(len(shape[y_temp])):
                if x_temp + self.col + dX < len(table[y_temp]):
                    table[y_temp][x_temp + self.col + dX] = shape[y_temp][x_temp]


        for y in range(0, 4):
            bin_table = 0
            for index, x in enumerate(table[y][::-1]):
                bin_table+= x*2**index
            table[y]= bin_table
        #Here table contains 4 lines with the new position of the shape as int
        #Here we don't care about Y cause we are going to test it after
        table_compare = []
        if self.line + dY < 0 :
            for index in range(self.line + dY, 0):
                table_compare.append(0b100000000001)

        for line in playground[max(self.line + dY,0) : self.line + dY + 4]:
            table_compare.append(line.binLine())

        #Completing the table to ensure that we have 4 lines
        if len(table_compare) < 4 :
            for index in range(4-len(table_compare), 5):
                table_compare.append(0b100000000001)

        #Here we have to tables :
        #1) table -> It's a table of four rows with the desired position of the shape
        #2) table_compare -> It's a table of four rows with the current content of the playground
        for y in range(0, 4):
            #We use the bit/bit & to check if there is a collision :
            # "100001" & "000100" => False
            # "100101" & "000100" => True -> Collision, so return False because we can't move
            if (table[y] & table_compare[y]) :
                return False
        return True

    def rotateShape(self):
        self.shape = SHAPES[self.shape_type][(self.shape_rotation +1)%4]
        self.shape_rotation += 1

    def drawShape(self, playground, dessin = True):
        for line_number, line in enumerate(self.shape) :
            for col_number, col in enumerate(line) :
                if self.shape[line_number][col_number] and line_number + self.line >=0 and col_number + self.col>= 0 :
                    if dessin :
                        playground[line_number + self.line].square_list[col_number + self.col].toogleColor(occupied=False, color=self.color)
                    else :
                        playground[line_number + self.line].square_list[col_number + self.col].toogleColor(occupied=False)

    def lockShape(self, playground):
        for line_number, line in enumerate(self.shape) :
            for col_number, col in enumerate(line) :
                if self.shape[line_number][col_number] and line_number + self.line >=0 and col_number + self.col>= 0 :
                    playground[line_number + self.line].square_list[col_number + self.col].toogleColor(occupied=True, color=self.color)

class Menu:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = Canvas(self.parent, bg="black", height=600, width=300, bd=0, highlightthickness=0)
        self.canvas.place(x=480, y=0)

        #Creating th futur shape array
        self.canvas.create_text(150,40,fill="red",font="Cambria 50 bold underline", text="Next")
        self.future_shape_array = []
        for y in range(0,6):
            line = []
            for x in range(0,6):
                self.canvas.create_rectangle(30+40*x + 1, 80+40*y + 1, 70+(40*x)-1, 120+(40*y)-1, fill="gray")
                if 0<x<5:
                    line.append(self.canvas.create_rectangle(30+40*x + 1, 80+40*y + 1, 70+(40*x)-1, 120+(40*y)-1, fill="gray"))
            if 0<y<5 :
                self.future_shape_array.append(line)

        #Addind the highest score
        self.load_score()
        self.canvas.create_text(150, 350, fill="red", font="Cambria 15 bold underline", text="Highest score")
        self.highest_score_label = self.canvas.create_text(150, 380 , fill="white", font="Cambria 20 italic", text=format(self.high_score,",").replace(",", " "))
        #Adding the current score
        self.current_score = 0
        self.canvas.create_text(150, 410, fill="red", font="Cambria 15 bold underline", text="Current score")
        self.current_score_label = self.canvas.create_text(150, 440 , fill="white", font="Cambria 20 italic", text=format(self.current_score,",").replace(",", " "))

        #Adding the number of line
        self.number_line = 0
        self.canvas.create_text(80, 480, fill="red", font="Cambria 15 bold underline", text="Lignes : ")
        self.lignes_label = self.canvas.create_text(150, 480, fill="white", font="Cambria 15 bold italic", text=str(self.number_line))


        #Adding the current level
        self.level_label = self.canvas.create_text(150, 540, fill="white", font="Cambria 25 bold italic", text="Level 1")

        #initing pygame and song playing
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        self.main_sound = pygame.mixer.Sound(MAIN_SONG)
        self.wall_sound = pygame.mixer.Sound(WALL_SONG)
        self.line_sound = pygame.mixer.Sound(LINE_SONG)
        self.loose_sound = pygame.mixer.Sound(LOOSE_SONG)
        self.level_up_sound = pygame.mixer.Sound(LEVEL_UP_SONG)
        self.list_song=[self.main_sound, self.wall_sound, self.line_sound, self.loose_sound, self.level_up_sound]
        self.change_volume('50')
        self.main_sound.play(-1)

        #Adding the volume control
        self.volume_canvas = Canvas(self.parent, bg="red", height=240, width=300, bd=0, highlightthickness=0)
        self.volume_canvas.place(x=480, y=600)
        self.volume_var =IntVar()
        self.volume_control = Scale(self.volume_canvas, orient='horizontal',
        from_=0, to=100,resolution=1, tickinterval=10, length=250,
        label='Volume (%)', variable=self.volume_var, command=self.change_volume)
        self.volume_control.set(50)
        self.volume_control.place(x=22,y=40)

    def increase_line_level(self, nb_line, current_level):
        self.number_line += nb_line
        self.canvas.itemconfigure(self.lignes_label, text=str(self.number_line))
        level = self.number_line//10 + 1
        self.canvas.itemconfigure(self.level_label, text="Level " + str(level))
        level_speed = LEVELS[min(level, 20)]
        if level != current_level :
            self.level_up_sound.play()
        return level_speed, level

    def change_volume(self, volume_var):
        for sound in self.list_song :
            sound.set_volume(int(volume_var)/100)

    def stop_music(self):
        for sound in self.list_song :
            sound.stop()

    def update_future_shape(self, shape, color):
        for index_line, line in enumerate(self.future_shape_array):
            for index_col, col in enumerate(line) :
                if shape[index_line][index_col] :
                    self.canvas.itemconfig(self.future_shape_array[index_line][index_col], fill = color)
                else :
                    self.canvas.itemconfig(self.future_shape_array[index_line][index_col], fill = "gray")

    def load_score(self):
        if not os.path.isfile(SCORE_FILE) :
            f = open(SCORE_FILE, "w")
            f.close()

        self.score_list = []
        with open(SCORE_FILE) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader :
                self.score_list=row
        self.score_list = [int(x) for x in self.score_list]
        self.high_score = int(max(self.score_list or [0]))

    def update_score(self, delta):
        self.current_score += delta
        self.canvas.itemconfigure(self.current_score_label, text=format(self.current_score,",").replace(",", " "))
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.canvas.itemconfigure(self.highest_score_label, text=format(self.high_score,",").replace(",", " "))

    def save_score(self):
        self.score_list.append(self.current_score)
        with open(SCORE_FILE, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(self.score_list)
        return True

class TetrisFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self)
        self.parent = parent
        self.parent.geometry("780x840")
        self.parent.title("Tetris")
        self.parent.protocol("WM_DELETE_WINDOW",self.onClose)

        #PlayGround Canvas
        self.canvas = Canvas(self.parent, bg="black", height=840, width=480, bd=0, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        #Creating playground as a grid
        self.playground = []
        for y in range(0, 21, 1):
            self.playground.append(Line(y, self.canvas, self.parent, is_protected = (True if y == 20 else False)))

        #Shapes containers:
        self.moving_shape = None
        self.future_shape = None

        #Adding the first Shape and the first future one
        self.moving_shape = self.getRandomShape()
        self.future_shape = self.getRandomShape()

        #Binding Keys
        self.parent.bind("<Any-KeyPress>", self.onKeypress)

        #initing the menu panel
        self.menu = Menu(self.parent)
        self.menu.update_future_shape(self.future_shape.shape, self.future_shape.color)
        self.current_speed, self.current_level = self.menu.increase_line_level(0, 0)
        self.animate()

    def onKeypress(self, event):
        if event.keysym == "Down":
            self.autoDecreaseShape()
        elif event.keysym == "Left":
            if self.moving_shape.canMoveShape(-1, 0, self.playground):
                self.moving_shape.drawShape(self.playground, dessin = False)
                self.moving_shape.col -=1
                self.moving_shape.drawShape(self.playground, dessin = True)
            else :
                self.menu.wall_sound.play()
        elif event.keysym == "Right":
            if self.moving_shape.canMoveShape(1, 0, self.playground):
                self.moving_shape.drawShape(self.playground, dessin = False)
                self.moving_shape.col +=1
                self.moving_shape.drawShape(self.playground, dessin = True)
            else :
                self.menu.wall_sound.play()
        elif event.keysym == "space":
            if self.moving_shape.canMoveShape(0, 0, self.playground, rotate = True):
                self.moving_shape.drawShape(self.playground, dessin = False)
                self.moving_shape.rotateShape()
                self.moving_shape.drawShape(self.playground, dessin = True)
            else :
                self.menu.wall_sound.play()

    def animate(self):
        self.cleanPlayground()
        if self.playground[0].isLoose() :
            self.gameLoose()
        else :
            self.autoDecreaseShape()
            self.master.after(self.current_speed, self.animate)

    def gameLoose(self):
        self.menu.save_score()
        self.menu.main_sound.stop()
        self.menu.loose_sound.play()
        if messagebox.askquestion ('You loose...','Want to play again ?',icon = 'question') == 'yes':
            for widget in self.parent.winfo_children():
                widget.destroy()
            del self.menu
            self.__init__(self.parent)
        else:
            messagebox.showinfo('Goodbye !','Thanks for playing Tetris ! Hope to see you soon !')
            self.parent.destroy()

    def autoDecreaseShape(self):
        if self.moving_shape.canMoveShape(0, 1, self.playground):
            self.moving_shape.drawShape(self.playground, dessin = False)
            self.moving_shape.line +=1
            self.moving_shape.drawShape(self.playground, dessin = True)
        else :
            self.moving_shape.lockShape(self.playground)
            self.moving_shape, self.future_shape = self.future_shape, self.getRandomShape()
            self.menu.update_future_shape(self.future_shape.shape, self.future_shape.color)

    def getRandomShape(self):
        shape_type, shape_positions = random.choice(list(SHAPES.items()))
        shape_position = random.randint(0, len(shape_positions)-1)
        shape_color =  random.choice(COLORS)
        return Shape(shape_type, shape_position, shape_color, col=3, line=-4)

    def cleanPlayground(self):
        index_to_remove = []
        for index, line in enumerate(self.playground):
            if line.lineFull() and not line.is_protected :
                index_to_remove.append(line)

        if index_to_remove:
            nb_lines = len(index_to_remove)
            self.menu.line_sound.play()
            if nb_lines == 4:
                delta = 1200 * self.current_level
            elif nb_lines == 3:
                delta = 300 * self.current_level
            elif nb_lines == 2:
                delta = 100 * self.current_level
            else:
                delta = 40 * self.current_level
            self.menu.update_score(delta)
            self.current_speed, self.current_level = self.menu.increase_line_level(nb_lines, self.current_level)
        for line_to_del in index_to_remove :
            self.playground.remove(line_to_del)
            self.playground = [Line(0, self.canvas, self.parent)] + self.playground
            line_to_del.clean()
            del(line_to_del)


        for num_line in range(0,20):
            if self.playground[num_line].y != num_line :
                #Move the line with num_line - y
                self.playground[num_line].moveLine(num_line -self.playground[num_line].y )

    def onClose(self):
        self.menu.save_score()
        self.menu.stop_music()
        try:
            self.parent.destroy()
        except RuntimeWarning as e:
            print(e)

def TetrisGame():
    TetrisFrame(Tk()).mainloop()

if __name__ == "__main__":
    TetrisGame()
