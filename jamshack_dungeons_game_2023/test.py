import time
import turtle
import math
import random
import tkinter as tk
from maze_generator import glevel

# Register shapes
images = ["wizard_right.gif", "wizard_left.gif", "treasure.gif", "wall.gif", "enemy_left.gif", "enemy_right.gif", "game_icon.gif"]
for image in images:
    turtle.register_shape(image)

wn = turtle.Screen()
root = tk.Tk()
wn.bgpic("bg_dungeon.png")
turtle.shape("game_icon.gif")
wn.title("GG")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
wn.setup(screen_width, screen_height)
wn.tracer(0)


# Create Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
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
        # self.shape("enemy_right.gif")
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
            # self.shape("enemy_left.gif")
        elif self.direction == "right":
            dx = 24
            dy = 0
            # self.shape("enemy_right.gif")
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

        if distance < 75:
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


# Setup maze
def setup_maze(level):
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
                treasures.append(treasure)

            if character == "E":
                enemy = Enemy(screen_x, screen_y)
                enemies.append(enemy)


# Main game loop function
def main_game_loop(lv):
    oldg = 0
    player.gold = 0

    # To display about game
    pen.goto(0, 340)
    pen.color("cyan")
    pen.write("Save Yourself", align="center", font=("Arial", 50, "bold"))

    # To display level number
    pen.goto(-225, 290)
    pen.color("brown")
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
                pen.goto(0, 0)
                pen.color("red")
                pen.write("Game Over!!!", align="center", font=("Arial", 30, "bold"))
                # turtle.done()
                # print("Game Over")
                time.sleep(5)
                wn.bye()
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
        # if player.gold >= (lv+4)*100:
        if player.gold >= 100:
            pen.goto(0, 0)
            pen.color("gold")
            pen.write("Level Completed!!!", align="center", font=("Arial", 50, "bold"))
            lv += 1
            time.sleep(3)
            pen.clear()
            # wn.bye()
            # turtle.done()
            # print("Game Completed")
            return lv

        # Update screen
        wn.update()


# To quit the game
def close_game():
    wn.bye()
    quit()


def proceed():
    pen.clear()
    pen.goto(0,0)
    pen.color("red")
    pen.write("""Game Started!!!
    All the Best!!!""", align="center", font=("Arial", 30, "bold"))


# Create class instances
pen = Pen()
player = Player()

pen.goto(0,50)
pen.color("#007975")
pen.write("Go Grab", align="center", font=("Arial", 50, "italic"))
pen.goto(0,-100)
pen.color("blue")
pen.write("Press Enter key to continue", align="center", font=("Arial", 25, "bold"))

# Mark walls
walls = []

# Create enemies list
enemies = []

# To setup level of maze
lv=0

# To setup maze
setup_maze(levels[lv])

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


# Turn-off screen updates
wn.tracer(0)

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

# Main game loop of lv 1

lv = main_game_loop(lv=lv)

# Resetting walls, treasure and enemies
walls = []
treasures = []
enemies = []

# To setup maze
setup_maze(levels[lv])

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=200)

# Main game loop of lv 2
lv = main_game_loop(lv=lv)
