#Author: Tristin Spencer
#Date written: 03/04/2023
#Assignment:   Module8 Final Project
#Short Desc: This program creates a GUI window and allows the user to play the classic snake game. 

from tkinter import *
import random
import time

#Game Dimensions, Colors, and Snake Speed
WIDTH = 500
HEIGHT = 400
SPACE_SIZE = 20
SNAKE = "#00FF00"
FOOD = "#0000FF"
SPEED = 10
# Define global variables
running = False
#create the GUI window
root = Tk()
root.title("Snake Game")
#create the canvas to draw the game
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()
#Class to represent the snake
class Snake:
    #Iniitialize the snake on the canvas and starting direction
    def __init__(self, canvas):
        self.canvas = canvas
        self.body = [[0, 0] for _ in range(3)]
        self.squares = [self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE, tag="snake") for x, y in self.body]
        self.direction = "right"
        self.canvas.bind_all("<KeyPress>", self.on_keypress)
    #Function to allow the movement of the snake and check for collisions
    def move(self):
        x, y = self.body[0]
        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE
        self.body = [[x, y]] + self.body[:-1]
        for i, square in enumerate(self.squares):
            x, y = self.body[i]
            self.canvas.coords(square, x, y, x + SPACE_SIZE, y + SPACE_SIZE)
        if self.collides_with_wall() or self.collides_with_self():
            game_over()
        if self.collides_with_food():
            self.grow()
            food.new()
    def collides_with_wall(self):
        x, y = self.body[0]
        return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT
    def collides_with_self(self):
        return self.body[0] in self.body[1:]
    def collides_with_food(self):
        return self.body[0] == [food.x, food.y]
    #Function to grow the snake when it collides with food
    def grow(self):
        self.body.append(self.body[-1])
        self.squares.append(self.canvas.create_rectangle(self.body[-1][0], self.body[-1][1], self.body[-1][0] + SPACE_SIZE, self.body[-1][1] + SPACE_SIZE, fill=SNAKE, tag="snake"))
        label.config(text="Points:{}".format(len(self.body) - 3))
    #Function for the actual control of the snake
    def on_keypress(self, event):
        if event.keysym == "Left":
            self.direction = "left"
        elif event.keysym == "Right":
            self.direction = "right"
        elif event.keysym == "Up":
            self.direction = "up"
        elif event.keysym == "Down":
            self.direction = "down"
#Class to represent the food. Generates food
class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.new() 
    def new(self):
        x = random.randint(0, (WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = random.randint(0, (HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE
        self.canvas.delete("food")
        self.canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD, tag="food")
        self.x = x
        self.y = y
#Function to end the game and display "Game Over" message
def game_over():
    global running
    running = False
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
#Function to Start the game
def start_game():
    global score, direction, running, snake, food
    global running  # add this line
    score, direction, running = 0, 'right', True
    canvas.delete("all")
    snake, food = Snake(canvas), Food(canvas)
    label.config(text="Points:{}".format(score))
    while running:
        snake.move()

        if snake.collides_with_wall() or snake.collides_with_self():
            game_over()

        if snake.collides_with_food():
            snake.grow()
            food.new()

        canvas.update()
        time.sleep(0.1)
#Function to pause the game
def pause_game():
    global running
    running = False
#Function to resume playing the game
def play_game():
    global running
    running = True
    while running:
        snake.move()
        if snake.collides_with_wall() or snake.collides_with_self():
            game_over()
        if snake.collides_with_food():
            snake.grow()
            food.new()
        canvas.update()
        time.sleep(0.1)
#Function to exit the game and shut down the program
def exit_game():
    root.destroy()
#Creating a start button to begin the game
start_button = Button(root, text="Start Over", command=start_game)
start_button.pack()
#Creating a pause button to pause the game
pause_button = Button(root, text="Pause", command=pause_game)
pause_button.pack()
#Creating a play button
play_button = Button(root, text="Play", command=play_game)
play_button.pack()
#Creating the Exit button
exit_button = Button(root, text="Exit", command=exit_game)
exit_button.pack()
#create the score label
label = Label(root, text="Points: ", font=('consolas', 40))
label.pack()
#start the game
start_game()
#start the GUI
root.mainloop()