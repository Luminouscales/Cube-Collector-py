import os, sys, random, math

selfpath = os.path.dirname(sys.argv[0])
prefixvar = 3 # How many prefixes the Kitties will appear with

# The odds for the next Kitty to be stronger by this amount. 0.5 is a good chance.
# 1 will make the enemy AT LEAST equal in power. 2 will make enemies deal at least double damage. 
# Anything higher will make it even harder to win for the winner.
# This is Effective Power so the enemy may deal more damage, not accounting for accuracy.
difficulty = 0.5

with open( selfpath + "/prefixes.txt", 'r' ) as file:
    lines = file.readlines()
    prefixtable = [line.strip() for line in lines]
    prefixmax = len(prefixtable) - 1

def doprefixstats( prefixes, statstable ):
    match prefixes:
        case "Big":
            statstable[0] += 20
            statstable[1] += 5
            statstable[3] -= 2
        case "Small":
            statstable[0] -= 20
            statstable[1] -= 5
            statstable[3] += 2
        case "Fast" | "Quick":
            statstable[3] += 1
        case "Dynamic":
            statstable[3] += 2
        case "Shapeless" | "Intemporal" | "Abstract":
            statstable[3] += 3
        case "Slow":
            statstable[3] -= 3
        case "Happy" | "Merry":
            statstable[0] += 10
            statstable[3] += 2
        case "Sad":
            statstable[0] -= 5
            statstable[3] -= 1
        case "Bright":
            statstable[4] += 5
        case "Loud" | "Noisy":
            statstable[1] += 5
            statstable[4] -= 5
        case "Quiet":
            statstable[1] -= 5
            statstable[4] += 5
        case "Tall":
            statstable[1] += 5
        case "Short":
            statstable[3] += 1
        case "Thin" | "Light":
            statstable[2] -= 2
            statstable[3] += 1
        case "Thick" | "Heavy":
            statstable[2] += 5
            statstable[3] -= 2
        case "Hard":
            statstable[2] += 5
        case "Soft":
            statstable[2] -= 5
        case "Strong":
            statstable[1] += 10
        case "Weak":
            statstable[1] -= 10
        case "Sharp":
            statstable[4] += 10
            statstable[1] += 5
        case "World-Ending":
            statstable[0] += 50
            statstable[1] += 20
            statstable[2] += 10
            statstable[3] += 3
            statstable[4] -= 25
        case "Dull":
            statstable[4] -= 10
        case "New" | "Healthy" | "True" | "Expensive" | "Right" | "Optimized" | "Efficient":
            statstable[0] += 10
            statstable[4] += 2
            statstable[1] += 2
            statstable[2] += 2
            statstable[3] += 1
        case "Old" | "Sick" | "False" | "Cheap" | "Wrong" | "Shitty" | "Useless" | "Pathetic":
            statstable[0] -= 10
            statstable[4] -= 2
            statstable[1] -= 2
            statstable[2] -= 2
            statstable[3] -= 1
        case "Wise" | "Calm":
            statstable[4] += 15
        case "Foolish":
            statstable[4] -= 5
        case "Brave":
            statstable[3] += 2
            statstable[1] += 5
            statstable[2] += 5
            statstable[0] += 10
        case "Cowardly":
            statstable[3] -= 1
            statstable[2] -= 5
        case "Brilliant":
            statstable[0] += 20
            statstable[4] += 4
            statstable[1] += 4
            statstable[2] += 4
            statstable[3] += 1
        case "Supreme":
            statstable[0] += 25
            statstable[4] += 6
            statstable[1] += 6
            statstable[2] += 6
            statstable[3] += 2
        case "Unreal" | "Ascended" | "Godly":
            statstable[0] += 30
            statstable[4] += 8
            statstable[1] += 8
            statstable[2] += 8
            statstable[3] += 3
        case "Dumb" | "Stupid":
            statstable[4] -= 10
        case "Kind":
            statstable[1] -= 2
            statstable[0] += 5
        case "Cruel" | "Evil":
            statstable[1] += 5
        case "Polite":
            statstable[1] -= 2
        case "Rude" | "Scary" | "Angry":
            statstable[3] += 1
            statstable[1] += 2
        case "Boring":
            statstable[3] -= 5
        case "Safe":
            statstable[0] += 10
            statstable[2] += 5
        case "Dangerous":
            statstable[1] += 10
            statstable[3] += 2
        case "Hungry":
            statstable[1] -= 2
            statstable[2] -= 2
        case "Full":
            statstable[3] -= 1
            statstable[2] += 5
        case "Profaned":
            statstable[0] += 10
            statstable[1] += 10
            statstable[2] -= 10
            statstable[3] += 2
            statstable[4] -= 15
        case "Auric" | "Draconic":
            statstable[0] += 20
            statstable[1] += 10
            statstable[2] += 10
            statstable[3] -= 4
            statstable[4] -= 20
        case "Calamitous":
            statstable[1] += 30
            statstable[2] -= 15
            statstable[4] -= 25
        case "Cobalt":
            statstable[0] += 5
            statstable[1] += 2
            statstable[2] += 2
            statstable[3] += 1
            statstable[4] += 2
        case "Mythril":
            statstable[0] += 10
            statstable[1] += 3
            statstable[2] += 3
            statstable[3] += 2
            statstable[4] += 3
        case "Titanium":
            statstable[0] += 15
            statstable[1] += 5
            statstable[2] += 5
            statstable[3] += 3
            statstable[4] += 5
        case "Iron" | "Galvanized":
            statstable[0] += 3
            statstable[1] += 1
            statstable[2] += 1
            statstable[3] += 1
            statstable[4] += 1
        case "Plastic":
            statstable[0] -= 3
            statstable[1] -= 1
            statstable[2] -= 1
            statstable[3] -= 1
            statstable[4] -= 1
        case "Shattered":
            statstable[2] -= 10
        case "Rusty":
            statstable[2] -= 5
            statstable[1] -= 5
        case "Feline" | "Kitty" | "Clever":
            statstable[4] += 5
            statstable[3] += 2
        case "Perseverant":
            statstable[0] += 20
            statstable[2] += 10


kitty2stats = [ 100, 10, 0, 1, 0 ]

def createkitty1():
    global kitty1stats
    global kitty1
    global kitty1power
    global kitty1save
    global kitty1wins

    prefixes = []
    for idx in range(prefixvar):
        prefixes.append(prefixtable[ random.randint( 0, prefixmax ) ])

    kitty1 = ""
    kitty1 = ' '.join(prefixes) + ' Kitty'
    kitty1stats = [ 100, 10, 0, 1, 0 ]

    kittyprefixes = kitty1.strip().split(' ') 
    # Delete Kitty from prefix table
    kittyprefixes.pop( len(kittyprefixes)-1 )

    for i in range( len(kittyprefixes) ):
        doprefixstats( kittyprefixes[i], kitty1stats )

    kitty1stats[0] = max(kitty1stats[0], 1 )
    kitty1stats[1] = max(kitty1stats[1], 1 )
    kitty1stats[3] = max(kitty1stats[3], 1 )

    kitty1power = 0
    kitty1power += kitty1stats[0] - 100 / 10 
    kitty1power += kitty1stats[1] - 1 
    kitty1power += kitty1stats[2] / 2
    kitty1power += kitty1stats[4] / 5
    kitty1power *= kitty1stats[3]

    kitty1save = kitty1stats[0]
    kitty1wins = 0

def createkitty2():
    global kitty2stats
    global kitty2
    global kitty2power
    global kitty2save
    global kitty2wins

    prefixes = []
    for idx in range(prefixvar):
        prefixes.append(prefixtable[ random.randint( 0, prefixmax ) ])

    kitty2 = ""
    kitty2 = ' '.join(prefixes) + ' Kitty'
    kitty2stats = [ 100, 10, 0, 1, 0 ]

    kittyprefixes = kitty2.strip().split(' ') 
    # Delete Kitty from prefix table
    kittyprefixes.pop( len(kittyprefixes)-1 )

    for i in range( len(kittyprefixes) ):
        doprefixstats( kittyprefixes[i], kitty2stats )

    kitty2stats[0] = max(kitty2stats[0], 1 )
    kitty2stats[1] = max(kitty2stats[1], 1 )
    kitty2stats[3] = max(kitty2stats[3], 1 )

    kitty2power = 0
    kitty2power += kitty2stats[0] - 100 / 10 
    kitty2power += kitty2stats[1] - 1 
    kitty2power += kitty2stats[2] / 2
    kitty2power += kitty2stats[4] / 5
    kitty2power *= kitty2stats[3]

    kitty2save = kitty2stats[0]
    kitty2wins = 0

createkitty1()
createkitty2()

def dopower():
    global kitty1epower
    global kitty2epower

    kitty1epower = math.floor( ( max( kitty1stats[1] - kitty2stats[2], 1 ) ) * ( max( kitty1stats[3] / kitty2stats[3], 1 ) ) )
    kitty2epower = math.floor( ( max( kitty2stats[1] - kitty1stats[2], 1 ) ) * ( max( kitty2stats[3] / kitty1stats[3], 1 ) ) )

dopower()

print( f"{kitty1}: { kitty1stats } {kitty1power}P {kitty1epower}EP" )
print( f"{kitty2}: { kitty2stats } {kitty2power}P {kitty2epower}EP"  )

input( "" )

# Cats duking it out on a giant ball
# Roll one of the cats to attack first. Then do OwnSpeed - EnemySpeed. If your value is zero or less, move to next turn and repeat.

def leaderboard():
    print( f"{kitty1}: { kitty1stats } {kitty1power}P {kitty1epower}EP | wins: {kitty1wins}" )
    print( f"{kitty2}: { kitty2stats } {kitty2power}P {kitty2epower}EP | wins: {kitty2wins}\n"  )

def proceed():
    print( f"The enemy's turn begins.")
    input("")
    os.system("cls")
    leaderboard()

def DoTurn( kittystats, kittyname, enemystats, enemyname, newturn ):
    global zoomies # 20 minutes for a single line of code... I don't know why you need to do this twice.
    global kitty1wins
    global kitty2wins # These two special cats for some reason need a global tag. Don't caaare

    if newturn:
        zoomies = kittystats[3]
    zoomies -= enemystats[3]
    # If you have more than 0 actions but still less than the enemy, 
    # convert leftover energy to damage
    bonus = 1
    if zoomies > 0 and zoomies < enemystats[3]: 
        bonus += zoomies / enemystats[3]
        zoomies = 0
    damage = math.floor( ( kittystats[1] - enemystats[2] ) * bonus )
    damage = max(damage, 1)
    # Accuracy check, 25% chance to miss by default reduced by accuracy and increased by enemy accuracy.
    # But at least 10
    hit = random.randint( 1, 100 ) + max( kittystats[4] - enemystats[4], -20 ) # FIX
    if hit < 25:
        print( f"The { kittyname } misses... [rolled {hit} out of 75]" ) # FIX add flashy actions
        if zoomies < 1:
            proceed()
            DoTurn( enemystats, enemyname, kittystats, kittyname, True )
        else:
            DoTurn( kittystats, kittyname, enemystats, enemyname, False )
    else:
        enemystats[0] -= damage  # Gets scratched
        print( f"The {enemyname} takes {damage} damage and now has {enemystats[0]} HP!")
        # Check if defeated
        if enemystats[0] < 1:
            print( f"The {enemyname} has been defeated by the {kittyname}!")
            input("Continue?")
            os.system('cls')
            # Continue the gauntlet!
            # See that pitiful pile of pink scales? It moves for nobody.
            if kitty1stats[0] < 1:
                while True:
                    createkitty1()
                    #kitty1stats[0] = kitty1save
                    #kitty1wins += 1
                    dopower()
                    if kitty2epower * difficulty < kitty1epower:
                        break
                kitty2wins += 1
                kitty2stats[0] = kitty2save
            else:
                while True:
                    createkitty2()
                    #kitty1stats[0] = kitty1save
                    #kitty1wins += 1
                    dopower()
                    if kitty1epower * difficulty < kitty2epower:
                        break
                kitty1wins += 1
                kitty1stats[0] = kitty1save
            #dopower()
            leaderboard()
            startrandom()
        else: # If alive, do speed calculations
            if zoomies < 1:
                proceed()
                DoTurn( enemystats, enemyname, kittystats, kittyname, True )
            else:
                DoTurn( kittystats, kittyname, enemystats, enemyname, False )

# Roll which cat first
def startrandom():
    if random.randint( 1, 2 ) == 1:
        DoTurn( kitty1stats, kitty1, kitty2stats, kitty2, True )
    else:
        DoTurn( kitty2stats, kitty2, kitty1stats, kitty1, True )
startrandom()


# Health [0]
# Strength [1]
# Defence [2]
# Speed [3]
# Accuracy [4]
