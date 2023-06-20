import time
import turtle
import math
import random
import tkinter as tk
import pygame
from maze_generator import glevel

# Register shapes
images = ["wizard_right.gif", "wizard_left.gif", "treasure.gif", "wall.gif", "enemy_left.gif", "enemy_right.gif", "game_icon.gif", "bg_dungeon.gif", "final_image.gif"]
for image in images:
    turtle.register_shape(image)

# Load musics of bgm
musics = ["starting_bgm.mp3", "game_play_bgm.mp3", "game_over.mp3", "game_victory.mp3"]

wn = turtle.Screen()
root = tk.Tk()
pygame.mixer.init()
wn.bgpic("bg_dungeon.png")
turtle.shape("game_icon.gif")
wn.title("GG")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
wn.setup(screen_width, screen_height)


# Create Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("blank")
        self.color("white")
        self.penup()
        self.speed(10)


# Create Player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wizard_right.gif")
        self.color("blue")
        self.penup()
        self.speed(10)
        self.gold = 0

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor()+24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor()-24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self, ):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()

        self.shape("wizard_left.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        self.shape("wizard_right.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if  distance < 5:
            return True
        else:
            return False


# Create treasure
class Treasure(turtle.Turtle):
    def __init__(self,x ,y):
        turtle.Turtle.__init__(self)
        self.shape("treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()


# Create Enemy
class Enemy(turtle.Turtle):
    def __init__(self,x ,y):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 50
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2) + (b**2))

        if distance < 100:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()


# Create levels
levels = glevel

# Add treasures list
treasures = []

# Mark walls
walls = []

# Create enemies list
enemies = []


# Setup maze
def setup_maze(level):
    walls.clear()
    enemies.clear()
    treasures.clear()
    wn.bgpic("bg_dungeon.png")
    turtle.shape("bg_dungeon.gif")
    player.shape("wizard_right.gif")
    # wn.tracer(0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            lx = len(level[0])//2 * 24
            screen_x = -lx + x*24
            screen_y = 288 - y*24

            if character == "X" or character=='x':
                pen.goto(screen_x, screen_y)
                pen.shape("wall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == "P":
                player.goto(screen_x, screen_y)

            if character == "T":
                treasure = Treasure(screen_x, screen_y)
                pen.stamp()
                treasures.append(treasure)

            if character == "E":
                enemy = Enemy(screen_x, screen_y)
                pen.stamp()
                enemies.append(enemy)


# Main game loop function
def main_game_loop(lv):

    # Keyboard Bindings
    turtle.listen()
    turtle.onkey(player.go_up, "Up")
    turtle.onkey(player.go_down, "Down")
    turtle.onkey(player.go_left, "Left")
    turtle.onkey(player.go_right, "Right")
    turtle.onkey(player.go_up, "w")
    turtle.onkey(player.go_down, "s")
    turtle.onkey(player.go_left, "a")
    turtle.onkey(player.go_right, "d")
    turtle.onkey(close_game, "q")
    turtle.onkey(close_game, "Q")
    turtle.onkey(proceed, "Return")

    oldg = 0
    player.gold = 0

    wn.bgpic("bg_dungeon.png")

    # To display about game
    pen.goto(0, 340)
    pen.color("cyan")
    pen.write("Go Grab", align="center", font=("Arial", 50, "bold"))

    # To display level number
    pen.goto(-225, 290)
    pen.color("red")
    pen.write(f"Level: {lv+1}", align="center", font=("Arial", 30, "bold"))

    # Main game loop
    while True:
        # Keep track of treasures
        for treasure in treasures:
            if player.is_collision(treasure):
                player.gold += treasure.gold
                # print(f"Gold: {player.gold}")
                treasure.destroy()
                treasures.remove(treasure)

        # Keep track of enemies
        for enemy in enemies:
            if player.is_collision(enemy):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(musics[2])
                pygame.mixer.music.play(-1)
                pen.goto(0, 0)
                pen.color("red")
                pen.write("Game Over!!!", align="center", font=("Arial", 30, "bold"))
                time.sleep(4)
                wn.bye()
                pygame.mixer.music.stop()
                quit()

        # Print player gold on screen
        pen.goto(160, 290)
        pen.color('gold')
        pen.write(f"Gold: {player.gold}", font=("Arial", 30, "bold"))
        if oldg != player.gold:
            pen.color("#253036")
            pen.write(f"Gold: {oldg}", font=("Arial", 30, "bold"))
            pen.color("gold")
            pen.write(f"Gold: {player.gold}", font=("Arial", 30, "bold"))
            oldg = player.gold

        # Keep track of gold to check level progress.
        if player.gold >=500:
        # if player.gold >= 100:
            pen.goto(0, 0)
            pen.color("gold")
            pen.write("Level Completed!!!", align="center", font=("Arial", 50, "bold"))
            lv += 1
            time.sleep(3)
            return lv

        # Update screen
        wn.update()


# To quit the game
def close_game():
    wn.bye()
    quit()


def proceed():
    pen.clear()
    turtle.shape("game_icon.gif")
    pen.goto(0,0)
    pen.color("red")
    pen.goto(0,40)
    pen.write("Game Started!!!", align="center", font=("Arial", 50, "bold"))
    pen.goto(0, -130)
    pen.write("All the best!!!", align="center", font=("Arial", 50, "bold"))
    time.sleep(3)
    pen.clear()
    global press_enter
    press_enter = True
    pen.write("Escape from your enemies and GO GRAB your treasures!!!", align="center", font=("Arial", 30, "bold"))
    time.sleep(3)
    pen.clear()
    pen.write("Use arrow keys or asdw keys to move your player", align="center", font=("Arial", 30, "bold"))
    time.sleep(3)
    pen.clear()
    pen.write("Press q to quit the game", align="center", font=("Arial", 40, "bold"))
    time.sleep(3)
    pen.clear()


# Create class instances
pen = Pen()
player = Player()

pygame.mixer.music.load(musics[0])
pygame.mixer.music.play(-1)
turtle.penup()
pen.goto(0,50)
pen.color("#007975")
pen.write("Go Grab", align="center", font=("Arial", 60, "italic"))
pen.goto(0,-100)
pen.color("gold")
pen.write("Press Enter key to continue", align="center", font=("Arial", 30, "bold italic"))
pen.goto(0,-200)
pen.color("red")
pen.write("Press q to quit the game", align="center", font=("Arial", 30, "bold"))
pen.goto(screen_width//2 - 450, -screen_height//2 + 100)
pen.color("red")


# Checking if user pressed enter key
press_enter = False
while True:
    turtle.listen()
    turtle.onkey(proceed, "Return")
    turtle.onkey(close_game, "q")
    turtle.update()

    if press_enter:
        break
pygame.mixer.music.stop()

# Music beginning of lv 1
pygame.mixer.music.load(musics[1])
pygame.mixer.music.play(-1)
# To setup level of maze
lv = 0

# To setup maze
setup_maze(levels[lv])

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

# Main game loop of lv 1

lv = main_game_loop(lv=lv)

pygame.mixer.music.stop()

# Music beginning of lv 2
pygame.mixer.music.load(musics[1])
pygame.mixer.music.play(-1)

# Resetting walls, treasure and enemies
walls.clear()
treasures.clear()
enemies.clear()
wn.clear()
wn.bgpic("bg_dungeon.png")
turtle.shape("bg_dungeon.gif")

# To setup maze for lv 2
player.shape("square")
player.color("blue")
setup_maze(levels[lv])

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=200)

# Main game loop of lv 2
lv = main_game_loop(lv=lv)

# Music beginning of lv 3
pygame.mixer.music.load(musics[1])
pygame.mixer.music.play(-1)

# Resetting walls, treasure and enemies
walls.clear()
treasures.clear()
enemies.clear()
wn.clear()
wn.bgpic("bg_dungeon.png")
turtle.shape("bg_dungeon.gif")

# To setup maze for lv 3
player.shape("square")
player.color("blue")
setup_maze(levels[lv])

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=150)

# Main game loop of lv 3
lv = main_game_loop(lv=lv)

# Music beginning of lv 4
pygame.mixer.music.load(musics[1])
pygame.mixer.music.play(-1)

# Resetting walls, treasure and enemies
walls.clear()
treasures.clear()
enemies.clear()
wn.clear()
wn.bgpic("bg_dungeon.png")
turtle.shape("bg_dungeon.gif")

# To setup maze for lv 4
player.shape("square")
player.color("blue")
setup_maze(levels[lv])

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=100)

# Main game loop of lv 4
lv = main_game_loop(lv=lv)

# Music beginning of lv 5
pygame.mixer.music.load(musics[1])
pygame.mixer.music.play(-1)

# Resetting walls, treasure and enemies
walls.clear()
treasures.clear()
enemies.clear()
wn.clear()
wn.bgpic("bg_dungeon.png")
turtle.shape("bg_dungeon.gif")

# To setup maze for lv 5
player.shape("square")
player.color("blue")
setup_maze(levels[lv])

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=50)

# Main game loop of lv 5
lv = main_game_loop(lv=lv)

# Game completion message
if lv == len(levels):
    pygame.mixer.music.load(musics[3])
    pen.clear()
    wn.clear()
    turtle.shape("bg_dungeon.gif")
    pen.color("gold")
    pen.write("""Congrulations!!! 
        You have completed all the levels!""", align="center", font=("Arial", 30, "italic"))
    pygame.mixer.music.play(start=1)
    time.sleep(5)
    pen.clear()
    pen.goto(0,50)
    pen.write("Credits", align="center", font=("Arial", 30, "bold"))
    pen.goto(0,-100)
    pen.write("This game is developed by Ganesh Rajapatruni and Jyotishka Deb", align="center", font=("Arial", 30, "bold italic"))
    time.sleep(4)
    pen.clear()
    pen.goto(0,50)
    pen.write("Developed by Ganesh Rajapatruni", align="center", font=("Arial", 40, "bold italic"))
    pen.goto(0,-100)
    pen.write("Maps are designed by Jyotishka Deb", align="center", font=("Arial", 40, "bold italic"))
    time.sleep(4)
    pygame.mixer.music.stop()