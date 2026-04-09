import scripts.data as d
import random
prefixes = d.prefixtable

print(" _._     _,-'""`-._")
print("(,-.`._,'(       |\`-/|")
print("    `-.-' \ )-`( , o o)")
print("          `-    \`_`"'-')

print( "FIXME srim cat text" )



# Text [next refresh]
# List of cats
# Current enemy cats


# Honour cat
# Index input to make a cat a fighter. 
# Must be affixless cat
# Price to honour depends on number of affixes
    # 1: 500
    # 2: 5000
    # 3: 25000
    # 4: 100000
# Max 10 slots. Eventually make so need more Treat stock to unlock more slots

# Remove cat from inventory
# Add it to cat scrims save
# Calculate stats from prefixes
# Add random stat offset from prefix amount
# 1: 
# 2:
# 3:
# 4:
# Roll skills
# Cat save format in file: [ cat name, stats offset, skills table ]




# Routine. Generate new enemies and save them to save/scrim_enemies.txt
def refresh_opponents():
    newtbl = []
    for i in range(1,5):
        prefixtable = []
        for o in range(1,i +1):
            prefixtable.append(prefixes[ random.randint( 0, d.prefixmax ) ])
        cube = ' '.join(prefixtable) + ' Kitty'
        newtbl.append(cube)
    
    newtbl.append( ["Dumb Dumb Kitty", [1,2,3,4 ]] )

    with open( d.selfpath + 'save/enemies.txt', 'w' ) as file:
        for enemy in newtbl:
            file.write( enemy + '\n' )

refresh_opponents()