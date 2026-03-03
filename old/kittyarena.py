import os, sys, random, math

selfpath = os.path.dirname(sys.argv[0])
prefixvar = 5 # How many prefixes the Kitties will appear with

# Ability tier, how strong the values are
# Roll how many abilties, odds stacking

# Flurry / Windfury - chance for a bonus attack regardless of speed
# Resilience - gain stat boost on lower hp
# Second Wind - revive
# Crit - crit
# Parry - parry
# Reflect - hard to code


# The odds for the next Kitty to be stronger by this amount. 0.5 is a good chance.
# 1 will make the enemy AT LEAST equal in power. 2 will make enemies deal at least double damage. 
# Anything higher will make it even harder to win for the winner.
# This is Effective Power so the enemy may deal more damage, not accounting for accuracy.
difficulty = 0.75

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
    kitty1power = math.floor( kitty1power )

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
    kitty2power = math.floor( kitty2power )

    kitty2save = kitty2stats[0]
    kitty2wins = 0

createkitty1()
createkitty2()

global kitty1rank
global kitty2rank
kitty1rank = 1
kitty2rank = 2

def dopower():
    global kitty1epower
    global kitty2epower

    kitty1epower = ( max( kitty1stats[1] - kitty2stats[2], 1 ) ) * ( max( kitty1stats[3] / max(kitty2stats[3],1), 1 ) )
    kitty2epower = ( max( kitty2stats[1] - kitty1stats[2], 1 ) ) * ( max( kitty2stats[3] / max(kitty1stats[3],1), 1 ) )

    tempmult = (kitty1stats[4] - kitty2stats[4]) / 50
    tempmult = max( tempmult, 0.1 )
    tempmult = min( tempmult, 1 )
    kitty1epower = round( kitty1epower * tempmult, 2 )
    
    tempmult = (kitty2stats[4] - kitty1stats[4]) / 50
    tempmult = max( tempmult, 0.1 )
    tempmult = min( tempmult, 1 )
    kitty2epower = round( kitty2epower * tempmult, 2 )

    # 3 - 8 = -5
    # should be a 5 disadvantage 
    # Need at least 25 to guarantee
    # * (acc / 25)

    # 26 disadv
    # 

    # Multiply EP based on accuracy. If you will always hit then mult by 1
    # The minimum hit is like 10
    # kittystats[4] - enemystats[4]
    # Guaranteed is when the modifier is 75 or more
    # So ( kittystats[4] - enemystats[4] ) / 75
    # max( x, 0.1 )
    # min(x, 1)
 
dopower()

#print( f"{kitty1}\n{ kitty1stats } {kitty1power}P {kitty1epower}EP\n" )
#print( f"{kitty2}\n{ kitty2stats } {kitty2power}P {kitty2epower}EP"  )

#input( "" )

# Cats duking it out on a giant ball
# Roll one of the cats to attack first. Then do OwnSpeed - EnemySpeed. If your value is zero or less, move to next turn and repeat.

def leaderboard():
    kitty1vstats = f"| {kitty1stats[0]} HP – {kitty1stats[1]} STR – {kitty1stats[2]} DEF – {kitty1stats[3]} SPD – {kitty1stats[4]} ACC |"
    kitty2vstats = f"| {kitty2stats[0]} HP – {kitty2stats[1]} STR – {kitty2stats[2]} DEF – {kitty2stats[3]} SPD – {kitty2stats[4]} ACC |"

    kitty1filler = ""
    for _ in range( len(str(kitty1rank)) + 1 ):
        kitty1filler = kitty1filler + " "

    kitty2filler = ""
    for _ in range( len(str(kitty2rank)) + 1 ):
        kitty2filler = kitty2filler + " "


    print( f"#{kitty1rank} | {kitty1} | wins: {kitty1wins}\n{kitty1filler} { kitty1vstats } [{kitty1power}P {kitty1epower}EP]\n" )
    print( f"#{kitty2rank} | {kitty2} | wins: {kitty2wins}\n{kitty2filler} { kitty2vstats } [{kitty2power}P {kitty2epower}EP]\n"  )

leaderboard()

#input("")

def proceed():
    input("")
    os.system("cls")
    #leaderboard()

# Function to generate a new cat opponent
def rollcat( loser ):
    global kitty1wins
    global kitty2wins
    global kitty1rank
    global kitty2rank


    temp = 0

    if loser == 1:
        kitty2wins += 1
        kitty2stats[0] = kitty2save
        kitty1rank = max( kitty1rank, kitty2rank ) + 1
        while True:
            temp += 1
            createkitty1()
            dopower()
            if kitty2epower * difficulty < kitty1epower:
                break
            if temp > 999:
                os.system('cls')
                input( "Generation is looped - the difficulty is too high, or it's just slow.")
                temp = 0
    else:
        kitty1wins += 1
        kitty1stats[0] = kitty1save
        kitty2rank = max( kitty1rank, kitty2rank ) + 1
        while True:
            temp += 1
            createkitty2()
            dopower()
            if kitty1epower * difficulty < kitty2epower:
                break
            if temp > 999:
                os.system('cls')
                input( "Generation is looped - the difficulty is too high, or it's just slow.")
                temp = 0



def DoTurn( kittystats, kittyname, enemystats, enemyname, newturn ):
    if newturn:
        proceed()
    
    global zoomies # 20 minutes for a single line of code... I don't know why you need to do this twice.
    global kitty1wins
    global kitty2wins # These two special cats for some reason need a global tag. Don't caaare

    if newturn:
        zoomies = kittystats[3]
    zoomies -= enemystats[3]
    # If you have more than 0 actions but still less than the enemy, 
    # convert leftover energy to damage
    bonus = 1
    lasthit = zoomies < enemystats[3]
    if zoomies > 0 and zoomies < enemystats[3]: 
        bonus += zoomies / enemystats[3]
        zoomies = 0
    damage = math.floor( ( kittystats[1] - enemystats[2] ) * max( bonus, 1 ) * ( random.randint( 5, 20 ) / 10 ) )

    damage = max(damage, 1) # At least 1 damage
    # Accuracy check, 25% chance to miss by default reduced by accuracy and increased by enemy accuracy.
    # But at least 10
    hit = random.randint( 1, 100 ) + max( kittystats[4] - enemystats[4], -65 )
    hit = min( hit, 95 ) # Always 5% chance to miss
    if hit < 25:
        leaderboard()
        print( f"The { kittyname } misses... [rolled {hit} out of 25]" ) # FIX add flashy actions
        if zoomies < 1:
            DoTurn( enemystats, enemyname, kittystats, kittyname, True )
        else:
            DoTurn( kittystats, kittyname, enemystats, enemyname, False )
    else:
        enemystats[0] -= damage  # Gets scratched
        leaderboard()
        print( f"The {enemyname} takes {damage} damage and now has {enemystats[0]} HP! [{hit} out of 25]")
        # Check if defeated
        if enemystats[0] < 1:
            print( f"The {enemyname} has been defeated by the {kittyname}!")
            input("Continue?")
            os.system('cls')
            # Continue the gauntlet!
            # See that pitiful pile of pink scales? It moves for nobody.
            if kitty1stats[0] < 1:
                rollcat( 1 )
            else:
                rollcat( 2 )
            #dopower()
            #leaderboard()
            startrandom()
        else: # If alive, do speed calculations
            leaderboard()
            if zoomies < 1:
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
