#***PLEASE NOTE, THIS PROGRAM IS WRITTEN IN PYTHON 3***

#This program is a game designed to help grade school children practice arithmetic and mental math
#skills.  The program should be invoked from the command line using its name PcTc.py.  Once started
#the program will ask the player for their name, then attempt to match that name to an existing player
#file.  If the file exists, the program will load it so the player will have continuity of play across
#multiple sessions.  The player is allowed to select the type of math questions they want to answer. 
#After making their selection, the program will give the player a three second countdown, then start
#the round of play.  The player has two minutes to answer 20 questions.  For every correct answer, 
#the player will get 1 point.  For every wrong answer, they will loose 1 point.  There is a system of
#ranks implemented to ramp up difficulty as the player progresses.  The rank system is dynamic and 
#can change after each round of play, either up or down.  This way children who are struggling with 
#a new level will not be burnt out by continuing to face questions they are not yet able to handle.
#the system tracks performance across a play session for each type of question, then offers a bonus 
#for correct answers to question types a player is struggling with.  The idea here being to motivate
#the player to keep trying to improve the areas where they are weakest rather than avoid them or 
#burn out.  

#Note, the various operations are always referred to by an operation ID.  This is standardized as 
#follows: 0 = addition, 1 = subtraction, 2 = multiplication, 3 = division.

from aRushRC1 import Player, TimeDrill, GameManager
import os
import sys

def playerSetup():
  #declare variables
  playerName = ""
  totalScore = 0

  #prompt user for name, use name to search for playerFile
  playerName = input("Please enter your name: ")
  if os.path.exists(playerName + '.txt'):
    if os.path.isfile(playerName + '.txt'):
      #if the file exists open it
      playerFile = open(playerName + '.txt', 'Ur')

      #try to read the total score from the playerFile
      try:
        totalScore = int(playerFile.readline())
      except Exception:
        #if something goes wrong with the read, print a warning, and set total score to 0
        print("Unable to read player file")
        totalScore = 0
      
      #return the loaded player data to the calling function
      return (playerName, totalScore)
  else:
    #if there is no matching playerFile, return the playername and default (0) total score
    return (playerName, totalScore)

def saveData(playerName, totalScore):
  outFile = open(playerName + '.txt', 'w')
  success = outFile.write(str(totalScore))
  if not success:
    print("Critical Error: Failed to save player data.")

def main(): 
  #call playerSetup to initialize basic player variables
  playerName, totalScore = playerSetup()

  #instantiate the GameManager object using values supplied by the playerSetup function
  player1 = GameManager(playerName, totalScore)

  #Call playGame, and capture the final score in total score to be saved in the playerFile
  totalScore = player1.playGame()  

  #call saveData to save the player's progress
  saveData(playerName, totalScore)

if __name__=='__main__':
    main()
