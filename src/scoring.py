#@todo(aaron): rewrite this from scratch.
'''
fs design:
scoremanager class has a list of 10 frames

each frame has a pointer to the previous frame and the next frame, none if there's not any
(frst frame has previous = none, last is next = none)

probably have firstframe, normalframe, lastframe classes that inherit from frame
maybe not normalframe
'''

def legacy_scoring():
    rolls[0]*21
    frames[0]*10
    currentRoll=0
    currentFrame=0
    def roll(pins):
        if pins==10:
            rolls[currentRoll]=pins
            currentRoll+=2
            currentFrame+=1
         rolls[currentRoll]=pins
         currentRoll+=1
        if currentRoll%2=0:
            currentFram+=1
            calculate()
    def calculate():
        for num in range(0,10):
            if rolls[num*2]==10:
                if num==0:
                    if rolls[num*2+2]==10:
                        frames[num]=10+rolls[num*2+2]+rolls[num+4]
                    else:
                        frames[num]=10+rolls[num*2+2]+rolls[num+3]
                else:
                    if rolls[num*2+2]==10:
                        frames[num]=frames[num-1]+10+rolls[num*2+2]+rolls[num+4]
                    else:
                        frames[num]=frames[num-1]+10+rolls[num*2+2]+rolls[num+3]
            
                        
            elif(rolls[num*2]+rolls[(num*2)+1]==10):
                if num==0:
                    frames[num]=10+rolls[num*2+2]
                else:
                    frames[num]=frames[num-1]+10+rolls[num*2+2]
            else:
                frames[num]=rolls[num*2]+rolls[nums*2+1]
                
                
                
                
'''
aaron's big bad wishlist!
ability to call a function get_score_result(numpins)
then it returns a an event type (see events.py)
'''
        
        
    
    
