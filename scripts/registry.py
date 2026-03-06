import os, math, time
from scripts import data as d

registry = d.registry
limit = d.limit

# registry input part 2, internal, to maintain flow
def inp_reg2( pages ):
    reginput = input("Input page [number], kitty name, kitty ID, sort [alph, value, id, count] or exit\n")
    reginput = reginput.strip().split('\t')
    command = reginput[0].lower()
    argument1 = "nil" 
    if len( reginput ) > 1:
        argument1 = reginput[1]
    if command == "exit":
        return
    # Check if exists
    elif d.checkreg( command )["found"]:
        checktable = d.checkreg(command)
        row = registry[ checktable["index"] ]
        print( "Found " + str(row[1]) + " of " + row[0] + " at index [" + str( checktable["index"] + 1 ) + "] with ID " + str( row[2] ) )
        inp_reg2( pages )
    elif command == "sort":
        # Sort alphabetically
        if argument1 == "alph":
            registry.sort( key=lambda x: x[0] )
        # Sort by value
        elif argument1 == "value":
            registry.sort( key=lambda x: d.getprice( x[0] ), reverse=True )
        elif argument1 == "id":
            registry.sort( key=lambda x: x[2] )
        elif argument1 == "count":
            registry.sort( key=lambda x: x[1], reverse=True )
        # Now return
        d.savereg()
        inp_reg()
    # Must be proper int and not more than max pages
    elif command == "page" and d.checkifproperint( argument1 ) and int(argument1) <= pages:
        os.system('cls')
        argument1 = int(argument1)
        d.printreg( argument1, pages, registry )
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
    d.printreg( 1, pages, registry )
    inp_reg2( pages )