import time, random, math
from datetime import datetime, timedelta

import scripts.data as d
dates = d.dates
daily = d.daily
inv_inputs = d.inv_inputs

# Open a box once per day for rewards. Increases each time you open (not a streak though).
# 86400 seconds in a day
def dailybox():
    format_str = "%Y-%m-%d %H:%M:%S"
    dbindex = -1
    eligible = False
    curtreats = int( dates[2][1] )

    # Get position of dailybox in dates
    for row in dates:
        if row[0] == 'dailybox':
            dbindex = dates.index( row )
    # If new setup  
    if dbindex == -1:
        dates.append( ['dailybox', datetime.now().strftime( format_str ) ] )
        d.savetime()
        dbindex = len(dates)-1
        # And give reward
        eligible = True
    else:
        # Counting the difference of seconds. If more than one day, give reward.
        format_str = "%Y-%m-%d %H:%M:%S"
        date1 = datetime.strptime(dates[dbindex][1], format_str)
        date2 = datetime.strptime(str(datetime.now().strftime( format_str )), format_str)
        time_difference = (date2 - date1).total_seconds()
        # If more than two hours have passed
        if time_difference >= daily:
            eligible = True
            dates[dbindex][1] = datetime.now().strftime( format_str )
            d.savetime()
    # Finally check through bool eligible if can receive.
    if eligible:
        print( "You open your daily box. It contains...")
        time.sleep( 2 )
        randint = random.randint( 1, 100 )
        match randint:
            case randint if randint <= 2: # Affix tag drop
                print( "An Affix Tag!" )
                d.additem( "Affix Tag", 1 )
            case randint if randint < 25:

                treats1percent = 1000 # every amount of this increases 4pbox chance by +1%
                treats1percentbonus = int(curtreats/treats1percent)

                count3 = max(1, int( 1 + treats1percentbonus/6 ) ) # count for 3pbox / for every 900c one more, min 1
                count4 = max(1,int(count3 / 2))

                if random.randint(1, 100) > int(94 - treats1percentbonus):
                    if count4 == 1:
                        joiner2 = "A"
                        joiner = ""
                    else:
                        joiner2 = str(count4)
                        joiner = "es"

                    d.additem( "Quadruple Prefixed Box", count4 )
                    print( f"{joiner2} Quadruple Prefixed Box{joiner}!" )
                else:
                    if count3 == 1:
                        joiner2 = "A"
                        joiner = ""
                    else:
                        joiner2 = str(count3)
                        joiner = "es"

                    d.additem( "Triple Prefixed Box", count3 )
                    print( f"{joiner2} Triple Prefixed Box{joiner}!" )

            case randint if randint >= 25 and randint <= 100:
                # 50% chance for treat tickets
                if random.randint( 1, 2 ) == 1:
                    if curtreats < 2000:
                        randint = random.randint( 200, 2000 )
                        print( f"{randint} credits!" )
                        d.addcredits( randint )
                    else:
                        randint = random.randint( curtreats/10, curtreats/4)
                        print( f"{randint} credits!" )
                        d.addcredits( randint )
                else:
                    if curtreats < 2000:
                        randint = random.randint( 5, 20 )
                        print( f"{randint} Treat Tickets!" )
                        d.additem( "Treat Ticket", randint )
                    else:
                        randint = random.randint( math.floor(curtreats/200), math.floor(curtreats/100) )
                        print( f"{randint} Treat Tickets!" )
                        d.additem( "Treat Ticket", randint )
        time.sleep( 3 )
    else:
        soondate = int(float((( date1 + timedelta( seconds=daily) ) - date2).total_seconds()))
        # Formatting seconds for dialogue
        if soondate >= 3600:
            amount = math.floor( soondate / 3600 )
            nominal = "hours"
        elif soondate < 3600 and soondate >= 60:
            amount = math.floor( soondate / 60 )
            nominal = "minutes"
        elif soondate <= 60:
            amount = soondate 
            nominal = "seconds"
        print( f"The daily box is still locked, you should check back in {amount} {nominal}." )
        time.sleep( 2 )
