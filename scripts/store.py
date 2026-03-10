import os, math

import scripts.data as d

inventory = d.inventory

store_prices = d.store_prices

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

    match command:
        case "exit" | "e": return
        case "buy" | "b": case_buy(argument, argument2)
        case "sell" | "s": case_sell(argument)
        case _: inp_store_buy( input( "Pardon?\n" ) )

# Input in store for buying a certain amount
def inp_store_buy_count( pl_input ):
    cash = inventory[0][1]
    # inputting "max" will give you the maximum amount you can buy
    if pl_input.lower() == "max" or pl_input.lower() == "all":
        pl_input = math.floor( cash / store_prices[ setcube ] )
        if pl_input < 1:
            inp_store_buy( input( "You can't afford any. Anything else?\n" ) )
            return
    if d.checkifproperint( pl_input ):
        # If it's bigger than 0 and if it's whole
        # Calc price and check if we have the funds
        pl_input = int( pl_input )
        price = pl_input * store_prices[ setcube ]
        price = int(price)
        locinput = input( str(pl_input) + " of " + setcube + " costs " + str( price ) + " credits. [buy or exit] " )
        if locinput == "buy":
            if cash >= price:
                # Add to inv; name and amount; remove cash
                d.addcredits( -price )
                d.additem( setcube, pl_input )
                inp_store_buy( input("Thanks for buying! Anything else?\n") )
            else:
                inp_store_buy( input( "You can't afford that. Anything else?\n" ) )
        else:
            inp_store_buy( input( "Alright. Anything else?\n" ) )
    else:
        inp_store_buy( input( "Invalid input." ) )

def case_buy(argument, argument2):
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

def case_sell(argument):
    # credits, available, cube
    # We have to check if the item is available, if it's sellable and if it's a cube
    # There are two sellables: cubes and items. You can't sell credits.
    checktable = d.checkinv( argument )
    # If an index was input, change sellitem from int to item name
    if checktable["found"] and d.checkifproperint( argument ):
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
                    total += d.getprice( row[0] ) * row[1]
                    
            if input( "That will get you " + str( total ) + " credits. [sell or exit]\n" ).lower() == "sell":
                for row in inventory[1:len(inventory)]:
                    try:
                        row[2] != "fav"
                    except:
                        inventory.pop( inventory.index( row ) )
                d.addcredits( total )
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
            price = d.getprice( argument )
            # Now we return and ask to sell
            # If more than 1, ask how many
            proceed = True
            if d.checkifproperint( argument2 ) and int( argument2 ) <= count:
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
                    d.addcredits( price )
                    inp_store_buy( input( "Thanks! Anything else?\n" ) )
                else:
                    inp_store_buy( input( "That's cool. Anything else?\n" ) )