from turtle import Turtle, Screen
import random
from tkinter import messagebox
#set up our screen
screen = Screen()
screen.setup(width=500, height=400)
screen.title("Turtle Racing Game")
#set up lists
all_turtles = []
position_y = [150, 100, 50, 0, -50, -100, -150]
color_list = ["red", "coral", "gold", "green", "blue", "purple"]

#user input
user_bet = screen.textinput(title="Select Your Bet!", prompt="Which turtle will win the race?\n(Red/Coral/Gold/Green/Blue/Purple)\nEnter the color: ")

#create turtles
for turtle_index in range(0, 6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(color_list[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=position_y[turtle_index])
    all_turtles.append(new_turtle)

#game starts and checks if win
if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                messagebox.showinfo("Result", f"Your bet is right! The {winning_color} turtle has won!")
            else:
                messagebox.showinfo("Result", f"Your guess is wrong. The {winning_color} turtle has won.")
            is_race_on = False

        else:
            turtle.forward(random.randint(0, 10))

#exit on click
screen.exitonclick()
