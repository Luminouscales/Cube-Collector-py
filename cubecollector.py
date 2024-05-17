import os, sys, random, time, math

selfpath = os.path.dirname(sys.argv[0])
inventorypath = selfpath + "/inventory.txt"
registrypath = selfpath + "/registry.txt"
verdate = "07.05.24"

# In the future we could use subprocess to slice up the code into more accessible chunks and run only what we need.

# Read the inventory and output it into the "inventory" var
inventory = []
if os.path.exists(inventorypath):
    with open( inventorypath, 'r' ) as file:
        for line in file:
            row = line.strip().split('\t') # What?
            inventory.append( row )
            # Turn every amount number into int
            row[1] = int( row[1] )


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

# Import list of prefixes
with open( selfpath + "/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1

# Primitive roll function
def rollcube( tier ):
    # Tier is value of box. 0 is standard. 1 is single prefix. 2 is double prefix and so on
    # Roll for single prefix
    if tier > 0 or random.randint( 1, 2 ) == 1:
        prefixes = prefixtable[ random.randint( 0, prefixmax ) ]
        # Roll for second prefix if tier is 2
        if tier > 1 or random.randint( 1, 3 ) == 1:
            prefix2 = prefixtable[ random.randint( 0, prefixmax ) ]
            prefixes = prefixes + " " + prefix2
            if tier > 2 or random.randint( 1, 4 ) == 1:
                prefix3 = prefixtable[ random.randint( 0, prefixmax ) ]
                prefixes = prefixes + " " + prefix3
                if tier > 3 or random.randint( 1, 5 ) == 1:
                    prefix4 = prefixtable[ random.randint( 0, prefixmax ) ]
                    prefixes = prefixes + " " + prefix4
        gotcube = prefixes + " Cube"
        # Add cube to inventory
        addcube( gotcube )
        return
    # return if prefixed cube dropped, if not: add a basic vanilla ass Cube manually
    addcube( "Cube" )

# Function that adds a cube to inventory
def addcube( cube ):
    for row in inventory:
        # If cube already in inventory add one more to count and end function
        if row[0] == cube:
            row[1] = row[1] + 1
            print( "You got a " + cube + "!" )
            saveinv()
            # Add to reg
            addreg( cube )
            return
    # If new then add the cube to inventory. The 1 is the amount of new cubes. So, just one.
    inventory.append( [cube, 1] )
    saveinv()   
    addreg( cube )
    print( "You got a brand new " + cube + "!" )

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
    inputs1( input("Available commands: \niventory\nregistry\nstore\n") )

# Function for checking if the given item is in the inventory
def checkinv(item):
    for row in inventory:
        if item.lower() == row[0].lower():
            # Scripts using checkinv() can read this table to get the bool and the item's row
            return { "found": True, "index": inventory.index( row ) }
    return { "found": False  }

# For checking if the cube is in the registry, meaning if it's a cube
def checkreg(item):
    for row in registry:
        if item.lower() == row[0].lower():
            return True
    return False

# "inventory" input that prints owned cubes
def inp_inv():
    print( "Your inventory contains:" )
    print("--------------------------------------------")
    for row in inventory:
        print( " - " + row[0] + "\t" + str( row[1] ) )
    print("--------------------------------------------")
    invinput = input("Commands: use, delete, info, exit\n").lower()
    if invinput == "exit":
        mainmenu()
    # Input for using an object
    elif invinput == "use":
        # Yes, .lower() for everything to compare string not based on capitalisation
        invuse = input("Which item would you like to use?\n").lower()
        # You have to iterate like that
        # checkinv() returns if found and index row where the item is
        checktable = checkinv( invuse )

        if checktable[ "found" ]:
            found = True
            rowindex = checktable[ "index" ]
            rowd = inventory[ rowindex ]
        else:
            print( "You don't have that." )
            time.sleep(1)
            inp_inv()
        # If it was found, if it's usable
        if found and invuse in inv_inputs:
            # If it's only one, use immediately, if not - ask
            if rowd[1] == 1:
                # Remove one use from the object; if it's last, remove it from inv
                rowd[1] -= 1
                if rowd[1] == 0:
                    inventory.pop(rowindex)
                rollcube( inv_inputs[invuse] )
                inp_inv()
            else:
                invusecount = input( "How many of those would you like to use?\n" )
                # Typical try check to prevent crash
                if checkifproperint( invusecount ) == False:
                    print( "That's not valid.\n" )
                    time.sleep(1)
                    inp_inv()
                else:
                    invusecount = int(invusecount)   
                    # Check if you have enough
                    if invusecount <= rowd[1]:
                        for i in range( invusecount ):
                            # Remove one use from the object; if it's last, remove it from inv
                            rowd[1] -= 1
                            if rowd[1] == 0:
                                inventory.pop(rowindex)
                            rollcube( inv_inputs[invuse] )
                            time.sleep(0.5)
                        inp_inv()
                    else:
                        print( "You don't have enough of those.\n" )
                        time.sleep(1)
                        inp_inv()
        else:
            print( "You can't use that." )
            time.sleep(1)
            inp_inv()
    # Give information about object. //FIX
    elif invinput == "info":
        pass

    # I shouldn't run it with elifs like that..
    elif invinput == "delete" or invinput == "del":
        invuse = input("Which item would you like to delete? Remember that this cannot be undone. Make sure you're deleting the right item.\n").lower()
        # checkinv() returns if found and index row where the item is
        checktable = checkinv( invuse )
        # If in inventory
        if checktable["found"]:
            rowindex = checktable[ "index" ]
            row = inventory[ rowindex ]
            # If there is more than one, ask how many
            if row[1] > 1:
                delcount = input( "How many of these would you like to delete?\n")
                # int check again.. should make it a function
                if checkifproperint( delcount ) == False:
                    print( "That's not valid.\n" )
                    time.sleep(1)
                    inp_inv()
                else:
                    delcount = int(delcount)   
                    # Delete if right
                    inventory[rowindex][1] -= delcount
                    print( "Items deleted." )
                    # If empty, delete from inv; don't delete completely if it's money
                    if row[1] == 0 and row[0] != "CREDITS":
                        inventory.pop( rowindex )
                    saveinv()
                    inp_inv()
            # If delete only one
            else:
                # If it's cash, don't remove whole line, just set to 0 or else the game will break
                if row[0] == "CREDITS":
                    inventory[rowindex][0] == 0
                else:
                    inventory.pop( rowindex )
                print( "Items deleted." )
                saveinv()
                inp_inv()
        else:
            print( "You don't have that." )
            time.sleep(1)
            inp_inv()
    else:
        print( "Invalid input." )
        time.sleep(1)
        inp_inv()

# //FIX add pages/categories to inventory

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

def printreg( page, maxpages ):
    # So we print a certain range in the list. First one is 1 - 50, then 51 - 101, then 151 - 201
    range1 = ( page - 1 ) * 50
    range2 = page * 50 + ( page - 1 ) * 50
    for row in registry[range1:range2]:
        print( "[" + str( row[2] ) + "] " + row[0] + " " + str( row[1] ) )
    print( "Page " + str( page ) + " of " + str(maxpages) )

# registry input part 2, internal, to maintain flow
def inp_reg2( pages ):
    reginput = input("Input page or 'exit'\n")
    if reginput.lower() == "exit":
        mainmenu()
    # Must be proper int and not more than max pages
    elif checkifproperint( reginput ) == False or int(reginput) > pages:
        print( "Incorrect input." )
        time.sleep( 1 )
        inp_reg()
    else:
        reginput = int(reginput)
        printreg( reginput, pages )
    inp_reg2(pages)

# "registry" input
def inp_reg():
    # Calculate number of pages
    # registry length
    reglen = len(registry)
    # pages, rounded up is full amount
    pages = math.ceil( reglen / 50 )
    print( "The registry contains:\n--------------------------------------------")
    # First ID, then cube, then amount 
    printreg( 1, pages )
    inp_reg2( pages )

# Input in store for buying a certain amount
def inp_store_buy_count( pl_input ):
    pl_input = pl_input.lower()
    if pl_input == "exit":
        mainmenu()
    else:
        # Exception check if you input something that's not a number
        try:
            pl_input = int(pl_input)
        except:
            inp_store_buy_count( input( "That's not valid.\n" ) )
        else:
            # If it's bigger than 0 and if it's whole
            if pl_input > 0 and pl_input % 1 == 0:
                # Calc price and check if we have the funds
                price = pl_input * store_prices[ setcube ]
                locinput = input( "That will be " + str( price ) + " credits. [buy or exit] " )
                if locinput == "buy":
                    cash = inventory[0][1]
                    if cash >= price:
                        # Add to inv; name and amount; remove cash
                        inventory[0][1] -= cash - price
                        additem( setcube, pl_input )
                        inp_store_buy( input("Thanks for buying! Anything else?\n") )
                    else:
                        inp_store_buy( input( "You can't afford that. Anything else?\n" ) )
                else:
                    inp_store_buy( input( "Alright. Anything else?\n" ) )
                
# Used in selling to get price of sold cube based on prefixes
def get_cube_cost(prefixes):
    match prefixes:
        case 0:
            return 10
        case 1:
            return 30
        case 2:
            return 300
        case 3:
            return 3000
        case 4:
            return 30000
        case 5:
            return 60000
        # Quad prefix with affix? Should be expensive.
        case 6:
            return 200000

# Input in store for buying
def inp_store_buy( pl_input ):
    pl_input = pl_input.lower()
    if pl_input == "exit":
        mainmenu()
    elif pl_input == "balance":
        inp_store_buy(input( "Your balance: " + str( inventory[0][1] ) + " credits\n"))
    elif pl_input == "buy":
        # First check if such a cube exists, then ask how many
        if pl_input in store_prices:
            # setcube is name of cube, used in next function
            global setcube
            setcube = pl_input
            inp_store_buy_count( input( "And how many would you like?\n" ) )
        else:
            inp_store_buy( input( "We don't sell that here.\n" ) )
    # For selling
    elif pl_input == "sell":
        sellitem = input( "What would you like to sell?\n" ).lower()
        # credits, available, cube
        # We have to check if the item is available, if it's sellable and if it's a cube
        # There are two sellables: cubes and items. You can't sell credits.
        checktable = checkinv( sellitem )
        # If the item is not inventory
        if checktable["found"] == False:
            inp_store_buy( input( "You don't have that.\n" ) )
        else:
            # Amount of items
            count = inventory[ checktable["index"] ][1]
            if sellitem == "credits":
                inp_store_buy( input( "You can't sell that.\n" ) )
            # If the item is valid
            else:
                # If it's a store item, sell it at 75% price
                if sellitem in store_prices:
                    price = math.ceil( store_prices[sellitem] * 0.75 )
                # If an item not found in store
                elif sellitem in item_sellprices:
                    price = math.ceil( item_sellprices[ sellitem ] )
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
                    price = get_cube_cost( spaces )
                # Now we return and ask to sell
                # If more than 1, ask how many
                if count > 1:
                    ask2 = input( "How many of those would you like to sell? You have " + str( count ) + "\n" )
                    if checkifproperint( ask2 ) and int( ask2 ) <= count:
                        # If valid count
                        ask2 = int(ask2)
                        price *= ask2
                        proceed = True
                    else:
                        proceed = False
                        inp_store_buy( input( "That's not valid. Anything else?\n" ) )
                # No matter the count, ask to sell, assuming we didn't input an invalid count value previously
                if proceed:
                    ask = input( "That'll get you " + str( price ) + " credits. Would you like to sell? [sell or exit]\n" ).lower()
                    if ask == "sell":
                        # If sold all, delete
                        if ask2 == count:
                            inventory.pop( checktable["index"] )
                        # If not, delete only the chosen amount
                        else:
                            inventory[checktable["index"]][1] -= ask2
                        inventory[0][1] += price
                        saveinv()
                        inp_store_buy( input( "Thanks! Anything else?\n" ) )
                    else:
                        inp_store_buy( input( "That's cool. Anything else?\n" ) )

    else:
        inp_store_buy( input( "Pardon?\n" ) )   


        

# "store" input
def inp_store():
    inp_store_buy( input("Hi, welcome to the Cube Emporium! What can I get you?\n--------------------------------\nBasic Box [10c]\nPrefixed Box[100c]\nDouble Prefixed Box[1000c]\nTriple Prefixed Box[10000c]\nQuadruple Prefixed Box[100000c]\n") )

# List of inputs for the player to utilise.
player_inputs = {
    "help": helpguide,
    "inventory": inp_inv,
    "inv": inp_inv,
    "registry": inp_reg,
    "reg": inp_reg,
    "store": inp_store
}

inv_inputs = {
    "basic box": 0,
    "prefixed box": 1,
    "double prefixed box": 2,
    "triple prefixed box": 3,
    "quadruple prefixed box": 4,
}

store_prices = {
    "basic box": 10,
    "prefixed box": 100,
    "double prefixed box": 1000,
    "triple prefixed box": 10000,
    "quadruple prefixed box": 100000,
}

# For convenient selling of items that aren't in the store
item_sellprices = {
    "placeholder": 999999
}

# Input def for main inputs
def inputs1( player_input ):
    player_input = player_input.lower() # .lower() for ignoring capitalisation
    if player_input in player_inputs:
        player_inputs[player_input]()
    else:
        player_input = inputs1( input("Meow, I don't get what you're saying... ") )

# Start message
def mainmenu():
    inputs1( input( 'Meow! Welcome to Cube Collector version ' + verdate + '. For help, type "help".\n' ) )

mainmenu()
