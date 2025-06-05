import os, sys, random, time, math
from datetime import datetime, timedelta

selfpath = os.path.dirname(sys.argv[0])
inventorypath = selfpath + "/inventory.txt"
registrypath = selfpath + "/registry.txt"
timepath = selfpath + "/time.txt"
verdate = "05.06.25"
# For inv/reg pages; how many items per page? 20 fits snugly in normal terminal size
limit = 20
format_str = "%Y-%m-%d %H:%M:%S"
# var used for daily rewards
daily = 3600 * 1

# 23.11.24 We've come so far... I remember when this little idea was just one primitive roll function.
# This thing is fairly playable and semi-balanced, and not the most boring.
# I've decided to change it from Cubes to Kittens. Only makes sense, right? And it will be much more charming.
# Just needs a lot of work. But it's fine.

# 05.06.25
# Life sucks but at least I get to be a code kitten


# Read the inventory and output it into the "inventory" var
inventory = []
if os.path.exists(inventorypath):
    with open( inventorypath, 'r' ) as file:
        for line in file:
            row = line.strip().split('\t') # What?
            inventory.append( row )
            # Turn every amount number into int
            row[1] = int( row[1] )

# Save Time file
def savetime():
    with open( timepath, 'w' ) as file:
        for row in dates:
            row_str = '\t'.join(map(str, row))
            file.write( row_str + '\n')

dates = []
# Read the Time file for tracking dailies and stuff.
if os.path.exists( timepath ):
    with open( timepath, 'r' ) as file:
        for line in file:
            row = line.strip().split('\t')
            dates.append( row )
    # Check if setup value is 0 meaning new save. I'm too lazy to do this the normal way.
    if dates[0][1] == "0":
        dates[0][1] = datetime.now().strftime( format_str )
        savetime()

# Load registry. The registry is a list of all ever unboxed cubes
registry = []
if os.path.exists( registrypath ):
    with open( registrypath, 'r' ) as file:
        for line in file:
            row = line.strip().split('\t')
            registry.append( row )
            row[1] = int( row[1] )
            row[2] = int( row[2] )

# Take all cubes from inventory var and save it as inventory.txt
def saveinv():
    with open( inventorypath, 'w' ) as file:
        for row in inventory:
            row_str = '\t'.join(map(str, row)) # What the fuck is map() ?
            file.write( row_str + '\n')

# Take all cubes from reg and save it as registry.txt
def savereg():
    with open( registrypath, 'w' ) as file:
        for row in registry:
            row_str = '\t'.join(map(str, row))
            file.write( row_str + '\n')

# Add cube to registry
def addreg( cube ):
    for row in registry:
        # If cube already in registry add one more to count and end function
        if row[0] == cube:
            row[1] = row[1] + 1
            savereg()
            return 
    # If new, add to reg
    # First one is name, second one is number of times found, second is unique ID.
    # Unique ID is counted by adding one to last cube's ID.
    registry.append( [ cube, 1, registry[len(registry) - 1][2] + 1 ] )
    savereg()

# Add or remove credits to inv
def addcredits(price):
    inventory[0][1] += price
    saveinv()

# Import list of prefixes
with open( selfpath + "/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1

# Import affixes
with open( selfpath + "/affixes.txt", 'r' ) as file:
    lines = file.readlines()
    affixtable = [line.strip() for line in lines]
    affixmax = len(affixtable) - 1

# Let's do it like this.
# Each box has four values corresponding to the drop rate in each tier.
# This way we can controll and adjust them manually.
# Means we can't prevent a prefix from rolling, we can just make it cosmically unlikely

# Function for rolling a cube
def rollcube( odds ):
    # Odds is a table of chances for a box
    # [ one prefix, two, three, four ]

    # Each box has a odds[3] * 5 percent chance of dropping an affix tag.
    if random.randint( 1, odds[3] * 5 ) == 1:
        print( "You found an Affix Tag! You lucky cat." )
        addcube( "Affix Tag", 1 )
        time.sleep( 1 )
    else:
        prefixes = []
        for idx in range(len(odds)):
            if random.randint( 1, odds[idx] ) != 1:
                break
                
            prefixes.append(prefixtable[ random.randint( 0, prefixmax ) ])

        cube = ' '.join(prefixes) + ' Kitty' if len(prefixes) > 0 else 'Kitty'
        addcube(cube, 1)

# Function that adds a cube to inventory
# fav decides if cube should be favourited when added
def addcube( cube, amount=1, fav=False ):
    
    for row in inventory:
        # If cube already in inventory add one more to count and end function
        if row[0] == cube:
            row[1] = row[1] + amount
            print( "You got a " + cube + "!" )
            saveinv()
            # Add to reg
            return
    # If new then add the cube to inventory. The 1 is the amount of new cubes. So, just one.
    if fav:
        inventory.append( [cube, 1, "fav"] )
    else:
        inventory.append( [cube, 1] )
    saveinv()
    # If it's not in reg yet, say it's brand new.
    if checkreg( cube )["found"]:
        print( "You got a " + cube + "!" )
    else:
        print( "[NEW] You got a " + cube + "!" )
    addreg( cube )

# Function that adds an item to inventory
def additem( cube, count ):
    # Make cube name capitalised for consistency
    cube = cube.upper()
    for row in inventory:
        # If cube already in inventory add one more to count and end function
        if row[0] == cube:
            row[1] = row[1] + count
            saveinv()
            return 
    inventory.append( [cube, count] )
    saveinv()

# When the player inputs "help". Lists an explanation of the game and commands.
def helpguide():
    inputs1( input("Available commands: \ninventory\nregistry\nstore\njobs\ndailybox\ntreats\n") )

# Function for checking if the given item is in the inventory
def checkinv(item):
    # We can input either int (for index) or string (for name)
    if checkifproperint( item ):
        try:
            return { "found": True, "index": int( item ) }
        except:
            return{ "found": False }
    # If it's a string
    else:
        for row in inventory:
            if item.lower() == row[0].lower():
                # Scripts using checkinv() can read this table to get the bool and the item's row
                return { "found": True, "index": inventory.index( row ), "amount": inventory[inventory.index( row )][1] }
    return { "found": False  }

# For checking if the cube is in the registry, meaning if it's a cube
def checkreg(item):
    # We can input either int (for index) or string (for name)
    if checkifproperint( item ):
        item = int(item)
        # Don't allow int index higher than length of registry
        if item <= len(registry):
            return { "found": True, "index": int( item ) - 1 }
        else:
            return{ "found": False }
    # If it's a string
    else:
        for row in registry:
            if item.lower() == row[0].lower():
                return { "found": True, "index": registry.index( row ) }
    return { "found": False  }


# Honestly these inventory inputs have become so nested it would be much more hygienic to split them up into functions and
# to throw them into a case match. //FIX Besides the fact that cases only work on newer py versions
    # Fuck the older py versions. I managed to get the different versions to work | 22.11

# "inventory" input that prints owned cubes
# printinv is a bool that decides if we should print the inventory or not
def inp_inv( printinv ):
    pages = math.ceil( len( inventory )/limit )
    if printinv:
        os.system('cls')
        print( "\nYour inventory contains:" )
        print("--------------------------------------------")
        # We'll nowe use printreg() to show the inventory in pages.
        printreg( 1, pages, inventory )
        print("--------------------------------------------")
        invinput = input("Commands: use, delete, info, exit, sort [alph, value, count], [kitty name], page [number], fav [kitty or nil]\n").lower()
    else:
        invinput = input("")
    invinput = invinput.strip().split('\t')
    command = invinput[0].lower()
    argument1 = "nil" 
    argument2 = 1
    if len( invinput ) > 1:
        argument1 = invinput[1]
        if len(invinput) > 2:
            argument2 = invinput[2]
    if command == "exit":
        mainmenu()
    elif command == "fav":
        checktable = checkinv( argument1 )
        # If printing favourites
        if argument1.lower() == "nil":
            print( "Favourite items:" )
            for row in inventory:
                if row[len(row) - 1] == "fav":
                    print( "- " + row[0] )
            time.sleep( 1 )
            inp_inv( False )
        # If favouriting a cube
        elif checktable["found"]:
            row = inventory[ checktable["index"] ]
            # If not favourited yet, meaning the last value is not "fav", add to favourites
            if row[len(row) - 1] != "fav":
                row.append( "fav" )
                print( row[0] + " added to favourites.")
                saveinv()
                inp_inv( False )
            # If favourited, remove from favourites
            else:
                row.pop( len(row) - 1 )
                print( row[0] + " removed from favourites." )
                saveinv()
                inp_inv( False )
        else:
            print( "Invalid kitty." )
            time.sleep( 1 )
            inp_inv( False )

    # If page and page number; argument1 is page number
    elif command == "page" and checkifproperint( argument1 ):
        if int( argument1 ) <= pages:
            os.system('cls')
            print( "\nYour inventory contains:" )
            print("--------------------------------------------")
            printreg( int( argument1 ), pages, inventory )
            print("--------------------------------------------")
            inp_inv( False )
        else:
            print( "Invalid page." )
            time.sleep(1)
            inp_inv( False )
    # Input for using an object
    elif command == "use":
        # argument1 is cube name or index
        # checkinv() returns if found and index row where the item is
        checktable = checkinv( argument1 )
        # If it's an index
        if checktable["found"] and checkifproperint( argument1 ):
            print( inventory[int(argument1)][0] )
            argument1 = inventory[int(argument1)][0].lower()
        # If it was found, if it's usable   
        if checktable[ "found" ] and argument1 in inv_inputs:
            rowindex = checktable[ "index" ]
            rowd = inventory[ rowindex ]
            # argument2 is how many we use
            if checkifproperint( argument2 ) == False:
                print( "That's not valid.\n" )
                time.sleep(1)
                inp_inv( False )
            else:
                argument2 = int(argument2)
                if argument2 > 40:
                    delay = 0.01
                else:
                    delay = 0.5
                # Check if it's a box. If not, we use the item's own function
                if argument1[len(argument1)-3:len(argument1)].lower() == "box":
                    # Check if you have enough
                    if argument2 <= rowd[1]:
                        for i in range( argument2 ):
                            # Remove one use from the object; if it's last, remove it from inv
                            rowd[1] -= 1
                            if rowd[1] == 0:
                                inventory.pop(rowindex)
                            rollcube( inv_inputs[argument1] )

                            # Function for rolling Treat Tickets
                            if random.randint( 1, 30 ) == 1:
                                ticketamount = math.ceil(( ( store_prices[ argument1 ] / 10 ) * random.uniform(0.8, 1.2) ))
                                additem( "Treat Ticket", ticketamount )
                                print(f"You also found {ticketamount} Treat Tickets!")

                            time.sleep(delay)
                        time.sleep( 1.5 )
                        inp_inv( True )
                    else:
                        print( "You don't have enough of those.\n" )
                        time.sleep(1)
                        inp_inv( False )
                else: # Not a box
                    inv_inputs[argument1.lower()]( rowindex )

        else:
            print( "You can't use that." )
            time.sleep(1)
            inp_inv( False )
    # Give information about object. //FIX
    elif command == "info":
        pass

    # I shouldn't run it with elifs like that..
    elif command == "delete" or command == "del":
        # checkinv() returns if found and index row where the item is
        checktable = checkinv( argument1 )
        # If index
        if checktable["found"] and checkifproperint( argument1 ):
            print( inventory[int(invuse)][0] )
            invuse = inventory[int(invuse)][0].lower()
        # If in inventory
        if checktable["found"]:
            rowindex = checktable[ "index" ]
            row = inventory[ rowindex ]
            # If there is more than one of the item
            if row[1] > 1:
                if checkifproperint( argument2 ) == False:
                    print( "That's not valid.\n" )
                    time.sleep(1)
                    inp_inv( False )
                else:
                    argument2 = int(argument2)   
                    # Delete if right
                    inventory[rowindex][1] -= argument2
                    print( "Items deleted." )
                    # If empty, delete from inv; don't delete completely if it's money
                    if row[1] == 0 and row[0] != "CREDITS":
                        inventory.pop( rowindex )
                    if row[0] == "CREDITS":
                        inventory[rowindex][0] == 0
                    saveinv()
                    inp_inv( True )
            # If delete only one
            else:
                # If it's cash, don't remove whole line, just set to 0 or else the game will break
                if row[0] == "CREDITS":
                    inventory[rowindex][0] == 0
                else:
                    inventory.pop( rowindex )
                print( "Items deleted." )
                saveinv()
                time.sleep( 1 )
                inp_inv( True )
        else:
            print( "You don't have that." )
            time.sleep(1)
            inp_inv( False )
    # sorting
    elif command == "sort":
        # Sort alphabetically
        if argument1 == "alph":
            inventory.sort( key=lambda x: x[0] )
        # Sort by value
        elif argument1 == "value":
            inventory.sort( key=lambda x: getprice( x[0] ), reverse=True )
        elif argument1 == "count":
            inventory.sort( key=lambda x: x[1], reverse=True )
        # In any case, we have to find credits and cube and insert them into the beginning of the table
        for row in inventory:
            if row[0].lower() == "credits":
                cash = row[1]
                inventory.pop( inventory.index(row) )
                inventory.insert( 0, ["Credits", cash] )
                break
        # Now return
        saveinv()
        inp_inv( True )
    # If it's a cube name, return if this cube exists
    elif checkinv( command )["found"]:
        checktable = checkinv( command )
        row = inventory[( checktable["index"] )]
        loc = math.ceil( checktable["index"] / limit )
        print( "Found " + str( row[1] ) + " of " + row[0] + " at index [" + str( checktable["index"] ) + "], page " + str( loc ) )
        inp_inv( False )
    else:
        print( "Invalid input." )
        time.sleep(1)
        inp_inv( False )

# //FIX add categories to inventory

# Function to check if it's an int, if it's whole and bigger than 0
def checkifproperint( number ):
    # Is it int?
    try:
        number = int(number)
    except:
        return False
    # Is it whole and bigger than 0?
    else:
        if number % 1 == 0 and number > 0:
            return True
        else:
            return False

def printreg( page, maxpages, table ):
    # So we print a certain range in the list. First one is 1 - limit, then 51 - 101, then 151 - 201
    # I'd love to do a cool, smooth calculation here but this is much easier. I'm a poet.
    if page == 1:
        range1 = 0
    else:
        range1 = limit * ( page - 1 )
    range2 = limit * page

    # Different approach for reg and inv
    if table == registry:
        for row in table[range1:range2]:
            print( "[" + str( row[2] ) + "] " + row[0] + " " + str( row[1] )  )
    else: # If inventory
        for row in table[range1:range2 + 1]:
            try:
                row[2]
                print( f"[{str( table.index( row ) )}] {row[0]} {str( row[1] )} *" )
            except:
                print( "[" + str( table.index( row ) ) + "] " + row[0] + " " + str( row[1] ) )
                
    print( f"Page {str( page )} of {str(maxpages)}" )

# registry input part 2, internal, to maintain flow
def inp_reg2( pages ):
    reginput = input("Input page [number], kitty name, kitty ID, sort [alph, value, id, count] or exit\n")
    reginput = reginput.strip().split('\t')
    command = reginput[0].lower()
    argument1 = "nil" 
    if len( reginput ) > 1:
        argument1 = reginput[1]
    if command == "exit":
        mainmenu()
    # Check if exists
    elif checkreg( command )["found"]:
        checktable = checkreg(command)
        row = registry[ checktable["index"] + 1 ]
        print( "Found " + str(row[1]) + " of " + row[0] + " at index [" + str( checktable["index"] ) + "] with ID " + str( row[2] ) )
        inp_reg2( pages )
    elif command == "sort":
        # Sort alphabetically
        if argument1 == "alph":
            registry.sort( key=lambda x: x[0] )
        # Sort by value
        elif argument1 == "value":
            registry.sort( key=lambda x: getprice( x[0] ), reverse=True )
        elif argument1 == "id":
            registry.sort( key=lambda x: x[2] )
        elif argument1 == "count":
            registry.sort( key=lambda x: x[1], reverse=True )
        # Now return
        savereg()
        inp_reg()
    # Must be proper int and not more than max pages
    elif command == "page" and checkifproperint( argument1 ) and int(argument1) <= pages:
        os.system('cls')
        argument1 = int(argument1)
        printreg( argument1, pages, registry )
    else:
        print( "Incorrect input." )
        time.sleep( 1 )
        inp_reg()
    #inp_reg2(pages)

# "registry" input
def inp_reg():
    # Calculate number of pages
    # registry length
    reglen = len(registry)
    # pages, rounded up is full amount
    pages = math.ceil( reglen / limit )
    print( "The registry contains:\n--------------------------------------------")
    # First ID, then cube, then amount 
    printreg( 1, pages, registry )
    inp_reg2( pages )

# Input in store for buying a certain amount
def inp_store_buy_count( pl_input ):
    cash = inventory[0][1]
    # inputting "max" will give you the maximum amount you can buy
    if pl_input.lower() == "max" or pl_input.lower() == "all":
        pl_input = math.floor( cash / store_prices[ setcube ] )
        if pl_input < 1:
            inp_store_buy( input( "You can't afford any. Anything else?\n" ) )
            return
    if checkifproperint( pl_input ):
        # If it's bigger than 0 and if it's whole
        # Calc price and check if we have the funds
        pl_input = int( pl_input )
        price = pl_input * store_prices[ setcube ]
        price = int(price)
        locinput = input( str(pl_input) + " of " + setcube + " costs " + str( price ) + " credits. [buy or exit] " )
        if locinput == "buy":
            if cash >= price:
                # Add to inv; name and amount; remove cash
                addcredits( -price )
                additem( setcube, pl_input )
                inp_store_buy( input("Thanks for buying! Anything else?\n") )
            else:
                inp_store_buy( input( "You can't afford that. Anything else?\n" ) )
        else:
            inp_store_buy( input( "Alright. Anything else?\n" ) )
    else:
        inp_store_buy( input( "Invalid input." ) )

def getprice( sellitem ):
    # If it's a store item, sell it at 75% price
    if sellitem.lower() in store_prices:
        sellitem = sellitem.lower()
        return math.ceil( store_prices[sellitem] * 0.75 )
    # If an item not found in store
    elif sellitem.lower() in item_sellprices:
        sellitem = sellitem.lower()
        return math.ceil( item_sellprices[ sellitem ] )
    # If cube
    else:
        # Now, this may get tricky. We calculate price of cube based on the amount of prefixes.
        # For that we iterate over the string and get the number of spaces. Each space = one prefix.
        # Yes, this means that an affix "upgrades" the cost of the cube by two levels. That works out.
        # You can have 0-6 spaces. 0 is Cube, 1 is one prefix etc.
        spaces = 0
        for letter in sellitem:
            if letter == " ":
                spaces += 1
        return get_cube_cost( spaces )

# Input in store for buying
def inp_store_buy( pl_input ):
    # Save as table, [1] is command [2] is argument
    pl_input = pl_input.strip().split('\t')
    command = pl_input[0].lower()

    if len( pl_input ) > 1:
        argument = pl_input[1]
    else:
        # Make argument incorrect if blank
        argument = "nil"

    # Argument 2 is usually the amount you want to buy/sell
    if len( pl_input ) > 2:
        argument2 = pl_input[2]
    else:
        argument2 = 1

    if command == "exit":
        os.system('cls')
        mainmenu()
    elif command == "balance":
        inp_store_buy(input( "Your balance: " + str( inventory[0][1] ) + " credits\n"))
    elif command == "buy":
        # First check if such a cube exists, then ask how many
        if argument in store_prices:
            # setcube is name of cube, used in next function
                # FIX Why do we not put the argument as a function arg? 
            global setcube
            setcube = argument

            match setcube:
                case "bb": setcube = "basic box"
                case "pb": setcube = "prefixed box"
                case "dpb": setcube = "double prefixed box"
                case "tpb": setcube = "triple prefixed box"
                case "qpb": setcube = "quadruple prefixed box"

            inp_store_buy_count( argument2 )
        else:
            inp_store_buy( input( "We don't sell that here.\n" ) )
    # For selling
    elif command == "sell":
        # credits, available, cube
        # We have to check if the item is available, if it's sellable and if it's a cube
        # There are two sellables: cubes and items. You can't sell credits.
        checktable = checkinv( argument )
        # If an index was input, change sellitem from int to item name
        if checktable["found"] and checkifproperint( argument ):
            argument = int(argument)
            print( "That's the " + inventory[ argument ][0] )
            argument = inventory[ argument ][0]
        # If the item is not inventory
        if checktable["found"] == False:
            # When selling all
            if argument == "all": #//FIX you can sell for 0 credits if inv is empty. Doesn't break anything, just a bit weird | 23.05.24
                total = 0
                for row in inventory[1:len(inventory)]:
                    # Don't sell favourites
                    try:
                        row[2] != "fav"
                    except:
                        total += getprice( row[0] ) * row[1]
                        
                if input( "That will get you " + str( total ) + " credits. [sell or exit]\n" ).lower() == "sell":
                    for row in inventory[1:len(inventory)]:
                        try:
                            row[2] != "fav"
                        except:
                            inventory.pop( inventory.index( row ) )
                    addcredits( total )
                    inp_store_buy( input( f"Thank you! You now have {inventory[0][1] } credits. Anything else?\n") )
                else:
                    inp_store_buy( input( "Alright. Anything else?" ) )
            else:
                inp_store_buy( input( "You don't have that.\n" ) )
        else:
            # Amount of items
            count = inventory[ checktable["index"] ][1]
            if argument == "credits":
                inp_store_buy( input( "You can't sell that.\n" ) )
            # If the item is valid
            else:
                price = getprice( argument )
                # Now we return and ask to sell
                # If more than 1, ask how many
                proceed = True
                if checkifproperint( argument2 ) and int( argument2 ) <= count:
                    # If valid count
                    argument2 = int(argument2)
                    price *= argument2
                else:
                    proceed = False
                    inp_store_buy( input( "That's not valid. Anything else?\n" ) )
                # No matter the count, ask to sell, assuming we didn't input an invalid count value previously
                if proceed:
                    ask = input( "That'll get you " + str( price ) + " credits. Would you like to sell? [sell or exit]\n" ).lower()
                    if ask == "sell":
                        inventory[checktable["index"]][1] -= argument2
                        # If sold all, delete
                        if inventory[ checktable["index"] ][1] == 0:
                            inventory.pop( checktable["index"] )
                        addcredits( price )
                        inp_store_buy( input( "Thanks! Anything else?\n" ) )
                    else:
                        inp_store_buy( input( "That's cool. Anything else?\n" ) )
    else:
        inp_store_buy( input( "Pardon?\n" ) )   





# "store" input
def inp_store():
    os.system('cls')
    print(" /\     /\ ")
    print("{  `---'  }")
    print("{  O   O  }")
    print("~~>  V  <~~")
    print(" \  \|/  /")
    print("  `-----'__")
    print("  /     \  `^\_")
    print(" {       }\ |\_\_   W")
    print(" |  \_/  |/ /  \_\_( )")
    print("  \__/  /(_E     \__/")
    print("    (  /")
    print("     MM")

    inp_store_buy( input("Hi, welcome to the Cat Emporium! What can I get you?\n--------------------------------\nBasic Box [10c]\nPrefixed Box[50c]\nDouble Prefixed Box[500c]\nTriple Prefixed Box[5000c]\nQuadruple Prefixed Box[50000c]\n\nYour balance: " + str( inventory[0][1] ) + " credits\n") )

# "debug" input to make the program close so I can run commands
def debug():
    pass

# Place to earn cash
def jobs():
    os.system('cls')
    plinput = input( "Welcome to the jobs section! You can earn cash here. Choose an activity to take your time!\nguessgame\n" )
    if plinput.lower() == "exit":
        mainmenu()
    elif plinput.lower() == "guessgame":
        guessgame()
# Activity: Guessing Game
def guessgame():
    os.system('cls')
    maxnum = 100
    # By guessing right the first time you get a triple prefix box. Each time you fail to guess, the reward halves
    newnumber = True
    print( f"Welcome to Guess Game! Guess a number from 1 to {maxnum}. The earlier you guess, the more credits you get!\n" )

    while True:
        if newnumber:
            reward = 1000
            rightnumber = random.randint( 1, maxnum )
            newnumber = False
        givenumber = input("Input a number! or exit\n")
        if str( givenumber.lower() ) == "exit":
            mainmenu()
            break
        elif checkifproperint( givenumber ) == False:
            print("Incorrect number!...")
        elif rightnumber > int(givenumber): # if guessed less
            os.system('cls')
            reward /= 2
            print( f"{givenumber} is lower, try something higher!" )
        elif rightnumber < int(givenumber): # if guessed more
            os.system('cls')
            reward /= 2
            print( f"{givenumber} is higher, try something lower!" )
        else:
            reward = math.ceil( reward )
            addcredits( reward )
            print( f"You guessed right! Your reward is {reward} credits! You now have {inventory[0][1]} credits." )
            
            newnumber = True

# Open a box once per day for rewards. Increases each time you open (not a streak though).
# 86400 seconds in a day
def dailybox():
    format_str = "%Y-%m-%d %H:%M:%S"
    dbindex = -1
    eligible = False
    # Get position of dailybox in dates
    for row in dates:
        if row[0] == 'dailybox':
            dbindex = dates.index( row )
    # If new setup  
    if dbindex == -1:
        dates.append( ['dailybox', datetime.now().strftime( format_str ) ] )
        savetime()
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
            savetime()
    # Finally check through bool eligible if can receive.
    if eligible:
        print( "You open your daily box. It contains...")
        time.sleep( 2 )
        randint = random.randint( 1, 100 )
        match randint:
            case randint if randint <= 2: # Affix tag drop
                print( "An Affix Tag!" )
                additem( "Affix Tag", 1 )
            case randint if randint >= 3 and randint <= 25:

                # 5 percent for quad pref, otherwise triple
                if random.randint(1, 100) < 6:
                    additem( "Quadruple Prefixed Box", 1 )
                    print( "A Quadruple Prefixed Box!" )
                else:
                    additem( "Triple Prefixed Box", 1 )
                    print( "A Triple Prefixed Box!" )

            case randint if randint >= 26 and randint <= 50:
                print( "A random kitty!" )

                if random.randint(1, 100) < 6:
                    rollcube( inv_inputs["quadruple prefixed box"] )
                else:
                    rollcube( inv_inputs["triple prefixed box"])
            case randint if randint >= 51 and randint <= 100:
                # 50% chance for treat tickets
                if random.randint( 1, 2 ) == 1:
                    randint = random.randint( 200, 2000 )
                    print( f"{randint} credits!" )
                    addcredits( randint )
                else:
                    randint = random.randint( 5, 20 )
                    print( f"{randint} Treat Tickets!" )
                    additem( "Treat Ticket", randint )
        time.sleep( 3 )
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
        print( f"The daily box is still locked, you should check back in {amount} {nominal}." )
        time.sleep( 3 )

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
    catsfed = math.floor( treatcount / 100 )
    tickets = 0
    ticketinfo = checkinv( "Treat Ticket" )

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
            savetime()

            reward = math.ceil(( catsfed * 25 ) * random.uniform( 0.75, 1.5 ))
            addcredits( reward )

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
            mainmenu()
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
    elif checkifproperint(plinput):
        plinput = int(plinput)
    
    if checkifproperint( plinput ) or plinput == "all" :
        plinput = int(plinput)
        # If less than what you have
        if plinput > inventory[0][1]:
            print( "You sadly don't have that much..." )
            time.sleep( 2 )
            os.system('cls')
            treats()
        else:
            addcredits( -plinput )
            dates[2][1] = plinput + int( dates[2][1] ) 
            savetime()
            print( "Thank you for donating!")
            time.sleep( 2 )
            os.system( 'cls' )
            treats()
    else:
        print( "That's not a correct value..." )
        time.sleep( 2 )
        os.system('cls')
        treats()

# Redeeming Treat Tickets. Each ticket is worth 100 Credits and can be sold for 25
def treatsredeem():
    ticketloc = checkinv( "Treat Ticket" )
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
        elif checkifproperint(plinput):
            plinput = int(plinput)
    
        if checkifproperint( plinput ) or plinput == "all":
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
                saveinv()
                dates[2][1] = int( dates[2][1] ) + plinput * 100
                savetime()
                print( "Thank you so much for redeeming!")
                time.sleep( 2 )
                os.system( 'cls' )
                treats()
        else:
            print( "That's not a correct value..." )
            time.sleep( 2 )
            os.system('cls')
            treats()

def freecash():
    addcredits( 10000 )
    saveinv()

# List of inputs for the player to utilise.
player_inputs = {
    "help": helpguide,
    "inventory": inp_inv, "inv": inp_inv,
    "registry": inp_reg, "reg": inp_reg,
    "store": inp_store, "shop": inp_store,
    "debug": debug,
    "jobs": jobs,
    "dailybox": dailybox,
    "treats": treats,
    "meow": freecash
}

def affixtag(row):
    # row is inventory index of the affix tag. god im sleepy
    # Apply an affix to a cube. Must be a cube with no affix (easy).
    plinput = input( "Which Kitty would you like to apply a random affix to? It can't already be affixed. [or exit]\n" )
    checktable = checkinv( plinput )
    cubeindex = checktable["index"]
    
    if plinput.lower() == "exit":
        inp_inv(True)
    elif checktable["found"]:
        if checkifproperint( plinput ):
            plinput = inventory[int(plinput)][0].lower()
        # Check if it's a cube
        if plinput[len(plinput)-5:len(plinput)].lower() != "kitty":
            print( "You can only affix Kitties, or the Kitty is already affixed." )
            time.sleep( 1.5 )
            affixtag(row)
        else:
            # Delete one tag if right
            inventory[row][1] -= 1
            # If empty, delete from inv
            if inventory[row][1] == 0:
                # If the Affixer will disappear and is positioned before the target cube, the cube's index has to be lowered
                # Otherwise the affix might hit the wrong cube or crash completely
                if row < cubeindex:
                    cubeindex -= 1
                inventory.pop( row )
            
            # Find cube in inventory. Get its name and row.
            cubename = inventory[cubeindex][0]
            # If the cube is favourited, the result will come out favd too. Convenience
            favd = False
            try:
                if inventory[cubeindex][2] == "fav":
                    favd = True
            except:
                favd = False
            inventory[cubeindex][1] -= 1
            if inventory[cubeindex][1] == 0:
                inventory.pop( cubeindex )
            if favd:
                addcube(  cubename + " " + affixtable[random.randint(0, affixmax)], 1, True )
            else:
                addcube(  cubename + " " + affixtable[random.randint(0, affixmax)], 1 )
            saveinv()
            time.sleep( 1.5 )
            inp_inv( True )
    else:
        print( "No such kitten." )
        time.sleep( 1.5 )
        affixtag(row)

# Used in selling to get price of sold cube based on prefixes
def get_cube_cost(prefixes):
    match prefixes:
        case 0:
            return 5
        case 1:
            return 20
        case 2:
            return 200
        case 3:
            return 3000
        case 4:
            return 25000
        case 5:
            return 100000
        # Quad prefix with affix? Should be expensive.
        case 6:
            return 500000
        case _:
            return math.pow(20, prefixes)
        

inv_inputs = {
    # First four values are prefix drop chances
    "basic box": [ 4, 25, 100, 1000 ],
    "prefixed box": [ 1, 15, 40, 100 ],
    "double prefixed box": [ 1, 1, 15, 35 ],
    "triple prefixed box": [ 1, 1, 1, 20],
    "quadruple prefixed box": [ 1, 1, 1, 1 ],
    "affix tag": affixtag
}


store_prices = {
    "basic box":10, "bb": 10,
    "prefixed box": 50, "pb": 50,
    "double prefixed box": 500, "dpb": 500,
    "triple prefixed box": 5000, "tpb": 5000,
    "quadruple prefixed box": 50000, "qpb": 50000,
}

# For convenient selling of items that aren't in the store
item_sellprices = {
    "kitty box": 999999,
    "affix tag": 75000,
    "treat ticket": 100
}

# Input def for main inputs
def inputs1( player_input ):
    player_input = player_input.lower() # .lower() for ignoring capitalisation
    if player_input in player_inputs:
        # Check if it's inventory to apply its bool correctly
        if player_input == "inv" or player_input == "inventory":
            player_inputs[player_input]( True )
        else:
            player_inputs[player_input]()
    else:
        player_input = inputs1( input("Meow, I don't get what you're saying... ") )

# Start message
def mainmenu():
    os.system('cls')
    return

while True:
    os.system('cls')

    print( "           __..--''``---....___   _..._    __" )
    print(  "/// //_.-'    .-/';  `        ``<._  ``.''_ `. / // /" )
    print( '///_.-" _..--."_    |                    `( ) ) // //' )
    print( "/ (_..-' // (< _     ;_..__               ; `' / ///" )
    print( " / // // //  `-._,_)' // / ``--...____..-' /// / //" )

    inputs1( input( 'Meow! Welcome to Kitty Collector version ' + verdate + '. For help, type "help".\n' ) )








# The Plaza
# You can open your dailybox there.
# You can also receive support from your fed cats here
    # At any time you can donate credits to feed cats. Afterwards, every day you get a portion of that money back, as thanks from the cats
    # Maybe this could also unlock stuff?
    # Think: you can unbox Treat Tickets which can be consumed for this stockpile


# You can also talk to the Phu'Sea (Fussy) Vendor here, who will seek Cats with certain Prefixes here every day.
    # You can match them partially or completely. A complete match for 2+ prefixes yields A LOT of cash since it's rare.
    # A partial match is still worth it though.
    # He accepts only one Prefix sale per day

# Continuity mechanics. Something to work for. Unlocks, investments
    # Something that upgrades the payout from Guessgame
    # Gives money for unlocking more and more of the registry