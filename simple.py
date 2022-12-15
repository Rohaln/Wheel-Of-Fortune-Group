import json
import os
import random
import sys

import time
import datetime
import msvcrt 
import string

os.chdir(os.path.dirname(os.path.realpath(__file__)))
#import sys, os

#os.chdir(sys._MEIPASS)
#global variables
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters2 = 'ABCDEFGHIJKMOPQUVWXYZ'
vowels  = 'AEIOU'
price_vowels  = 250
lettersGuessed=[] 
playerTurn = 0 
winner = ""

# This is the player class 
class Player:  
    cash =  0
    name = "Player 1" 
 
class Player_2: 
    cash = 0 
    name = "Player 2" 

class Player_3: 
    cash = 0 
    name = "Player 3" 

# This returns a random value when a player spins the wheel 
def spinWheel():
    with open("wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)

#randomly gets a category and phrase
def getCatandPhrase():
    with open("phrases.json", 'r') as f:
        phrases = json.loads(f.read())

        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        print(category)
        print(phrase)
        return (category, phrase.upper())
    
#randomly gets a prize
def getPrize():
    with open("prizes.json", 'r') as f:
        prizes = json.loads(f.read())

        category = random.choice(list(prizes.keys()))
        prize   = random.choice(prizes[category])
        print("Congratulation you Won:")
        print(prize)
        return (category, prize.upper())
    
#converts the phrase that was picked into _ also checks to see if the guessed letter is in the phrase
def MakePhraseHidden(phrase,lettersGuessed):
    hiddenword = ''
    for s in phrase:
        if (s in letters) and (s not in lettersGuessed):
            hiddenword = hiddenword+' _ '
        else:
            hiddenword = hiddenword+s      
    return hiddenword

#Hide the phrase but display RSTLN
def MakePhraseHidden2(phrase,lettersGuessed):
    hiddenword = ''
    for s in phrase:
        if (s in letters2) and (s not in lettersGuessed):
            hiddenword = hiddenword+' _ '
        else:
            hiddenword = hiddenword+s      
    return hiddenword

#enter a letter to guess.Checks to see if the letter is a vowel if so, then it asks the user if they want to spend money for a vowel
def checksVowel(phrase,guess,lettersGuessed):
    if guess in vowels:
        answer= str(input("Would You Like to pay $250 for a Vowel(y or yes):").upper())
        if (answer=="YES") or (answer=="Y"):
                MakePhraseHidden(phrase,lettersGuessed) 
                if Player.cash < price_vowels:
                        print("Need {} to guess a vowel. Try again.".format(price_vowels))
                else:
                        Player.cash -= price_vowels
                return True
        else:
            return False
            
  #Checks to see if there is still a _ in the hidden phrase
  # if there is the puzzel isnt solved and you will continue to have to guess letters until it is solved              
def checkSolved(phrase):
    if '_' in MakePhraseHidden(phrase,lettersGuessed):
        return False
    else:
        print("Puzzel Solved")
        return True
#checks to see if the puzzle is solved
def checkPhraseSolved(phrase):
    solve= str(input("Enter the Phrase or type back to go back:").upper())
    if solve==phrase:
        print("The Puzzel has been solved")
        checkSolved(phrase)
    elif solve=="back": 
        getGuess(phrase,lettersGuessed)
    else:
        print("That is not the Puzzle")
        getGuess(phrase,lettersGuessed)
#gets the users guess for the turn
def getGuess(phrase,lettersGuessed):
    #ask for a user to enter a letter
 guess= str(input("Guess a letter or write solve to then solve the puzzel:").upper())
 solvedQuestionmark=checkSolved(phrase)
 if guess=="SOLVE":
     checkSolved(phrase)
 elif(solvedQuestionmark== False):
     #checks if the letter guessed is a vowel and will recall the function if they do not want to pay the fee for the vowel
     check=checksVowel(phrase,guess,lettersGuessed)
     if check == False:
        getGuess(phrase,lettersGuessed)
 #if they pay the fee for the vowel or guess a non vowel then it 
     else:
        
        lettersGuessed+=guess
        hiddenPhrase=MakePhraseHidden(phrase,lettersGuessed) 
        
        print(hiddenPhrase)
        print(lettersGuessed)
 elif(solvedQuestionmark== True):
     pass


# increase the turn number.
def increaseTurn(playerTurn):
    if(playerTurn==1) or playerTurn ==2 or (playerTurn==0):
        playerTurn+=1
    else:
        playerTurn=1
        
    return playerTurn 

# Chooses the winner based on the player with the most cash
def delcareWinner(winner): 
    if Player.cash > Player_2.cash and Player.cash > Player_3.cash: 
        winner = Player.name 
    elif Player_2.cash > Player.cash and Player_2 > Player_3.cash: 
        winner = Player_2.name 
    else: 
        winner = Player_3.name 
    
    return winner
    #Hide the phrase but display RSTLN
def MakePhraseHidden2(phrase,lettersGuessed):
    hiddenword = ''
    for s in phrase:
        if (s in letters2) and (s not in lettersGuessed):
            hiddenword = hiddenword+' _ '
        else:
            hiddenword = hiddenword+s      
    return hiddenword


#listens for keyboard inputs
def kbfunc():
    userInput = msvcrt.kbhit()
    if userInput:
        #getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = False
    return ret
#gets phrases and cat for the toss up
def tossUpCatandPhrase():
    with open("Tossup.json", 'r') as f:
        phrases = json.loads(f.read())

        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        print(category)
        print(phrase)
        return (category, phrase.upper()) 

def tossUp(category, phrase,lettersGuessed):
    print(phrase)
    #number of letters are how many seconds u get
    total_sec=(len(phrase))
    
    #convets phrase into a list of letters
    phrase_list=list(phrase)
    print(phrase_list)
    print("press a to enter a guess of the word")
    hiddenPhrase = MakePhraseHidden(phrase,lettersGuessed)
    print(hiddenPhrase)
    solved=False
    random_letter=random.choice(phrase_list)
    while total_sec>0:
        userInput = kbfunc() 
        #need to find a way not to repeat letters
        while random_letter in lettersGuessed:
            random_letter=random.choice(phrase_list)
        
        #random_letter=random.choice(phrase_list)
        lettersGuessed+=random_letter
        hiddenPhrase=MakePhraseHidden(phrase,lettersGuessed) 
        
        print(hiddenPhrase)



        #displays the time left to guess
        timer = datetime.timedelta(seconds = total_sec)
        print(timer, end="\r")
        time.sleep(1)
        total_sec -= 1
        #checks to see if the there was a a in inputed to the get a letter guess
        if userInput != False and userInput.decode() == 'a':
            #pauses the timer to let the juser have enough time to enter a word
            getGuess(phrase,lettersGuessed)
        solved=checkSolved(phrase)
        if solved==True and total_sec !=0:
            player=int(input("Which player guessed the word: "))
            total_sec=0
                  



                        
    print("The Game is Over")
    
    
        
class GameLogic:
    if __name__ == '__main__': 
        try:  
            print(("*" * 80))
            print(("*" * 80))
            print((("*" * 5) + (" " * 70) + ("*" * 5)))
            print((("*" * 5) + (" " * 21) + "Welcome to WHEEL OF FORTUNE!" + (" " * 21) + ("*" * 5)))
            print((("*" * 5) + (" " * 70) + ("*" * 5)))
            print((("*" * 5) + (" " * 70) + ("*" * 5)))
            print(("*" * 80))
            print(("*" * 80))
            category, phrase = getCatandPhrase()#gets a category and a phrase from the functionh
            hiddenPhrase = MakePhraseHidden(phrase,lettersGuessed)
            print(hiddenPhrase)
            solved=checkSolved(phrase)#defualts to false on start up
            while(solved == False):
                playerTurn=increaseTurn(playerTurn)#prints the users turn
                print("It is Player {} turn".format(playerTurn)) 
                if (playerTurn == 1):
                    print("Player  {} has $ {}".format(playerTurn, Player.cash)) 
                elif(playerTurn == 2): 
                    print("Player  {} has $ {}".format(playerTurn, Player_2.cash)) 
                else: 
                    print("Player  {} has $ {}".format(playerTurn, Player_3.cash))  
     #gets the results of a wheel spin and prints out the value for each letter guess
                wheelResults = spinWheel()
                turnValueStr=wheelResults["text"]
                turnValueType=wheelResults["type"] 
                turnValueInt=wheelResults["value"]  
                if (playerTurn == 1):
                    Player.cash += turnValueInt
                elif(playerTurn == 2): 
                    Player_2.cash += turnValueInt
                else: 
                    Player_3.cash += turnValueInt 
                print("The Value for each Letter is {}".format(turnValueStr))
     #calls the getGuess function to get the users guess
                getGuess(phrase,lettersGuessed)
     #then rechecks if the puzzel is solved
                solved=checkSolved(phrase) 
      
      
            print("Toss up Time")
            time.sleep(5)#waits 5 seconds before next round starts
            lettersGuessed.clear()
            #toss up question
            category, phrase = tossUpCatandPhrase()#gets a category and a phrase from the functionh
            tossUp(category, phrase,lettersGuessed)


            time.sleep(5)#waits 5 seconds before next round starts   

            #clears the guessed letters for round 2
            lettersGuessed.clear()
            #repeats code for next round
            print("Toss up is finised get ready for game 2")
            category, phrase = getCatandPhrase()
            hiddenPhrase = MakePhraseHidden(phrase,lettersGuessed)
            print(hiddenPhrase)
            solved=checkSolved(phrase)
            while(solved == False):
                playerTurn=increaseTurn(playerTurn)
                print("It is Player  {} turn".format(playerTurn)) 
                if (playerTurn == 1):
                    print("Player  {} has $ {}".format(playerTurn, Player.cash)) 
                elif(playerTurn == 2): 
                    print("Player  {} has $ {}".format(playerTurn, Player_2.cash)) 
                else: 
                    print("Player  {} has $ {}".format(playerTurn, Player_3.cash)) 
                wheelResults = spinWheel()
                turnValueStr=wheelResults["text"]
                turnValueType=wheelResults["type"] 
                turnValueInt=wheelResults["value"] 
                if (playerTurn == 1):
                    Player.cash += turnValueInt
                elif(playerTurn == 2): 
                    Player_2.cash += turnValueInt
                else: 
                    Player_3.cash += turnValueInt 
                print("The Value for each Letter is {}".format(turnValueStr))
                getGuess(phrase,lettersGuessed)
                solved=checkSolved(phrase)



            print("Toss up Time")
            time.sleep(5)#waits 5 seconds before next round starts
            lettersGuessed.clear()
            #toss up question
            category, phrase = tossUpCatandPhrase()#gets a category and a phrase from the functionh
            tossUp(category, phrase,lettersGuessed)
            time.sleep(5)#waits 5 seconds before next round starts
                
            lettersGuessed.clear()
            print("Toss up 2 is finished get ready for game 3")
            category, phrase = getCatandPhrase()
            hiddenPhrase = MakePhraseHidden(phrase,lettersGuessed)
            print(hiddenPhrase)
            solved=checkSolved(phrase)
            while(solved == False):
                playerTurn=increaseTurn(playerTurn)
                print("It is Player  {} turn".format(playerTurn)) 
                if (playerTurn == 1):
                    print("Player  {} has $ {}".format(playerTurn, Player.cash)) 
                elif(playerTurn == 2): 
                    print("Player  {} has $ {}".format(playerTurn, Player_2.cash)) 
                else: 
                    print("Player  {} has $ {}".format(playerTurn, Player_3.cash)) 
                wheelResults = spinWheel()
                turnValueStr=wheelResults["text"]
                turnValueType=wheelResults["type"] 
                turnValueInt=wheelResults["value"]
                if (playerTurn == 1):
                    Player.cash += turnValueInt
                elif(playerTurn == 2): 
                    Player_2.cash += turnValueInt
                else: 
                    Player_3.cash += turnValueInt 
                print("The Value for each Letter is {}".format(turnValueStr))
                getGuess(phrase,lettersGuessed)
                solved=checkSolved(phrase) 

            #clears the guessed letters for bonus round
            lettersGuessed.clear() 

            # Declares the overall winner
            winner = delcareWinner(winner) 
            print ("The winner of the Game is {}".format(winner))



            #Start bonus round
            print("Toss up is finised get ready for the bonus")

            #Print the categories
            # Opening JSON file
            f = open('categories.json',)
            # returns JSON object as a dictionary
            data = json.load(f)
            # Iterating through the json list
            for i in data['categories']:
                print(i)
            # Closing file
            f.close()

            #ask the user for the category
            database = "phrases.json"
            data = json.loads(open(database).read())
            userchoise = input("Choose a Category : ")
            print ("You Selected",category)

            #
            category, phrase = getCatandPhrase()
            hiddenPhrase = MakePhraseHidden2(phrase,lettersGuessed)
            print(hiddenPhrase)
            solved=checkSolved(phrase)
            while(solved == False):
                playerTurn=increaseTurn(playerTurn)
                if (playerTurn == 1):
                    print("Player  {} has $ {}".format(playerTurn, Player.cash)) 
                elif(playerTurn == 2): 
                    print("Player  {} has $ {}".format(playerTurn, Player_2.cash)) 
                else: 
                    print("Player  {} has $ {}".format(playerTurn, Player_3.cash)) 
                wheelResults = spinWheel()
                turnValueStr=wheelResults["text"]
                turnValueType=wheelResults["type"]
                turnValueInt=wheelResults["value"] 
                if (playerTurn == 1):
                    Player.cash += turnValueInt
                elif(playerTurn == 2): 
                    Player_2.cash += turnValueInt
                else: 
                    Player_3.cash += turnValueInt 
                print("The Value for each Letter is {}".format(turnValueStr))
                getGuess(phrase,lettersGuessed)
                solved=checkSolved(phrase)
                prize = getPrize()
                #Start bonus round
            print("Toss up is finised get ready for the bonus")

            #Print the categories
            # Opening JSON file
            f = open('categories.json',)
            # returns JSON object as a dictionary
            data = json.load(f)
            # Iterating through the json list
            for i in data['categories']:
                print(i)
            # Closing file
            f.close()

            #ask the user for the category
            database = "phrases.json"
            data = json.loads(open(database).read())
            userchoise = input("Choose a Category : ")
            print ("You Selected",category)

            #
            category, phrase = getCatandPhrase()
            hiddenPhrase = MakePhraseHidden2(phrase,lettersGuessed)
            print(hiddenPhrase)
            solved=checkSolved(phrase)
            while(solved == False):
                playerTurn=increaseTurn(playerTurn)
                if (playerTurn == 1):
                    print("Player  {} has $ {}".format(playerTurn, Player.cash)) 
                elif(playerTurn == 2): 
                    print("Player  {} has $ {}".format(playerTurn, Player_2.cash)) 
                else: 
                    print("Player  {} has $ {}".format(playerTurn, Player_3.cash)) 
                wheelResults = spinWheel()
                turnValueStr=wheelResults["text"]
                turnValueType=wheelResults["type"]
                turnValueInt=wheelResults["value"] 
                if (playerTurn == 1):
                    Player.cash += turnValueInt
                elif(playerTurn == 2): 
                    Player_2.cash += turnValueInt
                else: 
                    Player_3.cash += turnValueInt 
                print("The Value for each Letter is {}".format(turnValueStr))
                getGuess(phrase,lettersGuessed)
                solved=checkSolved(phrase)
                prize = getPrize()
        
                
            lettersGuessed.clear()
        
                
            lettersGuessed.clear()
        except BaseException:
            print(sys.exc_info()[0])
            import traceback
            print(traceback.format_exc())
        finally:
            print("Press Enter to Exit")
            input()