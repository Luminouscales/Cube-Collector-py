import math, os, time, random

import scripts.data as d

inventory = d.inventory
limit = d.limit
registry = d.registry
inv_inputs = d.inv_inputs

# "inventory" input that prints owned cubes
# printinv is a bool that decides if we should print the inventory or not
def inp_inv( printinv ):
    pages = math.ceil( len( inventory )/limit )
    if printinv:
        os.system('cls')
        print( "\nYour inventory contains:" )
        print("--------------------------------------------")
        # We'll nowe use printreg() to show the inventory in pages.
        d.printreg( 1, pages, inventory )
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

    match command:
        case "exit" | "e": return
        case "fav": case_fav(argument1)
        case "page": case_page(argument1, pages)
        case "use": case_use( argument1, argument2 )
        case "info": return # FIXME
        case "delete": case_delete(argument1, argument2)
        case "sort": case_sort(argument1)
        case "r": case_random()
        case _: case_else(command)

# This is so much cleaner

def case_fav(argument1):
    checktable = d.checkinv( argument1 )
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
            d.saveinv()
            inp_inv( False )
        # If favourited, remove from favourites
        else:
            row.pop( len(row) - 1 )
            print( row[0] + " removed from favourites." )
            d.saveinv()
            inp_inv( False )
    else:
        print( "Invalid kitty." )
        time.sleep( 1 )
        inp_inv( False )

def case_page(argument1, pages):
    if d.checkifproperint( argument1 ) and int( argument1 ) <= pages:
        os.system('cls')
        print( "\nYour inventory contains:" )
        print("--------------------------------------------")
        d.printreg( int( argument1 ), pages, inventory )
        print("--------------------------------------------")
        inp_inv( False )
    else:
        print( "Invalid page." )
        time.sleep(1)
        inp_inv( False )

def case_use( argument1, argument2 ):
    # argument1 is cube name or index
    # d.checkinv() returns if found and index row where the item is
    checktable = d.checkinv( argument1 )
    # If it's an index
    if checktable["found"] and d.checkifproperint( argument1 ):
        argument1 = inventory[int(argument1)][0].lower()
    # If it was found, if it's usable   
    if checktable[ "found" ] and argument1 in inv_inputs:
        rowindex = checktable[ "index" ]
        rowd = inventory[ rowindex ]
        # argument2 is how many we use
        if d.checkifproperint( argument2 ) == False:
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
                        d.rollcube( inv_inputs[argument1] )

                        # Function for rolling Treat Tickets
                        if random.randint( 1, 30 ) == 1:
                            ticketamount = math.ceil(( ( d.store_prices[ argument1 ] / 10 ) * random.uniform(0.8, 1.2) ))
                            d.additem( "Treat Ticket", ticketamount )
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
                inp_inv( False )
    else:
        print( "You can't use that." )
        time.sleep(1)
        inp_inv( False )

def case_delete(argument1, argument2):
    # d.checkinv() returns if found and index row where the item is
    checktable = d.checkinv( argument1 )
    # If index
    if checktable["found"] and d.checkifproperint( argument1 ):
        print( inventory[int(invuse)][0] )
        invuse = inventory[int(invuse)][0].lower()
    # If in inventory
    if checktable["found"]:
        rowindex = checktable[ "index" ]
        row = inventory[ rowindex ]
        # If there is more than one of the item
        if row[1] > 1:
            if d.checkifproperint( argument2 ) == False:
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
                d.saveinv()
                inp_inv( True )
        # If delete only one
        else:
            # If it's cash, don't remove whole line, just set to 0 or else the game will break
            if row[0] == "CREDITS":
                inventory[rowindex][0] == 0
            else:
                inventory.pop( rowindex )
            print( "Items deleted." )
            d.saveinv()
            time.sleep( 1 )
            inp_inv( True )
    else:
        print( "You don't have that." )
        time.sleep(1)
        inp_inv( False )

def case_sort(argument1):
    # Sort alphabetically
    if argument1 == "alph":
        inventory.sort( key=lambda x: x[0] )
    # Sort by value
    elif argument1 == "value" or argument1 == "val":
        inventory.sort( key=lambda x: d.getprice( x[0] ) * x[1], reverse=True )
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
    d.saveinv()
    inp_inv( True )

def case_random():
    print("")
    for _ in range(20):
        print( inventory[random.randint(0, len(inventory)-1 )][0] )
    inp_inv( False )

# No command input, either "find" a cube or except invalid input
def case_else(command):
    if d.checkinv( command )["found"]:
        checktable = d.checkinv( command )
        row = inventory[( checktable["index"] )]
        loc = math.ceil( checktable["index"] / limit )
        print( "Found " + str( row[1] ) + " of " + row[0] + " at index [" + str( checktable["index"] ) + "], page " + str( loc ) )
        inp_inv( False )
    else:
        print( "Invalid input." )
        time.sleep(1)
        inp_inv( False )