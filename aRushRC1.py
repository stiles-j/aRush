#Class definitions for aRush
#Note, in all functions, the type of question is identified by an integer.  For this purpose 0 = addition,
#1 = subtraction, 2 = multiplication, 3 = division.  The tracking arrays have a 5th element that is used 
#to track bonus points awarded.
from random import randint
from time import time, sleep

class Player():
  """The player class serves as a data model for the aRush game.  This class will track player performance,
  manintain the total score and other relevant player details.  The data members are all private, as are
  many of the fuctions.  The pubic functions make up the API for the Player class and should be the only
  methods called by client code"""

  #static data members
  rankLevels = [0, 20, 50, 95, 163, 315, 543]
  ranks = {0: "Rookie", 1: "Number-Cruncher", 2: "BIG-Number-Cruncher", 3: "Big-BAD-Number-Cruncher", 4: "Sir-Crunch-A-Lot", 5: "Magical-Number-Cruncher", 6: "Supreme-Crunch-O-Naut"}

  def __init__(self, playerName = '', totalScore = 0):
    self.__playerName = playerName
    self.__totalScore = totalScore
    self.__playerRank = 0
    self.__maxOperandValue = 10
    self.__maxOperands = 2
    self.__questionsAsked = [0, 0, 0, 0, 0]
    self.__questionsCorrect = [0, 0, 0, 0, 0]
    self.__lowPerformer = -1
    self.__lowPct = 1
    self.__setPlayerRank()
    self.__setRange()


  def __setPlayerRank(self) :
    #__setPlayerRank is a worker function that will set the numeric playerRank attribute based on totalScore
    #This method is invoked by __init__ and setTotalScore, and should not be called from outside the class
  
    if self.__totalScore >= 543:
      self.__playerRank = 6
    elif self.__totalScore >= 315:
      self.__playerRank = 5
    elif self.__totalScore >= 163:
      self.__playerRank = 4
    elif self.__totalScore >= 95:
      self.__playerRank = 3
    elif self.__totalScore >= 50:
      self.__playerRank = 2
    elif self.__totalScore >= 20:
      self.__playerRank = 1
    else:
      self.__playerRank = 0
      
  def __setRange(self):
    #__setRange is a worker function that sets the maxOperandValue and maxOperands attributes based on
    #the playerRank attribute.  It is called by __init__ and setTotalScore and should not be called from
    #outside the class.  Always call __setPlayerRank before __setRange. 
    if self.__playerRank == 0:
      self.__maxOperandValue = 10
      self.__maxOperands = 2
    elif self.__playerRank == 1:
      self.__maxOperandValue = 12
      self.__maxOperands = 2
    elif self.__playerRank == 2:
      self.__maxOperandValue = 15
      self.__maxOperands = 2
    elif self.__playerRank == 3:
      self.__maxOperandValue = 15
      self.__maxOperands = 3
    elif self.__playerRank == 4:
      self.__maxOperandValue =20
      self.__maxOperands = 3
    elif self.__playerRank == 5:
      self.__maxOperandValue = 30
      self.__maxOperands = 3
    elif self.__playerRank == 6:
      self.__maxOperandValue = 30
      self.__maxOperands = 4
      
  def awardPoints(self, amount):
    """
      awardPoints will increment or decrement the players totalScore attribute depending on whether
      it is passed a positive or negative argument.  After updating the score, it calls the 
      __setPlayerRank and setRange functions to update their relevant attributes as required. 
    """
    self.__totalScore += amount
    self.__setPlayerRank()
    self.__setRange()
    return self.__playerRank
    
  def getTotalScore(self):
    """Public interface to get totalScore data member value"""
    return self.__totalScore
    
  def getRank(self):
    """Public inteface to get playerRank value as a string.  To be clear, this returns the string description
    of the rank, not the numeric rank.  If you need the numeric rank use getNumericRank"""
    return Player.ranks[self.__playerRank]

  def getNumericRank(self):
    """Public interface to return the numeric playerRank value.  If you need the string description of the
    player rank use getRank"""
    return self.__playerRank
    
  def getMaxOperandValue(self):
    return self.__maxOperandValue
    
  def getMaxOperands (self):    
    return self.__maxOperands
    
  def getPlayerName (self):
    return self.__playerName
    
  def trackPerformance(self, qType, correct):
    """
    To track player performance, call this function after each question is asked.  It expects an int
    that defines the question type (0 - 3), and a bool defining if the question was answered correctly
    """
    if correct:
      self.__questionsCorrect[qType] += 1
    self.__questionsAsked[qType] += 1
    
  def getLowPerformer(self):
    """This function calculates the lowest performing question type for the player.  trackPerformance
    must be used properly for this function to work. This function returns a tuple with the index
    of the low performing problem type and the actual percent correct.  This allows client code to
    decide if the low performer is low enough to warrant action"""
    #first calculate the % correct for each question type:
    if self.__questionsAsked[0] > 0:
      additionPct = (self.__questionsCorrect[0] / self.__questionsAsked[0])
    else:
      additionPct = 1
    
    if self.__questionsAsked[1] > 0:
      subtractionPct = (self.__questionsCorrect[1] / self.__questionsAsked[1])
    else:
      subtractionPct = 1
      
    if self.__questionsAsked[2] > 0:
      multiplyPct = (self.__questionsCorrect[2] / self.__questionsAsked[2])
    else:
      multiplyPct = 1
    
    if self.__questionsAsked[3] > 0:
      divisionPct = (self.__questionsCorrect[3] / self.__questionsAsked[3])
    else:
      divisionPct = 1
      
    #next, find who's the lowest performer, and store it in the __lowPerformer attribute and
    #the actual percent correct in __lowPct
    self.__lowPct = additionPct
    self.__lowPerformer = 0
    
    if subtractionPct < self.__lowPct:
      self.__lowPerformer = 1
      self.__lowPct = subtractionPct
    
    if multiplyPct < self.__lowPct:
      self.__lowPerformer = 2 
      self.__lowPct = multiplyPct
      
    if divisionPct < self.__lowPct:
      self.__lowPerformer = 3
      self.__lowPct = divisionPct
  
    return (self.__lowPerformer, self.__lowPct)
    
class GameManager():
  """The game manager object is the only one that should be instantiated by client code.  It will instantiate
  Player and TimeDrill objects itself.  GameManager handles all interactions with the player outside of asking
  the acutal math questions which is directly handled by the TimeDrill class.  Client code should ONLY call 
  GameManager methods directly, and should not call Player or TimeDrill methods"""

  def __init__(self, playerName, startingScore):
    #initialize variables
    self.bonusQuestionType = 5
    self.playerName = playerName
    self.questionType = 5

    #instantiate the player object
    self.player1 = Player(self.playerName, startingScore) 

    #instantiate the TimeDrill object
    self.drill = TimeDrill(self.player1)

    #cache current player rank for future use
    self.currentRank = self.player1.getNumericRank()

  def greetPlayer(self):
    """greetPlayer will give new players the basics fo the game, and inform returning players of
    how many points they need to earn their next rank, as well as making silly commentary"""
    rank = self.player1.getNumericRank()
    if rank == 0:
      print("\n Hello", self.player1.getPlayerName(), "It looks like you're new here, so here's how the game works:\n \
First, you select what type of math you want to practice.  The game will\n \
give you a three second countdown, and then start.  You will have two\n \
minutes to answer twenty math questions.  For every answer you get right,\n \
you'll get one point.  Wrong answers will cause you to loose one point. If\n \
you finish early, you will get extra points for the time you have left! If\n \
you don't finish in time, the questions you didn't answer will cost you!\n \
Watch out, sometimes you will be offered extra points as a bonus for a\n \
certain type of question, so make sure you get those questions right to\n \
move up the ranks faster!  Right now your rank is Rookie, earn 20 points\n \
to get to the next rank!\n")
    elif rank == 1:
      print(" Hey, hey", self.player1.getPlayerName() + ",",  "Your current rank is Number-Cruncher! You\n \
no longer have to wear the funny looking hat with the propeller on the top\n \
like you did when you were a rookie, and the other mathematicians no\n \
longer laugh when you walk by.  Great work!  Now, go forth and build your\n \
legend! You currently have", self.player1.getTotalScore(), "total points.\n \
Earn 50 total points to get to the next rank.  You can do it!\n")
    elif rank ==2:
      print(" Alright", self.player1.getPlayerName() + ",", "your current rank is BIG-Number-Cruncher!\n \
You're well on your way to becoming a serious math wizard!  Rookies look\n \
at you with envy, and the upper ranks have begun to take notice of your\n \
exploits.  Numbers don't scare you, you got this. You currently have", self.player1.getTotalScore(), "total\n \
points.  You need 95 total points to get to the next rank.  Now go out\n \
there and show 'em you've got the right stuff! (and the right answers!)\n")
    elif rank == 3:
      print(" Hey", self.player1.getPlayerName() + "!", "Your current rank is Big-BAD-Number-Cruncher!  Numbers don't scare\n \
you, numbers should be scared OF you!  Math problems? No problem for you!\n \
You currently have", self.player1.getTotalScore(), "total points. You need 163 total points to get to the\n \
next rank. Now go out there and crunch-Crunch-CRUNCH your way to victory!\n")
    elif rank == 4:
      print(" " + self.player1.getPlayerName() + ",", "you've come so far... You are now in the elite ranks of number\n \
crunchers and are known as Sir-Crunch-A-Lot.  Your legend is known far and\n \
wide, and new number crunchers look to you as a hero among number crunchers!\n \
Truly, you have not met a math problem you could not CRUNCH!  You currently\n \
have", self.player1.getTotalScore(), "total points.  You need 315 total points to reach the next rank.\n \
Now go forth brave Sir-Crunch-A-Lot! Perform your daring deeds of\n \
mathematical doing, and let your legend grow!\n")
    elif rank == 5:
      print(" Look, it's", self.player1.getPlayerName() +"!", "All number crunchers know your name now! Your skills at\n \
number crunching are the stuff of legend.  Wild rumours circulate that you\n \
shoot lightning bolts out of your eyes, fireballs out of your ears, and icky\n \
green stuff out of your nose... (wait, maybe that last bit is true).  You\n \
are called", self.player1.getPlayerName() + ",", "The-Magical-Number-Cruncher, Wizard of mathematics! You\n \
currently have", self.player1.getTotalScore(), "total points.  You need 543 total points to make the next\n \
(and highest) rank.  Now go", self.player1.getPlayerName() + ",", "work your winding mathematical\n \
ways, and achieve your destiny of becoming the greatest number-cruncher of\n \
all time!\n")
    elif rank == 6:
      print(" Hail", self.player1.getPlayerName() + ",", "the great and powerful!  Greatest of the Number Crunchers, leader\n \
of the order of Number Crunchers!  All math problems cower at the mention\n \
of your name!  And so do rookies as a point of fact.  Last week one fainted\n \
when they heard you were coming to visit...  Maybe you should work on\n \
making yourself more approachable... But in the meantime, there are always\n \
more numbers to be crunched! Go forth, mighty", self.player1.getPlayerName(), "Supreme-Crunch-O-Naut!\n \
Go, and do great math!\n")

  def applyRound(self):
    """This method applies the last round of play to the player's total score.  It should be called immediately after
    calling the runTest on the TimeDrill object.  This functionality is intentionally not built into the TimeDrill
    class to create a better separation of duties as well as allow the GameManager class to be extended to create
    other bonuses, penalties, interactions etc that could be applied at this point"""
    self.player1.awardPoints(self.drill.getCurrentScore())

  def reportScore(self):
    """reportScore gives the player a summary of their performance last round.  It typically 
    should be called after applyRound"""

    lastRoundScore = self.drill.getCurrentScore()
    print("\n\n Alright,", self.playerName + ",", "Last round your total score was", lastRoundScore)
    #check for time bonus award, and mention it if there was one.
    if self.drill.getTimeBonus() > 0:
      print(" " + str(self.drill.getTimeBonus()), "of those points were from the time bonus.  Way to work the speed!")

  def offerBonus(self):
    """offerBonus will determine if a bonus round is due and inform the player of the type of question that will
    receive a bonus next round.  It should be called before selectType, so the player has the opportunity to 
    choose a question type that will earn bonuses.  If you do not want your game to use the bonus round feature, simply
    do not call this fuction."""

    #call getLowPerformer method on Player object to get data
    (lowPerformer, lowPct) = self.player1.getLowPerformer()
    #if the lowPerformer is less than 50% set and offer a bonus round
    if lowPct < 0.5:
      self.bonusQuestionType = lowPerformer
      #set the name of the question and type for later use
      if lowPerformer == 0:
        qType = "addition"
      elif lowPerformer == 1:
        qType = "subtraction"
      elif lowPerformer == 2:
        qType = "multiplication"
      elif lowPerformer == 3:
        qType = "division"
      else:
        print("Something has gone awry in the offerBonus method in the GameManager class.  Please look into it.")
      #inform player of bonus
      print("\n Hey", self.playerName + ",", qType, "questions are worth double points next round!\n \
Be sure to answer", qType, "questions correctly to rack up the points!")    
    else:
      #otherwise set the bonus round to an invalid number and move on
      self.bonusQuestionType = 5

  def selectType(self):
    """This method prompts the user for the type of questions they want to answer, performs apropriate data validation,
    and stores the answer in questionType for use elsewhere.  Offer Bonus should be called before this method if you 
    intend to use the bonus round feature."""

    #first reset the questionType variable to a bogus value to force a selection
    self.questionType = 5

    while self.questionType < 0 or self.questionType > 4:
      try:
        print(" Okay,", self.player1.getRank(), self.player1.getPlayerName() + ",", "What kind of questions would you like\n \
to answer? Type the number next to the type of question you want to answer:\n\n \
0 Addition\n 1 Subtraction\n 2 Multiplication\n 3 Division\n 4 All\n")
        self.questionType = int(input(" "))
        if self.questionType < 0 or self.questionType > 4:
          print(" Please enter a number between 0 and 4")
      except Exception:
        print(" Please enter a number between 0 and 4")
        self.questionType = 5

  def promoteRank(self):
    """promoteRank informs the player of changes to their rank and, by implication, that the questions will be changing
    in difficulty.  The actual work of changing ranks and the attendant attributes is handled by the Player object
    automatically when it updates total score.  This function is strictly for player feedback and should only be 
    called after applyRound has been called"""
    # if new rank is higher than old rank update rank and congradulate player, then display the greeting for the new rank
    if self.currentRank < self.player1.getNumericRank():
      self.currentRank = self.player1.getNumericRank()
      print("\n\n Congratulations", self.playerName + ",", "Your hard work has paid off and you've earned a new rank!\n \
You are now", self.player1.getRank(), self.playerName + ".", "Take pride, you've earned it!\n\n")
      self.greetPlayer()
    elif self.currentRank > self.player1.getNumericRank():
      #if new rank is lower than old rank, inform player gently of the demotion and update currentRank
      self.currentRank = self.player1.getNumericRank()
      print("\n\n Hey", self.playerName, "we really took a beating on that last round!  We're going\n \
to step back for a minute to the easier questions at the rank", self.player1.getRank() + ".",  "Think of\n \
it as a chance to take a breather, I know you'll be back to the upper ranks in no time!\n\n")
    else:
      #otherwise, the rank didn't change, so do nothing
      return

  def playGame(self):
    """playGame is a convinience function that acts effectively as a single player game-in-a-box.  Since single
    player is the most common way for a game of this nature to be run, this function seems justified in existing.  
    Also, for more complex games such as multi-player or those played over a network, this function can serve as 
    a template for how to make use of the GameManager methods to run a game"""

    #declare variables
    replay = 1

    self.greetPlayer()
    while replay:
      self.offerBonus()
      self.selectType()
      self.drill.runTest(self.questionType, self.bonusQuestionType)
      self.applyRound()
      self.reportScore()
      self.promoteRank()

      #prompt user to play again
      print("\n Hey,", self.playerName + ",", "want to play another round?  Practice makes perfect!\n \
Enter 1 to play agian, or 0 to exit\n")
      replay = -1  #set replay to a bogus value to lock player into while loop until valid response is entered
      while replay != 0 and replay != 1:
        try:
          replay = int(input())
          if replay != 0 and replay != 1:
            print("Please enter 1 to play again, or 0 to exit the game")
        except Exception:
          print("Please enter 1 to play again, or 0 to exit the game")
          replay = -1
    #say goodbye to the exiting player
    print("\nGreat work today", self.playerName + "!", "Your total score finishes at", str(self.player1.getTotalScore()) + ".", "See you next time!")

    #return total score to calling function to be used for persistence
    return self.player1.getTotalScore()



class TimeDrill():
  
  def __init__(self, player, bonusQuestion = 5): #bonusQuestion defaults to 5 which is none.  
    self.__currentScore = 0
    self.__currentPlayer = player
    self.__bonusQuestion = 5
    self.__totalTimeBonus = 0
    
  def __qAddition(self):
    
    #declare variables
    numOperands = 2
    operands = []
    
    #determine number of operands
    if self.__currentPlayer.getMaxOperands == 2:
      numOperands = 2
    else:
      numOperands = randint(2, self.__currentPlayer.getMaxOperands())
  
    #generate values for each operand and store in the operands array
    for num in range(0, numOperands):
      operands.append(randint(0, self.__currentPlayer.getMaxOperandValue()))
    
    #calculate the correct answer 
    answer = 0
    for number in operands:
      answer += number
    
    #display question to user and prompt for answer:
    for num in range(0, numOperands - 1):
      print(operands[num], "+ ", end="")
    print (operands[numOperands - 1], "= ", end="")

    #handle possible bad user input
    try:
        userInput = int(input())
    except Exception:
        print("Invalid input")
        userInput = -999999
    
    if int(userInput) == answer:
      return 1
    else:
      return 0

  def __qSubtraction(self):
    numOperands = 2
    operands = []

    #determine number of operands
    if self.__currentPlayer.getMaxOperands == 2:
        numOperands = 2
    else:
        numOperands = randint(2, self.__currentPlayer.getMaxOperands())

    #generate the first term, pad the number to allow for a greater array of questions
    operands.append(randint(0, self.__currentPlayer.getMaxOperandValue()) + 5)
      
    #generate remaining terms, ensuring the answer does not go below 0
    answer = operands[0]

    for num in range(1, numOperands):
        operands.append(randint(0, answer))
        answer -= operands[num] 

    #display the question to the user and prompt for input
    for num in range(0, numOperands - 1):
        print (operands[num], "- ", end="")
    print(operands[numOperands - 1], "= ", end="")

    #handle possible invalid input from user
    try:
        userInput = int(input())
    except Exception:
        print("Invalid input")
        userInput = -999999
        
    #return true or false based on whether user input matched answer:
    if userInput == answer:
        return 1
    else:
        return 0

  def __qMultiplication(self):
    numOperands = 2
    operands = []
    answer = 1

    #determine number of operands:
    if self.__currentPlayer.getMaxOperands() ==2 or self.__currentPlayer.getMaxOperands() == 3:
      numOperands = 2
    else:
      numOperands = randint(2, self.__currentPlayer.getMaxOperands())

    #generate the numbers to be used in the question, and store in operands[] there is an adjustment
    #to keep the numbers manageagle for multiplication
    for num in range(0, numOperands):
      operands.append(randint(0, self.__currentPlayer.getMaxOperandValue() - 2))

    #calculate the correct answer
    for num in operands:
      answer *= num

    #display the question to the user and prompt for the answer
    for num in range (0, numOperands - 1):
      print(operands[num], "* ", end="")
    print (operands[numOperands - 1], "= ", end="")

    #Exception handling for possible bad user input
    try:
      userInput = int(input())
    except Exception:
      print("Invalid Input")
      userInput = -999999

    #Return true if userInput matches answer, otherwise return false
    if userInput == answer:
      return 1
    else:
      return 0

  def __qDivision(self):
    numOperands = 2
    operands = []
    answer = 0

    #determine number of operands
    if self.__currentPlayer.getMaxOperands() == 2 or self.__currentPlayer.getMaxOperands() == 3:
      numOperands = 2
    else:
      numOperands = randint(2, self.__currentPlayer.getMaxOperands())

    #Generate values for each operand.  There is an adjustment to keep the numbers more manageable for division
    #and to prevent division by 0
    operands.append(randint(1, self.__currentPlayer.getMaxOperandValue() - 3))

    for num in range(1, numOperands):
      operands.append(operands[0] * randint(0, self.__currentPlayer.getMaxOperandValue() - 2))

    #calculate the correct answer and store in "answer"
    for num in range(numOperands - 1, 0, -1):
      answer = operands[num] / operands[num - 1]

    #display the question and prompt user for answer
    for num in range(numOperands - 1, 0, -1):
      print(operands[num], '/ ', end="")
    print (operands[0], "= ", end="")

    #Handle possible bad input by user
    try:
      userInput = int(input())
    except Exception:
      print("Invalid input")
      userInput = -999999

    #If user input matches answer return true, otherwise return false
    if userInput == answer:
      return 1
    else:
      return 0

  def __countdown(self):
    sleep(1)
    print("\n\nReady? ")
    sleep(1)
    print("Steady! ")
    sleep(1)
    print("GO!!!\n")
    sleep(1)

  def __awardPoints(self, qType, correct, amount = 1):
    if correct:
      self.__currentScore += amount
      if qType == self.__bonusQuestion:
        self.__currentScore += 1
        print("Bonus!")
    else:
      self.__currentScore -= amount

    #call trackPerformance on the player object to record players "batting averages"
    self.__currentPlayer.trackPerformance(qType, correct)

    
  def __applyTimeBonus(self, time):
    #award 1 point per full 6 seconds remaining
    bonusAmount = int(time / 6)
    #record bonusAmount in __totalTimeBonus for reporting purposes
    self.__totalTimeBonus = bonusAmount
    #award bonus points
    self.__awardPoints(4, 1, bonusAmount)

    
  def runTest(self, qType, bonusQuestionType):
    #declare variables
    thisQuestion = qType
    answer = 0
    startTime = time()
    endTime = startTime + 120
    currentTime = time()
    questionsAsked = 0

    #reset the __currentScore, bonusQuestionType and __totalTimeBonus each round:
    self.__currentScore = 0
    self.__totalTimeBonus = 0
    self.__bonusQuestion = bonusQuestionType

    #give the player a 3 second countdown to get ready:
    self.__countdown()

    #start timer, the entirety of the drill is executed within the timer loop
    while currentTime <= endTime and questionsAsked < 20:
      #if this question is 4, generate a random number between 0 and 3 and call the appropriate question function
      if thisQuestion == 4:
        thisQuestion = randint(0, 3)
      if thisQuestion == 0:
        answer = self.__qAddition()
      elif thisQuestion == 1:
        answer = self.__qSubtraction()
      elif thisQuestion == 2:
        answer = self.__qMultiplication()
      elif thisQuestion == 3:
        answer = self.__qDivision()
      else:
        print("Something went terribly wrong in the runTest method of TimeDrill.  Please look into it") #we should never get here
      #call award points to increment/decrement score
      self.__awardPoints(thisQuestion, answer)
      #update currentTime, increment questionsAsked and reset thisQuestion to qType for the next run through the loop
      currentTime = time()
      questionsAsked += 1
      thisQuestion = qType

    #award time bonus if any:
    timeRemaining = endTime - currentTime
    self.__applyTimeBonus(timeRemaining)

    #apply penalty for unanswered questions if any
    questionsRemaining  = 20 - questionsAsked
    if questionsRemaining:
      self.__awardPoints(4, 0, questionsRemaining)
    return self.__currentScore

  def getCurrentScore(self):
    return self.__currentScore

  def setBonusRound(self, qType):
    if qType >= 0 and qType < 4:
      self.__bonusQuestion = qType
    else:
      self.__bonusQuestion = 5

  def getTimeBonus(self):
    return self.__totalTimeBonus