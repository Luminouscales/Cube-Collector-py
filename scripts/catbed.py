from datetime import datetime

import scripts.data as d
import scripts.funcs as f

format_str = "%Y-%m-%d %H:%M:%S"

def catbed():
    f.clear()
    plinput = input("Welcome to the cat bed! Sit down and rest with us :3 As your mind clears, you get some Credits!")

    match plinput:
        case "exit" | "e": return
        case _: catbedrun()


def catbedrun():
    f.clear()
    timestart = datetime.now()

    input("Slow purrs...")

    timeend = datetime.now()
    timedif = (timeend - timestart).total_seconds()

    if timedif >= 7200:
        input("Oh, you seem to have overslept...")
    else:
        credits = max(1, int( timedif*2 ) )
        d.addcredits( credits )
        input(f"Thank you for spending time with us! You get {credits} Credits :3")