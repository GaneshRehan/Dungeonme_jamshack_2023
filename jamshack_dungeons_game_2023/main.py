import time
import turtle
import math
import random
import tkinter as tk
from maze_generator import glevel

wn = turtle.Screen()
root = tk.Tk()
wn.bgpic("bg_dungeon.png")
# wn.bgcolor("black")
wn.title("Save Yourself")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
wn.setup(screen_width, screen_height)
# wn.tracer(0)

# Register shapes
images = ["wizard_right.gif", "wizard_left.gif", "treasure.gif", "wall.gif", "enemy_left.gif", "enemy_right.gif"]
for image in images:
    turtle.register_shape(image)


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
            screen_x = -288+x*24
            screen_y = 288-y*24

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


# To quit the game
def close_game():
    wn.bye()
    quit()


# Create class instances
pen = Pen()
player = Player()

# Mark walls
walls = []

# Create enemies list
enemies = []

# To display about game
pen.goto(0,340)
pen.color("cyan")
pen.write("Save Yourself", align="center", font=("Arial", 50, "bold"))

# To display level number
pen.goto(-225, 290)
pen.color("brown")
pen.write("Level: 1", align="center", font=("Arial", 30, "bold"))

# To setup maze
setup_maze(levels[0])

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

# Turn-off screen updates
wn.tracer(0)

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

oldg = 0

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
            time.sleep(2)
            wn.bye()
            quit()

    # Print player gold on screen
    pen.goto(160,290)
    pen.color('gold')
    pen.write(f"Gold: {player.gold}", font=("Arial", 30, "bold"))
    if oldg != player.gold:
        pen.color("#253036")
        pen.write(f"Gold: {oldg}", font=("Arial", 30, "bold"))
        pen.color("gold")
        pen.write(f"Gold: {player.gold}", font=("Arial", 30, "bold"))
        oldg = player.gold

    # Keep track of gold to check level progress.
    if player.gold >= 400:
        pen.goto(0,0)
        pen.color("gold")
        pen.write("Level Completed!!!",align="center", font=("Arial", 50, "bold"))
        turtle.done()
        # print("Game Completed")
        break

    # Update screen
    wn.update()