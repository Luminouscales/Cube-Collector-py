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

import random, os
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

def rollcat(name):
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

    for i in range( pram ):
        kittyskills.append( allskills[ random.randint(0, len(allskills)-1)] )

    # Incremental skill rolls
    while True:
        numb = random.randint( 0, 100 ) + 5 * pram
        print( numb )
        if numb > 90:
            kittyskills.append( allskills[ random.randint(0, len(allskills)-1)] )
        else:
            break

    # Last setup
    kittystats[3] = max( 1, kittystats[3]) # At least 1 speed
    kitty1 = Cat( name, kittystats[0], kittystats[1], kittystats[2], kittystats[3], kittystats[4], kittystats, kittystats[3] )

    return kitty1