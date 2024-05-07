import os, sys, random, time, atexit

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
    # Unique ID is counted by adding one to last cube's ID. Let's just hope it's sorted correctly.
    registry.append( [ cube, 1, registry[len(registry) - 1][2] + 1 ] )
    savereg()

# Import list of prefixes
with open( selfpath + "/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1

# Primitive roll function
def rollcube():
    # Roll for single prefix
    if random.randint( 1, 2 ) == 1:
        prefixes = prefixtable[ random.randint( 0, prefixmax ) ]
        # Roll for second prefix
        if random.randint( 1, 3 ) == 1:
            prefix2 = prefixtable[ random.randint( 0, prefixmax ) ]
            prefixes = prefixes + " " + prefix2
            if random.randint( 1, 4 ) == 1:
                prefix3 = prefixtable[ random.randint( 0, prefixmax ) ]
                prefixes = prefixes + " " + prefix3
                if random.randint( 1, 5 ) == 1:
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
    # Add to reg
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
    # If new then add the cube to inventory. The 1 is the amount of new cubes. So, just one.
    inventory.append( [cube, count] )
    saveinv()

# When the player inputs "help". Lists an explanation of the game and commands.
def helpguide():
    inputs1( input("Available commands: \nbalance\niventory\nregistry\nstore\n") )

# "inventory" input that prints owned cubes
def inp_inv():
    print( inventory )
    inputs1( input("\n") )

# "registry" input
def inp_reg():
    print( registry )
    inputs1( input("\n") )

# Input in store for buying a certain amount
def inp_store_buy_count( pl_input ):
    pl_input = pl_input.lower()
    # Exception check if you input something that's not a number
    if pl_input == "exit":
        mainmenu()
    else:
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
                

# Input in store for buying
def inp_store_buy( pl_input ):
    pl_input = pl_input.lower()
    if pl_input == "exit":
        mainmenu()
    elif pl_input == "balance":
        inp_store_buy(input( "Your balance: " + str( inventory[0][1] ) + " credits\n"))
    else:
        # First check if such a cube exists, then ask how many
        if pl_input in store_inputs:
            # setcube is name of cube, used in next function
            global setcube
            setcube = pl_input
            inp_store_buy_count( input( "And how many would you like?\n" ) )
        else:
            inp_store_buy( input( "We don't sell that here.\n" ) )

# "store" input
def inp_store():
    inp_store_buy( input("Hi, welcome to the Cube Emporium! What can I get you?\nBasic Box [10c]\nPrefixed Box[100c]\nDouble Prefixed Box[1000c]\nTriple Prefixed Box[10000c]\nQuadruple Prefixed Box[100000c]\n") )

# input func for the store
def inputs_store1( input ):
    if input in store_inputs:
        store_inputs[input]()
    else:
        inputs1( input("Hmm, I don't think you can buy that. ") )

# List of inputs for the player to utilise.
# What inputs should we have?
    # Check inventory, check registry
    # Open box
    # Store
    # Sell cube
    # Check balance
player_inputs = {
    "help": helpguide,
    "inventory": inp_inv,
    "inv": inp_inv,
    "registry": inp_reg,
    "reg": inp_reg,
    "store": inp_store
}

def basicbox():
    pass

def prefbox():
    pass

def dprefbox():
    pass

def tprefbox():
    pass

def qprefbox():
    pass

store_inputs = {
    "basic box": basicbox,
    "prefixed box": prefbox,
    "double prefixed box": dprefbox,
    "triple prefixed box": tprefbox,
    "quadruple prefixed box": qprefbox,
}


store_prices = {
    "basic box": 10,
    "prefixed box": 100,
    "double prefixed box": 1000,
    "triple prefixed box": 10000,
    "quadruple prefixed box": 100000,
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
    inputs1( input( 'Meow! Welcome to Cube Collector version ' + verdate + '. For help, type "help". ' ) )

mainmenu()