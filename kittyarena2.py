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

import json, random
import kaprefixes as script

with open( "scripts/content/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1


class Cat:
    def __init__(self, name, attack, defense, hp, skills):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.skills = skills
 
cat = Cat("Pixel", 12, 12, 12, ["Test1", "Test2"] )

cat_data = cat.__dict__

with open("cat.json", "w") as f:
    json.dump(cat_data, f)

# loading back
with open("cat.json", "r") as f:
    data = json.load(f)

loaded_cat = Cat(**data)

print( loaded_cat.name )

#------------------------------

prefixes = []
for _ in range(3):
    prefixes.append(prefixtable[ random.randint( 0, prefixmax ) ])

prefixamount = len(prefixes)

kitty1 = ""
kitty1 = ' '.join(prefixes) + ' Kitty'
#///

# Random stat offset
ghealth = random.randint( -50, 50 )
gatt = random.randint( -10, 10 )
gdef = random.randint( -10, 10 )
gacc = random.randint( -20, 20 )

# First table run
kitty1stats = [ 100 + ghealth, 10 + gatt, 0 + gdef, 1, 0 + gacc ]

# Apply static prefix changes
for i in range( prefixamount ):
    script.doprefixstats( prefixes[i-1], kitty1stats )

print( kitty1 )
print( kitty1stats )