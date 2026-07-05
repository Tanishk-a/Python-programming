import turtle
import math
import time

# Screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Endless Heart 💖")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

colors = ["red", "hot pink", "deep pink", "magenta", "violet"]
color_index = 0

def heart(t, scale):
    x = 16 * math.sin(t)**3
    y = (13 * math.cos(t)
         - 5 * math.cos(2*t)
         - 2 * math.cos(3*t)
         - math.cos(4*t))
    return x * scale, y * scale

scale = 15
grow = True

while True:
    pen.clear()
    pen.color(colors[color_index])
    color_index = (color_index + 1) % len(colors)

    # Draw heart
    for i in range(0, 628):
        t = i / 100
        x, y = heart(t, scale)
        pen.goto(x, y)
        pen.pendown()

    pen.penup()

    # 💌 Text inside heart
    pen.goto(0, -10)
    pen.color("white")
    pen.write("Love", align="center", font=("Comic Sans MS", 18, "bold"))

    # 💓 Beating effect
    if grow:
        scale += 0.5
        if scale >= 18:
            grow = False
    else:
        scale -= 0.5
        if scale <= 15:
            grow = True

    time.sleep(0.08)
