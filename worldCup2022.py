import requests
from bs4 import BeautifulSoup
from time import sleep
import RPi.GPIO as gpio

websiteURL = "https://www.foot-direct.com/live/"
team1PreviousScore = "0"
team2PreviousScore = "0"
supportedTeam = "Argentine"
relayPin = 18

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(relayPin,gpio.OUT, initial=gpio.LOW)

def triggerEvent():
    gpio.output(relayPin, gpio.HIGH)
    sleep(1)
    gpio.output(relayPin, gpio.LOW)
    sleep(1)
    gpio.output(relayPin, gpio.HIGH)
    sleep(1)
    gpio.output(relayPin, gpio.LOW)
    sleep(1)
    gpio.output(relayPin, gpio.HIGH)
    sleep(1)
    gpio.output(relayPin, gpio.LOW)
    sleep(1)
    gpio.output(relayPin, gpio.HIGH)
    sleep(1)
    gpio.output(relayPin, gpio.LOW)

while(True):

    page = requests.get(websiteURL)
    parser = BeautifulSoup(page.content,'html.parser')
    matchInfos = parser.find("div", {"data-groupid":"7912263966302864319"})

    if(matchInfos == None):
        print("Pas de match en cours")

    else:
        team1Name = matchInfos.find(class_="match__team match__team--home").find(class_="match__teamInfos").text.strip()
        team2Name = matchInfos.find(class_="match__team match__team--away").find(class_="match__teamInfos").text.strip()
        team1ActualScore = matchInfos.find(class_="match__team match__team--home").find(class_="match__score").text.strip()
        team2ActualScore = matchInfos.find(class_="match__team match__team--away").find(class_="match__score").text.strip()
        regularTime = matchInfos.find(class_="chrono__min")

        print(team1Name+" : "+team1ActualScore)
        print(team2Name+" : "+team2ActualScore)
    
        chronoPeriod = matchInfos.find(class_="chrono__period")
    
        if(chronoPeriod==None):
            additionnalTime = matchInfos.find(class_="chrono__additionnalTime").text.strip()[:-1]
       
            if(additionnalTime != "+"):
                print(regularTime.text.strip() + additionnalTime)
                   
            else:
                print(regularTime.text.strip()[:-1])
            
        else:
            print("MT")
        
        if(team1ActualScore != team1PreviousScore):
            if(team1Name == supportedTeam):
                team1PreviousScore = team1ActualScore
                TriggerEvent()

            else:
                print(team1Name+" vient de marquer un but !")
                team1PreviousScore = team1ActualScore
            
        if(team2ActualScore != team2PreviousScore):
            if(team2Name == supportedTeam):
                team2PreviousScore = team2ActualScore
                TriggerEvent()
                
            else:
                print(team2Name+" vient de marquer un but !")
                team2PreviousScore = team2ActualScore
               
    print(" ")
    sleep(60) 