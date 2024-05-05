import os, sys, random, time, atexit

selfpath = os.path.dirname(sys.argv[0])
inventorypath = selfpath + "/inventory.txt"

# Read the inventory and output it into the "inventory" var
inventory = []
if os.path.exists(inventorypath):
    with open( inventorypath, 'r' ) as file:
        for line in file:
            row = line.strip().split('\t') # What?
            inventory.append( row )

# Take all cubes from inventory var and save it as inventory.txt
def saveinv():
    with open( inventorypath, 'w' ) as file:
        for row in inventory:
            row_str = '\t'.join(map(str, row)) # What the fuck is map() ?
            file.write( row_str + '\n')

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
            row[1] = int( row[1] ) + 1
            print( "You got a " + cube + "!" )
            return 
    # If new then add the cube to inventory. The 1 is the amount of new cubes. So, just one.
    inventory.append( [cube, '1'] )
    print( "You got a brand new " + cube + "!" )