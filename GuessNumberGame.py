#player can input a number, and the other player can guess. 
#This script was imported from Replit as well as the the clear function. To use this program, update clear function according to your IDE.

from art import logo
import random
from replit import clear

def game():
  print(logo)
  print("Welcome to the 'Guess a Number' game!")
  player_1 = input("Player 1, please input your name: ").title()
  player_2 = input("Player 2, please input your name: ").title()
  set_num = int(input(f"{player_1}, please input a number between 0 and 100 for {player_2} to guess: "))    
  clear()
  print(f"{player_2}, now it's time to guess the number!")
  #randomly pick a number for player to guess
  #let user choose difficulty level and set reamining chances to 5 or 10 
  if input("Type 'easy or 'hard' to choose a difficulty level: ").lower() == "easy":
    chance_remain = 10
    print("You will have 10 chances to guess the right number!")
  else:
    chance_remain = 5
    print("You will have 5 chances to guess the right number!")
  #ask user to input guess
  while chance_remain >= 1:
    guess_num = int(input("Please make a guess: "))
    if guess_num > set_num:
      chance_remain -= 1
      print("You guessed too large.")
      print(f"You have {chance_remain} chances left.")
    elif guess_num < set_num:
      chance_remain -= 1
      print("You guessed too small.")
      print(f"You have {chance_remain} chances left.")
    else:
      print(f"You win! The number is {set_num}, you guessed the right number!")
      break
  #if chance used up, tell user that he lose
  if chance_remain == 0:
    print(f"Sorry, you used up all guesses, {player_1} is the winner.")
#refresh the page and start new game      
while input("Type 'Y' to start the 'Guess a Number' game, type 'N' to exit: ").lower() == "y":
  clear()
  game()
