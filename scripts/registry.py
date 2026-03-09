import os, math, time
from scripts import data as d

registry = d.registry
limit = d.limit

# FIXME reg pages are fucked but who cars

# registry input part 2, internal, to maintain flow
def inp_reg2( pages ):
    reginput = input("Input page [number], kitty name, kitty ID, sort [alph, value, id, count] or exit\n")
    reginput = reginput.strip().split('\t')
    command = reginput[0].lower()
    argument1 = "nil"

    if len( reginput ) > 1:
        argument1 = reginput[1]

    match command:
        case "exit": return
        case "sort": case_sort(argument1)
        case "page": case_page( argument1, pages )
        case _: case_else( command, pages )


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

def case_sort(argument1):
    # Sort alphabetically

    match argument1:
        case "alph": registry.sort( key=lambda x: x[0] )
        case "value": registry.sort( key=lambda x: d.getprice( x[0] ), reverse=True )
        case "id": registry.sort( key=lambda x: x[2] )
        case "count": registry.sort( key=lambda x: x[1], reverse=True )
        case _: input("invalid sort?")

    d.savereg()
    inp_reg()

def case_page(argument1, pages):
    if d.checkifproperint( argument1 ) and int(argument1) <= pages:
        os.system('cls')
        argument1 = int(argument1)
        d.printreg( argument1, pages, registry )
        inp_reg2( pages )
    else:
        input("invalid something idk")

def case_else( command, pages ):
    if d.checkreg( command )["found"]:
        checktable = d.checkreg(command)
        row = registry[ checktable["index"] ]
        print( "Found " + str(row[1]) + " of " + row[0] + " at index [" + str( checktable["index"] + 1 ) + "] with ID " + str( row[2] ) )
        inp_reg2( pages )
    else:
        print( "Incorrect input." )
        time.sleep( 1 )
        inp_reg()