import random, time, threading
from tkinter import *
from random import *

COURT_WIDTH = 1000
COURT_HEIGHT = 500
COURT_COLOR = "black"
LEFT_PLAYER = "left"
RIGHT_PLAYER = "right"

class Pong(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # create game elements
        self.create_game_board()
        self.top_border = self.board.create_rectangle(40, 0, 1000-40, 5, fill="black")
        self.bottom_border = self.board.create_rectangle(40, 500-5, 1000-40, 500, fill="black")

        # game over boundaries
        self.left_border = self.board.create_rectangle(0, 0, 5, 500, fill = "black")
        self.right_border = self.board.create_rectangle(1000-5, 0, 1000, 500, fill = "black")

        # paddle1
        self.paddle1_hi = self.board.create_rectangle(20, 205, 40, 235, fill='white', outline="")
        self.paddle1_mid = self.board.create_rectangle(20, 235, 40, 265, fill='white', outline="")
        self.paddle1_low = self.board.create_rectangle(20, 265, 40, 295, fill='white', outline="")

        #paddle2
        self.paddle2_hi = self.board.create_rectangle(1000-20, 205, 1000-40, 235, fill='white', outline="")
        self.paddle2_mid = self.board.create_rectangle(1000-20, 235, 1000-40, 265, fill='white', outline="")
        self.paddle2_low = self.board.create_rectangle(1000-20, 265, 1000-40, 295, fill='white', outline="")

        x1, y1 = 495, randint(20, 500 - 40)
        x2, y2 = x1 + 10, y1 + 10
        self.ball = self.board.create_oval(x1, y1, x2, y2, fill='white')

        self.score_p1 = 0
        self.score_p2 = 0
        self.create_scoreboard()

        self.bind('<Any-KeyPress>', self.map_keys)

        self.new_round()

    def new_round(self):
        self.board.coords(self.paddle1_hi, 20, 205, 40, 235)
        self.board.coords(self.paddle1_mid, 20, 235, 40, 265)
        self.board.coords(self.paddle1_low, 20, 265, 40, 295)

        self.board.coords(self.paddle2_hi, 1000-20, 205, 1000-40, 235)
        self.board.coords(self.paddle2_mid, 1000-20, 235, 1000-40, 265)
        self.board.coords(self.paddle2_low, 1000-20, 265, 1000-40, 295)

        x1, y1 = 495, randint(20, 500 - 40)
        x2, y2 = x1 + 10, y1 + 10
        self.board.coords(self.ball, x1, y1, x2, y2)
        self.dx = -1.25
        self.dy = 1.25

        time.sleep(1)

    def create_scoreboard(self):
        # player 1 score
        self.scoreboard1 = Label(self, text="Player 1 Score : {}".format(self.score_p1))
        self.scoreboard1.pack(anchor='e')

        # player 2 score
        self.scoreboard2 = Label(self, text="Player 2 Score : {}".format(self.score_p2))
        self.scoreboard2.pack(anchor='w')

    def update_scoreboard(self):
        self.scoreboard1['text'] = "Player 1 Score : {}".format(self.score_p1)
        self.scoreboard2['text'] = "Player 2 Score : {}".format(self.score_p2)

    def create_game_board(self):
        self.board = Canvas(self, width=COURT_WIDTH, height=COURT_HEIGHT, background=COURT_COLOR)
        self.board.pack(padx=10, pady=10)

    def map_keys(self, event=None):
        key = event.keysym
        if key == "w":
            self.move_paddle1("up")
        elif key == "s":
            self.move_paddle1("down")
        elif key=="Up":
            self.move_paddle2("up")
        elif key == "Down":
            self.move_paddle2("down")
        else:
            pass

    def move_paddle1(self, dir):
        if dir == "up" and self.board.coords(self.paddle1_hi)[1] >= 25:
            self.board.move(self.paddle1_hi, 0, -20)
            self.board.move(self.paddle1_mid, 0, -20)
            self.board.move(self.paddle1_low, 0, -20)
        elif dir == "down" and self.board.coords(self.paddle1_low)[3] <= 500-25:
            self.board.move(self.paddle1_hi, 0, 20)
            self.board.move(self.paddle1_mid, 0, 20)
            self.board.move(self.paddle1_low, 0, 20)
        else:
            return

    def move_paddle2(self, dir):
        if dir == "up" and self.board.coords(self.paddle2_hi)[1] >= 25:
            self.board.move(self.paddle2_hi, 0, -20)
            self.board.move(self.paddle2_mid, 0, -20)
            self.board.move(self.paddle2_low, 0, -20)
        elif dir == "down" and self.board.coords(self.paddle2_low)[3] <= 500-25:
            self.board.move(self.paddle2_hi, 0, 20)
            self.board.move(self.paddle2_mid, 0, 20)
            self.board.move(self.paddle2_low, 0, 20)
        else:
            return

    def move_ball(self):
        self.board.move(self.ball, self.dx, self.dy)

    def move_paddle(self, canvas_obj_id):
        return
    def evaluate(self):
        x1, y1, x2, y2 = self.board.coords(self.ball)
        overlap_list = self.board.find_overlapping(x1, y1, x2, y2)

        # paddle 1 collision
        if self.paddle1_hi in overlap_list:
            self.dx = self.dx * -1
            self.dy = self.dy - 0.25
        elif self.paddle1_mid in overlap_list:
            self.dx = self.dx * -1
        elif self.paddle1_low in overlap_list:
            self.dx = self.dx * -1
            self.dy = self.dy + 0.25

        # paddle 2 collision
        if self.paddle2_hi in overlap_list:
            self.dx = self.dx * -1
            self.dy = self.dy - 0.25
        elif self.paddle2_mid in overlap_list:
            self.dx = self.dx * -1
        elif self.paddle2_low in overlap_list:
            self.dx = self.dx * -1
            self.dy = self.dy + 0.25

        # top and bottom border collisions
        elif self.top_border in overlap_list or self.bottom_border in overlap_list:
            self.dy = self.dy * -1

        # end game
        elif self.left_border in overlap_list:
            self.score_p2 = self.score_p2 + 1
            self.update_scoreboard()
            self.new_round()
        elif self.right_border in overlap_list:
            self.score_p1 = self.score_p1 + 1
            self.update_scoreboard()
            self.new_round()
        else:
            return



    def re_update(self):
        self.move_ball()
        self.evaluate()






if __name__ == '__main__':
    root = Pong(className="Pong Game")
    while True:
        root.update()
        root.update_idletasks()
        root.re_update()
        time.sleep(0.005)
