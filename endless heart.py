import turtle
import math
import time

screen = turtle.Screen()
screen.bgcolor("black")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.color("red")
pen.penup()

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
    pen.penup()

    for i in range(0, 628):
        t = i / 100
        x, y = heart(t, scale)
        pen.goto(x, y)
        pen.pendown()

    # 💓 heartbeat effect
    if grow:
        scale += 0.5
        if scale >= 18:
            grow = False
    else:
        scale -= 0.5
        if scale <= 15:
            grow = True

    time.sleep(0.05)
