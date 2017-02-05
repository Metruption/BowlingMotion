
rolls=[0]*21
frames=[0]*10
currentRoll=0
currentFrame=0
def roll(pins):
    global rolls
    global frames
    global currentRoll
    global currentFrame
    
    if pins==10 and currentFrame!=9 and currentRoll<21:
        rolls[currentRoll]=pins
        currentRoll+=2
        currentFrame+=1
    elif currentRoll<21:
         rolls[currentRoll]=pins
         currentRoll+=1
    if currentRoll%2==0 and currentRoll<21:
        currentFrame+=1
        print ("new Frame")
        calculate()
def calculate():
    global rolls
    global frames
    global currentRoll
    global currentFrame
    score=0
    for num in range(0,10):
        if rolls[num*2]==10:
            if num==0:
                if rolls[num*2+2]==10:
                    score=10+rolls[num*2+2]+rolls[num+4]
                else:
                    score=10+rolls[num*2+2]+rolls[num+3]
            else:
                if rolls[num*2+2]==10:
                    score=score+10+rolls[num*2+2]+rolls[num+4]
                else:
                    score=score+10+rolls[num*2+2]+rolls[num+3]
        
                    
        elif(rolls[num*2]+rolls[(num*2)+1]==10):
            if num==0:
                score=10+rolls[num*2+2]
            else:
                score=score+10+rolls[num*2+2]
        else:
            score=score+rolls[num*2]+rolls[num*2+1]
        print (str(score)+":"+str(num))
    score=score+rolls[20]
    print("final"+str(score))
    return score
        
                
                
                
                
        
        
        
        
    
    
