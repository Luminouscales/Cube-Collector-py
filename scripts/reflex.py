from datetime import datetime
import time, random, math

import scripts.data as d
import scripts.funcs as f

format_str = "%Y-%m-%d %H:%M:%S:%f"

def reflexrun():
    while True:
        f.clear()
        plinput = input( "FIXME reflex text. Press enter when you're ready, or 'exit'")
        if plinput.lower() == "exit" or plinput.lower() == "e": 
            return
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
            reward = max( 1, math.floor(difference/6) + seconds*5 )

            d.addcredits( reward )

            input(f"Your time is: {miliseconds}ms. That nets you {reward} Credits! ")