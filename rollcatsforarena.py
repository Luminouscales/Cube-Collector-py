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

import json, random, os
import kaprefixes as script

allskills = script.allskills

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "scripts", "content", "prefixes.txt")

with open( file_path, 'r' ) as file:
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
 
#cat = Cat("Pixel", 12, 12, 12, ["Test1", "Test2"] )

#cat_data = cat.__dict__

#with open("cat.json", "w") as f:
    #json.dump(cat_data, f)

# loading back
#with open("cat.json", "r") as f:
    #data = json.load(f)

#oaded_cat = Cat(**data)

#print( loaded_cat.name )

#------------------------------

prefixes = []
for _ in range(3):
    prefixes.append(prefixtable[ random.randint( 0, prefixmax ) ])

pram = len(prefixes) # Prefix amount

kitty1name = ""
kitty1name = ' '.join(prefixes) + ' Kitty'
#///

# Random stat offset
ghealth = random.randint( -50, 50 )
gatt = random.randint( -10, 10 )
gdef = random.randint( -10, 10 )
gacc = random.randint( -20, 20 )

# First table run
kitty1stats = [ 100 * pram + ghealth, 10 * pram + gatt, pram * 5 + gdef, 1, pram * 10 + gacc ]

# Apply static prefix changes
for i in range( pram ):
    script.doprefixstats( prefixes[i-1], kitty1stats )

# Roll skills

kitty1skills = []

for i in range( pram ):
    kitty1skills.append( allskills[ random.randint(0, len(allskills)-1)] )

# Incremental skill rolls
while True:
    numb = random.randint( 0, 100 ) + 5 * pram
    print( numb )
    if numb > 90:
        kitty1skills.append( allskills[ random.randint(0, len(allskills)-1)] )
    else:
        break

# Last setup
kitty1stats[3] = max( 1, kitty1stats[3]) # At least 1 speed
kitty1 = Cat( kitty1name, kitty1stats[0], kitty1stats[1], kitty1stats[2], kitty1stats[3], kitty1stats[4], kitty1skills, kitty1stats[3] )

# Save?

cat_data = kitty1.__dict__

with open("cat.json", "w") as f:
    json.dump(cat_data, f)

print( kitty1name )
print( kitty1stats )
print( kitty1skills )


def rollcat(name):
    prefixes = name.strip().split(' ')
    prefixes = prefixes[0:len(prefixes)-2]

    # Random stat offset
    ghealth = random.randint( -50, 50 )
    gatt = random.randint( -10, 10 )
    gdef = random.randint( -10, 10 )
    gacc = random.randint( -20, 20 )

    # First table run
    kitty1stats = [ 100 * pram + ghealth, 10 * pram + gatt, pram * 5 + gdef, 1, pram * 10 + gacc ]