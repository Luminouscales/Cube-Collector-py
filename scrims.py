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


# Routine. Generate new enemies and save them to save/scrim_enemies.txt
def refresh_opponents():
    newtbl = []
    for i in range(1,5):
        prefixtable = []
        for o in range(1,i +1):
            prefixtable.append(prefixes[ random.randint( 0, d.prefixmax ) ])
        cube = ' '.join(prefixtable) + ' Kitty'
        newtbl.append(cube)

    with open( d.selfpath + 'save/enemies.txt', 'w' ) as file:
        for enemy in newtbl:
            file.write( enemy + '\n' )

refresh_opponents()