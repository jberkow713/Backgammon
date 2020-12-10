import turtle
import os
import math
import random 
from copy import deepcopy
import numpy as np

def BigRoll():
        Die = random.randint(2, 6)
        Die2 = random.randint(2,6)
        return Die+Die2 
# print(BigRoll())        

screen = turtle.Screen()
screen.setup(800,800)
Boardsize = 800
player = turtle.Turtle()
player.color("red")
player.shape("square")
player.penup()
player.speed(0)

def random_move():
        
        amplifier = random.randint(1,5)
        speed = BigRoll()*amplifier

        
        rand = random.randint(0,3)
        x = player.xcor()
        y = player.ycor()

        if rand == 0:
                x += speed
                y += speed 
        if rand == 1:
                x -= speed 
                y -= speed
        if rand == 2:
                y += speed * 1.5
                x+=speed * 1.5
        if rand == 3:
                x+= speed * 2                
                y += speed * 2
         
        player.setx(x)
        player.sety(y)
        if x < -(Boardsize/2) or x > (Boardsize/2):
                x = 0
                y = 0
        if y < -(Boardsize/2) or y > (Boardsize/2):
                x = 0
                y = 0
        player.setpos(x, y)
        return(player.position())

        
def gamble():
        player.setpos(0,0)
        Amount = input("How much would you like to risk?")
        Amount = int(Amount)
        guess = input("How many moves before your turtle is reset?")
        guess = int(guess)
        
        count = 1
        
        random_move()

        while random_move() != (0,0):
                
                random_move()
                count +=1
              

                

        if guess == count:
                reward = Amount**2
                print(f"What a guess! You receive{reward-Amount}")
                return (reward-Amount)

        elif guess != count:
                if guess / count >.85:
                        reward = Amount*2
                        print(f"Not a bad guess... you have made {reward-Amount}")
                        return (reward-Amount)
                elif guess / count < .7:
                        reward = 0
                        print(f"Better luck next time fool! You lost{Amount}")
                        return 0 
    
        
Player_Money = 10000
       

                                       



                 






turtle.listen()
turtle.onkey(random_move, "x")

turtle.onkey(gamble, "g") 

turtle.mainloop()