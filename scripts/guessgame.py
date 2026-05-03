import os, math, random

import scripts.data as d
import scripts.funcs as f

# Activity: Guessing Game
def guessgame():
    f.clear()
    maxnum = 100
    # By guessing right the first time you get a triple prefix box. Each time you fail to guess, the reward halves
    newnumber = True
    print( f"Welcome to Guess Game! Guess a number from 1 to {maxnum}. The earlier you guess, the more credits you get!\n" )

    while True:
        if newnumber:
            reward = 1000
            rightnumber = random.randint( 1, maxnum )
            newnumber = False
        givenumber = input("Input a number! or exit\n")
        if str( givenumber.lower() ) == "exit":
            return
        elif d.checkifproperint( givenumber ) == False:
            print("Incorrect number!...")
        elif rightnumber > int(givenumber): # if guessed less
            f.clear()
            reward /= 2
            print( f"{givenumber} is lower, try something higher!" )
        elif rightnumber < int(givenumber): # if guessed more
            f.clear()
            reward /= 2
            print( f"{givenumber} is higher, try something lower!" )
        else:
            reward = math.ceil( reward )
            d.addcredits( reward )
            print( f"You guessed right! Your reward is {reward} credits! You now have {d.inventory[0][1]} credits." )
            
            newnumber = True
