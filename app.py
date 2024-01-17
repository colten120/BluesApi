import requests
import time
import threading
import datetime
import math
from tkinter import *

# Optional properties
playOpponentGoal = True
opponentGoalMessage = 'BOO!'
customMessage = ''

# Operational properties
volume = 50
delay = 0

# State properties
bluesScore = 0
opponentScore = 0
opponentAbbr = ''
goalTime = False
intermission = False
intermissionJustEnded = False
intermissionTimer = 0
intermissionTime = 900 #15 minutes in seconds
intermissionTimestamp = time.time()

processing = False
firstCheck = True

root = Tk()
canvas = Canvas(root, bg="black", height=500, width=500)
canvas.pack()

def get_data(api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            #print("sucessfully fetched the data")
            return response.json()
        else:
            print(f"Hello person, there's a {response.status_code} error with your request")

def isBluesGameGoing(games):
    for game in games:
        if(game['status']['state'].lower() != 'final'):
            if(game['teams']['away']['teamName'] == 'Blues' or game['teams']['home']['teamName'] == 'Blues'):
                return game
    return ''

def checkScore(game):
    global bluesScore
    global opponentScore
    global opponentAbbr
    global goalTime
    global playOpponentGoal
    global opponentGoalMessage
    global firstCheck
    
    if(opponentAbbr == ''):
        if(game['teams']['away']['abbreviation'] != 'STL'):
            opponentAbbr = game['teams']['away']['abbreviation']
        else:
            opponentAbbr = game['teams']['home']['abbreviation']
    
    score = game['scores']['STL']
    if(score > bluesScore):
        if(firstCheck == False):
            #Set off horn and lights
            print('------------------------')
            print('------------------------')
            print('------------------------')
            print('BLUES GOAL!!!')
            print('------------------------')
            print('------------------------')
            print('------------------------')
            goalTime = True
            displayGoal('GOAL!', True)
        bluesScore = score
    if(score < bluesScore):
        bluesScore = score
    
    oScore = game['scores'][opponentAbbr]
    if(oScore > opponentScore):
        if(firstCheck == False):
            #Set off horn and lights
            print('------------------------')
            print('------------------------')
            print('------------------------')
            print(opponentAbbr + ' goal')
            print('------------------------')
            print('------------------------')
            print('------------------------')
            if(playOpponentGoal):
                goalTime = True
                displayGoal(opponentGoalMessage, False)
        opponentScore = oScore
    if(oScore < opponentScore):
        opponentScore = oScore
    
    firstCheck = False

def getIntermissionTime():
    global intermissionTimestamp
    global intermissionTime
    global intermission
    global intermissionJustEnded
    
    currentTimestamp = time.time()
    timeElapsed = currentTimestamp - intermissionTimestamp
    timeLeft = intermissionTime - timeElapsed
    
    minutes = math.floor(timeLeft/60)
    seconds = math.floor(timeLeft - (60*minutes))
    
    print('Game returns in: ' + str(minutes) + ':' + str(seconds))
    displayIntermissionTimer(minutes, seconds)
    
    if(minutes <= 0 and seconds <= 0):
        intermissionTime = 900
        intermission = False
        intermissionJustEnded = True
        
def displayTime(game):
    global canvas
    global root
    global bluesScore
    global opponentScore
    global opponentAbbr
    
    canvas.delete("all")
    
    minutes = game['status']['progress']['currentPeriodTimeRemaining']['min']
    seconds = game['status']['progress']['currentPeriodTimeRemaining']['sec']
    
    #displayIntermissionTimer(minutes, seconds)
    print('Game time: ' + str(minutes) + ':' + str(seconds) + '  STL: ' + str(bluesScore) + '  ' + opponentAbbr + ' ' + str(opponentScore))

    timeTxt =  str(minutes) + ':' + str(seconds) + '\n\n\n\n'
    nameTxt = 'STL\t'+opponentAbbr+'\n\n'
    scoreTxt = '\n\n' + str(bluesScore)+'        '+str(opponentScore)
    canvas.create_text(250, 250, anchor="center", text=timeTxt, fill="#FFFFFF", font=("Helvetica", 32), justify='center')
    canvas.create_text(250, 250, anchor="center", text='\n\nSTL\t     \n\n', fill="blue", font=("Helvetica", 38), justify='center')
    canvas.create_text(250, 250, anchor="center", text='\n\n\t'+opponentAbbr+'\n\n', fill="#FFFFFF", font=("Helvetica", 38), justify='center')
    canvas.create_text(250, 250, anchor="center", text=scoreTxt, fill="#FFFFFF", font=("Helvetica", 64), justify='center')
    #txt = 'STL\t\t'+opponentAbbr+'\n'+bluesScore+'\t\t'+opponentScore
    #canvas.create_text(250, 250, anchor="center", text=txt, fill="#FFFFFF", font=("Helvetica", 32), justify='center')

def displayGoal(message, isBlues):
    global canvas
    global root
    global goalTime
    
    canvas.delete("all")
    
    sleepTime = 0.5
    
    color1 = 'blue'
    color2 = 'yellow'
    
    if(not isBlues):
        color1 = 'red'
        color2 = 'white'
    
    displayGoalText(message, color1, color2)
    time.sleep(sleepTime)
    displayGoalText(message, color2, color1)
    time.sleep(sleepTime)
    displayGoalText(message, color1, color2)
    time.sleep(sleepTime)
    displayGoalText(message, color2, color1)
    time.sleep(sleepTime)
    displayGoalText(message, color1, color2)
    time.sleep(sleepTime)
    displayGoalText(message, color2, color1)
    time.sleep(sleepTime)
    
    goalTime = False
    resetCanvasBg()

def displayGoalText(message, bgColor, txtColor):
    global canvas
    global root
    
    canvas.delete("all")
    txt = 'GOAL!'
    
    canvas.configure(bg=bgColor)
    canvas.create_text(250, 250, anchor="center", text=message, fill=txtColor, font=("Helvetica", 64), justify='center')

    root.update()
        
def displayIntermissionTimer(min, sec):
    global canvas
    
    canvas.delete("all")
    
    txt = 'Game will return in:\n'+str(min)+':'+str(sec);
    canvas.create_text(250, 250, anchor="center", text=txt, fill="#FFFFFF", font=("Helvetica", 32), justify='center')

def displayNoGame():
    global canvas
    canvas.delete("all")
    canvas.create_text(250, 250, anchor="center", text="No game found.", fill="#FFFFFF", font=("Helvetica", 32))

def resetCanvasBg():
    global canvas
    canvas.configure(bg='black')

def heartbeat():
    global processing
    global intermissionTimestamp
    global intermission
    global intermissionJustEnded
    global root
    
    threading.Timer(1.0, heartbeat).start()
    if(intermission):
        getIntermissionTime()
        #time.sleep(1)
    elif(goalTime):
        print('Goal time!')
    elif(not processing):
        processing = True
        #print('Getting data...')
        data = get_data('https://nhl-score-api.herokuapp.com/api/scores/latest')
        game = isBluesGameGoing(data['games'])
        if(game != ''):
            if(game['status']['state'] == 'LIVE'):
                if(game['status']['progress']['currentPeriodTimeRemaining']['pretty'] == 'END'):
                    if(intermissionJustEnded == False):
                        #Intermission
                        print("Intermission true")
                        intermission = True
                    else:
                        print('Game will return shortly!')
                else:
                    intermissionJustEnded = False
                    intermissionTimestamp = time.time()
                    checkScore(game)
                    displayTime(game)
            else:
                print('No game currently')
                displayNoGame()
        else:
            print('No game currently')
        processing = False
        root.update()

def main():
    global root
    
    heartbeat()
    root.mainloop()
    
main()
