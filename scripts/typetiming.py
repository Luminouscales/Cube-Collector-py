import random, math, os
from datetime import datetime
import scripts.data as d

format_str = "%Y-%m-%d %H:%M:%S"
prefixtable = d.prefixtable
prefixmax = d.prefixmax

def typetiming():
    while True:
        os.system("cls")
        aim = ""
        lettercount = 0
        for i in range(1, 20):
            word = prefixtable[ random.randint(0, prefixmax) ].lower()
            lettercount += len(word) + 1
            aim = aim + " " + word

        timestart = datetime.strptime( datetime.now().strftime( format_str ), format_str )
        plinput = input(aim[1:len(aim)] + "\n")
        timeend = datetime.strptime( datetime.now().strftime( format_str ), format_str )

        timeseconds = ( timeend - timestart ).total_seconds()

        count = 0
        npoints = 0
        for letter in plinput:
            count += 1
            if letter != aim[count]:
                print( letter, aim[count])
                npoints += 1


        lps = math.floor( lettercount / timeseconds )
        reward = 100 * (lps/5) * (1.5 - npoints/5)
        if lps > 9:
            reward *= 2.5
        reward = max( 1, reward )
        reward = int( float(reward) )

        d.addcredits( reward )
        plinput = input(f"Errors: {npoints}, Time: {timeseconds}, Letters: {lettercount}, LPS: {lps}, Reward: {reward} credits! Continue or exit ")
        match plinput.lower():
            case "exit": return
            case _: pass
        

# Average of 5 letters per second
# For 5 lps: 100 credits
# Each error decreases reward by 10%
