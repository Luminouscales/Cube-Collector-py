import os, sys, random, time, math
from datetime import datetime

selfpath = os.path.dirname(sys.argv[0]) + "/scripts/"
savepath = selfpath + "/save/"
inventorypath = selfpath + "save/inventory.txt"
registrypath = selfpath + "save/registry.txt"
timepath = selfpath + "save/time.txt"
limit = 20 # For inv/reg pages; how many items per page? 20 fits snugly in normal terminal size
format_str = "%Y-%m-%d %H:%M:%S"
# var used for daily rewards
daily = 3600 * 0.25

#/----------------------------/
# DATA IO
#/----------------------------/
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

# Import list of prefixes
with open( selfpath + "content/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1

# Import affixes
with open( selfpath + "content/affixes.txt", 'r' ) as file:
    lines = file.readlines()
    affixtable = [line.strip() for line in lines]
    affixmax = len(affixtable) - 1

#/----------------------------/
# INVENTORY/REG IO
#/----------------------------/
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

# Function for rolling a cube
def rollcube( odds ):
    # Odds is a table of chances for a box
    # [ one prefix, two, three, four ]

    # Each box has a odds[3] * 5 percent chance of dropping an affix tag.
    if random.randint( 1, odds[3] * 20 ) == 1:
        print( "You found an Affix Tag! You lucky cat." )
        addcube( "Affix Tag", 1 )
        time.sleep( 1 )
    else:
        prefixes = []
        for idx in range(len(odds)):
            if random.randint( 1, odds[idx] ) != 1:
                break
                
            prefixes.append(prefixtable[ random.randint( 0, prefixmax ) ])
        
        # Time for big randomness. Each rolled kitty has a 1% chance to get an extra prefix, an infinite amount of times. Good luck!
        extra = False
        while True:
            if random.randint( 1, 20 + ( odds[0] * 5 ) - 5 ) == 1: # Temp calculation to make pb less likely to be profitable
                prefixes.append(prefixtable[ random.randint( 0, prefixmax ) ])
                print( "*** This Kitty is carrying an extra prefix! ***" )
            else:
                break

        cube = ' '.join(prefixes) + ' Kitty' if len(prefixes) > 0 else 'Kitty'
        addcube(cube, 1)
        if extra:
            time.sleep( 2 )

# Function that adds a cube to inventory
# fav decides if cube should be favourited when added
def addcube( cube, amount=1, fav=False, text=True ): # text set in gallery, usually True
    
    for row in inventory:
        # If cube already in inventory add one more to count and end function
        if row[0] == cube:
            row[1] = row[1] + amount
            if text:
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
    if text:
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

#/----------------------------/
# MISC FUNCTIONS
#/----------------------------/
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

# Used in selling to get price of sold cube based on prefixes
def get_cube_cost(prefixes):
    match prefixes:
        case 0:
            return 5
        case 1:
            return 20
        case 2:
            return 150
        case 3:
            return 1250
        case 4:
            return 20000
        case 5:
            return 60000
        # Quad prefix with affix? Should be expensive.
        case 6:
            return 250000
        case _:
            return math.floor( math.pow(7, prefixes) )

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
        
def affixtag(row):
    # row is inventory index of the affix tag. god im sleepy
    # Apply an affix to a cube. Must be a cube with no affix (easy).
    plinput = input( "Which Kitty would you like to apply a random affix to? It can't already be affixed. [or exit]\n" )
    checktable = checkinv( plinput )
    cubeindex = checktable["index"]
    
    if plinput.lower() == "exit":
        return
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
            return
    else:
        print( "No such kitten." )
        time.sleep( 1.5 )
        affixtag(row)

        

#/----------------------------/
# DATA TABLES
#/----------------------------/
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
    "affix tag": 25000,
    "treat ticket": 20
}

inv_inputs = {
    # First four values are prefix drop chances
    "basic box": [ 8, 25, 100, 1000 ],
    "prefixed box": [ 1, 15, 40, 100 ],
    "double prefixed box": [ 1, 1, 15, 35 ],
    "triple prefixed box": [ 1, 1, 1, 20],
    "quadruple prefixed box": [ 1, 1, 1, 1 ],
    "affix tag": affixtag
}