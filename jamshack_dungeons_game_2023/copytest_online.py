import turtle


def proceed():
    turtle.register_shape("bg_dungeon.gif")
    turtle.shape("bg_dungeon.gif")
    global x
    x = True
    return x

# Register a shape
turtle.register_shape("game_icon.gif")

x = False

pen=turtle.Turtle()

# Use the shape
turtle.shape("game_icon.gif")
while True:

    if x == True:
        break

pen.color("red")
pen.write("Press Enter to proceed",align="center",font=("Arial",24,"normal"))


