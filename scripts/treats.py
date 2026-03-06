import os, math, random, time
from datetime import datetime, timedelta
from scripts import data as d

dates = d.dates
daily = d.daily
inventory = d.inventory

# Treats - investing in kitty food
def treats():
    os.system('cls')

    print("( \\")
    print(" \ \\")
    print(" / /                |\\\\")
    print("/ /     .-`````-.   / ^`-.")
    print("\ \    /         \_/  {|} `o")
    print(" \ \  /   .---.   \\ _  ,--'")
    print("  \ \/   /     \,  \(     ")
    print("   \   \/\      (\  )")
    print("    \   ) \     ) \\ \\")
    print("jgs  ) /__ \__  ) (\ \___")
    print("    (___)))__))(__))(__)))")

    treatcount = int( dates[2][1] )
    #catsfed = math.floor( treatcount / 100 )
    catsfed = math.floor( math.sqrt(treatcount*25) )
    tickets = 0
    ticketinfo = d.checkinv( "Treat Ticket" )

    # Seek treats
    if ticketinfo['found']:
        tickets = ticketinfo['amount']
    else:
        tickets = 0

    print(f"Meow! Welcome to the Treat Stockpile! We have currently amassed {treatcount} treats, feeding {catsfed} kitties!")

    # Treat rewards
    # Counting the difference of seconds. If more than one day, give reward.
    if catsfed > 0:
        format_str = "%Y-%m-%d %H:%M:%S"
        date1 = datetime.strptime(dates[3][1], format_str)
        date2 = datetime.strptime(str(datetime.now().strftime( format_str )), format_str)
        time_difference = (date2 - date1).total_seconds()
        # If more than two hours have passed
        if time_difference >= daily:
            dates[3][1] = datetime.now().strftime( format_str )
            d.savetime()

            #reward = math.ceil(( catsfed * 25 ) * random.uniform( 0.75, 1.5 ))
            reward = math.ceil(random.randint( catsfed, catsfed * 3 ) * random.uniform( 0.75, 1.5 ))
            d.addcredits( reward )

            print( f"MRAW, thank you for contributing to our stockpile! Your happy kittens have brought you {reward} Credits in thanks!")
        else:
            soondate = (( date1 + timedelta( seconds=daily) ) - date2).total_seconds()
            # Formatting seconds for dialogue
            if soondate >= 3600:
                amount = math.floor( soondate / 3600 )
                nominal = "hours"
            elif soondate < 3600 and soondate >= 60:
                amount = math.floor( soondate / 60 )
                nominal = "minutes"
            elif soondate <= 60:
                amount = math.floor( soondate / 60 )
                nominal = "seconds"
            print( f"Your kittens are currently resting contently. They might offer something again in {amount} {nominal}." )

    print(f"You have {inventory[0][1]} Credits and {tickets} Treat Tickets.") # and treats

# FIX more treat rewards?

    print("donate, redeem, exit")

    plinput = input("").lower()

    match plinput:
        case "exit":
            return
        case "donate":
            treatsdonate()
        case "redeem":
            treatsredeem()
        case _:
            print( "I'm not sure what you mean..." )
            time.sleep( 1 )
            os.system('cls')
            treats()

def treatsdonate():
    print( "Meow, how much would you like to contribute?" )
    plinput = input("").lower()
    # If "all" then all money
    if plinput == "all":
        plinput = inventory[0][1]
    elif d.checkifproperint(plinput):
        plinput = int(plinput)
    
    if d.checkifproperint( plinput ) or plinput == "all" :
        plinput = int(plinput)
        # If less than what you have
        if plinput > inventory[0][1]:
            print( "You sadly don't have that much..." )
            time.sleep( 2 )
            os.system('cls')
            treats()
        else:
            d.addcredits( -plinput )
            dates[2][1] = plinput + int( dates[2][1] ) 
            d.savetime()
            print( "Thank you for donating!")
            time.sleep( 2 )
            os.system( 'cls' )
            treats()
    else:
        print( "That's not a correct value..." )
        time.sleep( 2 )
        os.system('cls')
        treats()

# FIX super rare affixes?

# Redeeming Treat Tickets. Each ticket is worth 100 Credits and can be sold for 25
def treatsredeem():
    ticketloc = d.checkinv( "Treat Ticket" )
    ticketamount = 0

    if ticketloc['found'] == False:
        print( "You don't seem to have any Treat Tickets at this time..." )
        time.sleep( 2 )
        os.system('cls')
        treats()
    else:
        ticketamount = ticketloc['amount']
        print( "Meow, how many Treat Tickets would you like to redeem?" )
        plinput = input("").lower()
        # If "all" then all money
        if plinput == "all":
            plinput = ticketamount
        elif d.checkifproperint(plinput):
            plinput = int(plinput)
    
        if d.checkifproperint( plinput ) or plinput == "all":
            plinput = int(plinput)
            # If less than what you have
            if plinput > ticketamount:
                print( "You sadly don't have that much..." )
                time.sleep( 2 )
                os.system('cls')
                treats()
            else:
                inventory[ticketloc['index']][1] = int( inventory[ticketloc['index']][1] ) - plinput
                if inventory[ticketloc['index']][1] == 0:
                    inventory.pop( ticketloc['index'] )
                d.saveinv()
                dates[2][1] = int( dates[2][1] ) + plinput * 25
                d.savetime()
                print( "Thank you so much for redeeming!")
                time.sleep( 2 )
                os.system( 'cls' )
                treats()
        else:
            print( "That's not a correct value..." )
            time.sleep( 2 )
            os.system('cls')
            treats()

treats()