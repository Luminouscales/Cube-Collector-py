import random, json
import scripts.kaprefixes as script
import scripts.data as d

allskills = script.allskills

with open( "scripts/content/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1

def rollcat(name):
    prefixes = name.strip().split(' ')
    prefixes.pop( len(prefixes ) - 1 )
    pram = len(prefixes)

    # Random stat offset
    ghealth = random.randint( -50, 50 )
    gatt = random.randint( -3, 10 )
    gdef = random.randint( -3, 3 )
    gacc = random.randint( -20, 20 )

    # First table run
    kittystats = [ 100 * pram + ghealth, 10 * pram + gatt, pram * 5 + gdef, 1, pram * 10 + gacc ]

    # Apply static prefix changes
    for i in range( pram ):
        script.doprefixstats( prefixes[i-1], kittystats )

    # Roll skills
    kittyskills = []

    for i in range( pram ):
        kittyskills.append( allskills[ random.randint(0, len(allskills)-1)] )

    # Incremental skill rolls
    while True:
        numb = random.randint( 0, 100 ) + 10 * pram
        if numb >= 90:
            kittyskills.append( allskills[ random.randint(0, len(allskills)-1)] )
        else:
            break

    # Last setup
    kittystats[3] = max( 1, kittystats[3]) # At least 1 speed

    kitty = d.Cat( name, kittystats[0], kittystats[1], kittystats[2], kittystats[3], kittystats[4], kittyskills, False)

    return kitty

def rollname(prefixcount):
    prefixes = []
    for i in range(prefixcount):
        prefixes.append( prefixtable[ random.randint( 0, prefixmax ) ] )

    cat = ' '.join(prefixes) + ' Kitty'
    return cat


# Roll however much cats to be available to fight in arena
def rollcatenemies():

    enemies = []

    for i in range( 13 ):
        # 0-3: one prefix
        if i < 4:
            prefixes = 1
        # 4-6: two prefix
        elif i < 7:
            prefixes = 2
        # 7-8: three pref
        elif i < 9:
            prefixes = 3
        elif i == 9:
            prefixes = 4
        elif i == 10:
            prefixes = 5
        elif i == 11:
            prefixes = 6
        else:
            prefixes = 7

        name = rollname( prefixes )
        newenemy = rollcat( name )
        enemies.append( newenemy )

    with open(f"scripts/save/{d.savenum}/arena_enemies.json", "w") as f:
        json.dump([cat.__dict__ for cat in enemies], f, indent=4)