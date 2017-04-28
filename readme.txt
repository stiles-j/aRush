To run this application, unzip this archive, and place PcTc.py and aRushRC1.py in the same directory.
From there, you can run PcTc.py from the command line by typing:

python pctc.py

Player files will be saved in the same directory the application is saved in, and should not be moved.

#Author: Justice Stiles
#Description: 

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

