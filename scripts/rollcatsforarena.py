# Using a Gladiator Tag on a Kitty
# As a base, roll a random offset for:
    # Health
    # Damage
    # Defence
    # Speed
    # Accuracy
# Based on number of prefixes, a bonus to all stats (as a base, more prefixes = much stronger)
# Apply the prefix changes
# Roll random skills. One prefix: one skill, then 25%(?) chance compounding for more
# Save as a json?

import random, json
import scripts.kaprefixes as script

allskills = script.allskills

with open( "scripts/content/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1

class Cat:
    def __init__(self, name, hp, att, de, sp, acc, skills, tempo):
        self.name = name
        self.hp = hp
        self.att = att
        self.de = de
        self.sp = sp
        self.acc = acc
        self.skills = skills
        self.tempo = tempo

class CatEnemy:
    def __init__(self, name, hp, att, de, sp, acc, skills, tempo, defeated):
        self.name = name
        self.hp = hp
        self.att = att
        self.de = de
        self.sp = sp
        self.acc = acc
        self.skills = skills
        self.tempo = tempo
        self.defeated = defeated

def rollcat(name, friendly=True):
    prefixes = name.strip().split(' ')
    prefixes = prefixes[0:len(prefixes)-2]
    pram = len(prefixes)

    # Random stat offset
    ghealth = random.randint( -50, 50 )
    gatt = random.randint( -10, 10 )
    gdef = random.randint( -10, 10 )
    gacc = random.randint( -20, 20 )

    # First table run
    kittystats = [ 100 * pram + ghealth, 10 * pram + gatt, pram * 5 + gdef, 1, pram * 10 + gacc ]

    # Apply static prefix changes
    for i in range( pram ):
        script.doprefixstats( prefixes[i-1], kittystats )

    # Roll skills
    kittyskills = []

    for i in range( pram + 1 ):
        kittyskills.append( allskills[ random.randint(0, len(allskills)-1)] )

    # Incremental skill rolls
    while True:
        numb = random.randint( 0, 100 ) + 5 * pram
        if numb > 90:
            kittyskills.append( allskills[ random.randint(0, len(allskills)-1)] )
        else:
            break

    # Last setup
    kittystats[3] = max( 1, kittystats[3]) # At least 1 speed
    if friendly:
        kitty = Cat( name, kittystats[0], kittystats[1], kittystats[2], kittystats[3], kittystats[4], kittyskills, kittystats[3] )
    else:
        kitty = CatEnemy( name, kittystats[0], kittystats[1], kittystats[2], kittystats[3], kittystats[4], kittyskills, kittystats[3], False )

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

    for i in range( 10 ):
        # 0-3: one prefix
        if i < 4:
            prefixes = 1
        # 4-6: two prefix
        elif i < 7:
            prefixes = 2
        # 7-8: three pref
        elif i < 9:
            prefixes = 3
        else:
            prefixes = 4

        name = rollname( prefixes )
        newenemy = rollcat( name, False )
        enemies.append( newenemy )

    with open("scripts/save/arena_enemies.json", "w") as f:
        json.dump([cat.__dict__ for cat in enemies], f, indent=4)