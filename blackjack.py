#Daniel Rovell
#Black Jack Game for Praeses
#This game was made to run with python 3

#How to use:
#Depending on your install run 'python3 blackjack.py' or '*your python3 command* blackjack.py'
#

import os
import os.path
import random
import sys
import datetime

values = {'ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10}

#Function for making a deck
def newDeck(values):
    deck = []
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    index = 0
    for key in values:
        for f in range(0, len(suits)):
            deck.append(key + ' of ' + suits[f])
            index += 1
    return deck

#Player class, each player has a hand
class Player:
    def __init__(self, hand, draw):
        self.hand = hand

    def drawCard(self, deck):
        draw = random.choice(deck) 
        return draw

#Computer the score and run an ace check
def computeScore(hand):
    total = 0
    value_set = []
    for i in hand:
        card = i.partition(' ')[0]
        if card in values:
            x = values[card]  
            value_set.append(x)
    total = (sum(value_set))
    ace_check = True
    while ace_check == True:
        if total > 21 and 11 in value_set:
            value_set.remove(11)
            value_set.append(1)
            total = sum(value_set)
        else:
            ace_check = False
    return total 

#Main function
def main():
    #initialize variables
    playing = True
    betting = False
    firstRound = True
    bet = 0
    playerTotal = 0
    dealerTotal = 0
    playerWonTotal = 0
    playerWon = 0
    playerLostTotal = 0
    playerLost = 0
    playerMoney = 0
    dealerMoney = 0
    playerLosses = 0
    playerWins = 0

    #Welcome message
    print('#################################################################')
    print("----------------------Welcome to BlackJack!----------------------")
    print('---------------------------Let\'s play!---------------------------')
    print('#################################################################')

    #Game loop
    while playing == True:
        #Initialize deck, player, and dealer
        deck = newDeck(values)
        player = Player([],[])
        dealer = Player([],[])

        #Will the player be betting money?
        status = 'checkBetting'
        while (status == 'checkBetting'):
            if (firstRound == False) and (playerMoney == 0):
                print('You have no more money to bet with this session.')
                betting = False
                choice = input('Do you still want to play without betting? ')
                if choice == 'yes':
                    status = 'initialize'
                elif choice == 'no':
                    status = 'exit'
                    break
            else:
                choice = input('Will you be betting? ')
            if choice == 'yes':
                betting = True
                status = 'initialize'
                if firstRound == True:
                    playerMoney += 10000
                    dealerMoney += 100000
                    print('Betting has been turned on. You have been given $10,000 dollars for this session.')
            elif choice == 'no':
                betting = False
                status = 'initialize'
                print('Very well. Please enjoy the game.')
            else:
                print('Please Enter \'yes\' or \'no\'')
                
        #Starting Hand
        while (status == 'initialize'):
            playerWon = 0
            playerLost = 0
            while betting == True:
                bet = input('How much will you be betting for this game? ')
                if bet.isdigit() == False:
                    print('Please enter a positive number.')
                elif int(bet) > playerMoney:
                    print('You cannot bet that much.')
                else:
                    bet = int(bet)
                    playerMoney -= bet
                    dealerMoney -= bet
                    print('Player: ${0}'.format(playerMoney))
                    print('Dealer: ${0}'.format(dealerMoney))
                    break
            player.hand.append(player.drawCard(deck))
            deck.remove(player.hand[0])
            player.hand.append(player.drawCard(deck))
            playerTotal = computeScore(player.hand)
            deck.remove(player.hand[1])
            print('You were dealt: ' + ', '.join(player.hand))
            print('Your Hand Total: {0}'.format(playerTotal))
            dealer.hand.append(player.drawCard(deck))
            dealerTotal = computeScore(dealer.hand)
            deck.remove(dealer.hand[0])
            print('The dealer\'s hand is: ' + ', '.join(dealer.hand))
            print('Dealer\'s Hand Total: {0}'.format(dealerTotal))
            status = 'yourTurn'
        
        #Player Decides to hit or stay
        while (status == 'yourTurn'):
            choice = input('Will you hit or stay? ')
            if choice == 'hit':
                player.hand.append(player.drawCard(deck))
                playerTotal = computeScore(player.hand,)              
                deck.remove(player.hand[-1])
                print('Your hand is now: ' + ', '.join(player.hand))
                print('Your Hand Total: {0}'.format(playerTotal))
                if playerTotal > 21:
                    status = 'youLose'
                else: status = 'yourTurn'
            elif choice == 'stay':
                status = 'dealersTurn'
            else:
                print('Please enter \'hit\' or \'stay\'')

        #After player stays, dealer's turn 
        while (status == 'dealersTurn'):
            if (dealerTotal >= 17):
                if dealerTotal >21 or (dealerTotal <= playerTotal):
                    status = 'youWin'
                else:
                    status = 'youLose'
            elif(dealerTotal < 17):
                dealer.hand.append(player.drawCard(deck))
                dealerTotal = computeScore(dealer.hand)
                deck.remove(dealer.hand[-1])
                print('The dealer\'s hand is: ' + ', '.join(dealer.hand))
                print('Dealer\'s Hand Total: {0}'.format(dealerTotal))
                status = 'dealersTurn'

        #After player wins
        while status == 'youWin':
            print('You Win')
            playerWins += 1
            playerWon += bet
            playerWonTotal += bet
            playerMoney += bet*2
            print('Player: ${0}'.format(playerMoney))
            print('Dealer: ${0}'.format(dealerMoney))
            status = 'playAgain'

        #After player loses
        while status == 'youLose':
            print('You Lose')
            playerLosses += 1
            playerLost += bet
            playerLostTotal += bet
            dealerMoney += bet*2
            print('Player: ${0}'.format(playerMoney))
            print('Dealer: ${0}'.format(dealerMoney))
            status = 'playAgain'
        
        #Will the player play again?
        while (status == 'playAgain'):
            #If the blackjack.txt file doesn't exit, create it
            if (os.path.isfile('blackjack.txt')) == False:
                f = open("blackjack.txt", "w+")
                f.write('BlackJack Results: \n')
            choice = input('Do you want to play again? ')
            if choice == 'yes':
                #Output game stats
                now = datetime.datetime.now()
                f = open("blackjack.txt", "a")
                f.write('{0} Game Stats == Money Left: ${1}, Player Won: ${2}, Player Lost: ${3}\n'.format(now , playerMoney, playerWon, playerLost) )
                firstRound = False
                playerTotal = 0
                dealerTotal = 0
                status = 'initialize'
            elif choice == 'no':
                #Output game stats
                now = datetime.datetime.now()
                f = open("blackjack.txt", "a")
                f.write('{0} Game Stats == Money Left: ${1}, Player Won: ${2}, Player Lost: ${3}\n'.format(now , playerMoney, playerWon, playerLost) )
                status = 'exit'
            else:
                print('Please enter \'yes\' or \'no\'')

        while (status == 'exit'):
            #Output the session stats and exit game
            now = datetime.datetime.now()
            f = open("blackjack.txt", "a")
            f.write('{0} SESSION STATS == Money Left: ${1}, Player Won: ${2}, Player Lost: ${3}, Player Won {4} game(s), Player Lost {5} game(s),\n'.format(now , playerMoney, playerWonTotal, playerLostTotal, playerWins, playerLosses) )
            print('Exiting Game.')
            playing = False
            status = ''

main()
        
