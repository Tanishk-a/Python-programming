import turtle
import math
import random
import time

screen = turtle.Screen()
screen.bgcolor("black")

main = turtle.Turtle()
main.hideturtle()
main.speed(0)
main.color("red")
main.penup()

small = turtle.Turtle()
small.hideturtle()
small.speed(0)
small.penup()

def heart(t, scale):
    x = 16 * math.sin(t) ** 3
    y = (13 * math.cos(t)
         - 5 * math.cos(2 * t)
         - 2 * math.cos(3 * t)
         - math.cos(4 * t))
    return x * scale, y * scale   # RETURN IS IMPORTANT

hearts = []

def create_small_heart():
    hearts.append({
        "x": 0.0,
        "y": 0.0,
        "scale": random.uniform(3, 6),
        "dy": random.uniform(1, 3),
        "color": random.choice(["red", "hot pink", "magenta"])
    })

scale = 15
grow = True

while True:
    main.clear()
    small.clear()

    # Draw main heart
    main.penup()
    for i in range(0, 628):
        t = i / 100
        x, y = heart(t, scale)
        main.goto(x, y)
        main.pendown()

    # Create small hearts
    if random.randint(1, 6) == 1:
        create_small_heart()

    # Draw small hearts
    for h in hearts[:]:
        h["y"] += h["dy"]
        small.color(h["color"])
        small.penup()

        for i in range(0, 628, 30):
            t = i / 100
            x, y = heart(t, h["scale"])
            small.goto(h["x"] + x, h["y"] + y)
            small.pendown()

        if h["y"] > 250:
            hearts.remove(h)

    # Beating effect
    if grow:
        scale += 0.3
        if scale >= 18:
            grow = False
    else:
        scale -= 0.3
        if scale <= 15:
            grow = True

    time.sleep(0.05)
