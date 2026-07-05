import math
from turtle import *

# Heart shape equations
def heart_x(t):
    return 16 * math.sin(t) ** 3

def heart_y(t):
    return (13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t))

# Screen setup
speed(0)
bgcolor("black")
color("red")
pensize(2)
penup()

# Draw heart
for i in range(0, 628):
    t = i / 100
    x = heart_x(t) * 20
    y = heart_y(t) * 20
    goto(x, y)
    pendown()

hideturtle()
done()
