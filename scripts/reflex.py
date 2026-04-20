from datetime import datetime
import time, random, os, math

import scripts.data as d

format_str = "%Y-%m-%d %H:%M:%S:%f"

def reflexrun():
    while True:
        os.system("cls")
        plinput = input( "FIXME reflex text. Press enter when you're ready, or 'exit'")
        if plinput.lower() == "exit": 
            pass
        else:
            seconds = random.randint(1, 8)
            randomtime = seconds + random.random()
            print( "Wait..." )
            time.sleep( randomtime )

            timenow = datetime.strptime( datetime.now().strftime( format_str ), format_str )
            input("now")
            timethen = datetime.strptime( datetime.now().strftime( format_str ), format_str )

            reflextime = timethen - timenow
            miliseconds = ( reflextime.seconds * 1000000 + reflextime.microseconds )/1000
            miliseconds = math.floor( miliseconds )

            difference = 450 - miliseconds
            reward = max( 1, 50 + math.floor(difference/4) + seconds*10 )

            d.addcredits( reward )

            input(f"Your time is: {miliseconds}ms. That nets you {reward} Credits! ")