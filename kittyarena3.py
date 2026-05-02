import json, random, os, time

debug = True

def Debug( msg ):
    if debug: print(msg + "\n")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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

# Set up both cats
# FIXME This will be changed later

with open("cat.json", "r") as f:
    data1 = json.load(f)

with open("cat2.json", "r") as f:
    data2 = json.load(f)

kitty1 = Cat(**data1)
kitty2 = Cat(**data2)

kitty1health = kitty1.hp
kitty2health = kitty2.hp
# Tempo is how many times the cat can act each turn, carrying over
kitty1tempo = kitty1.tempo
kitty2tempo = kitty2.tempo

global logstack
logstack = []

#/----------------------------/
# FUNCTIONS
#/----------------------------/

def leaderboard():
    kitty1vstats = f"| {kitty1.hp} HP – {kitty1.att} STR – {kitty1.de} DEF – {kitty1.sp} SPD – {kitty1.acc} ACC | {kitty1.tempo} TEMPO"
    kitty2vstats = f"| {kitty2.hp} HP – {kitty2.att} STR – {kitty2.de} DEF – {kitty2.sp} SPD – {kitty2.acc} ACC | {kitty2.tempo} TEMPO"

    print( f"# {kitty1.name} { kitty1vstats }" )
    print( f"# {kitty2.name} { kitty2vstats }" )

# Used to print text of what is happening
def PrintTable( table, interval ):
    for row in table:
        print(row)
        # A little delay if there's more than one thing in the log
        if len(table) > 1 or row == len(table)+1:
            time.sleep( interval )

def DoTurn( attacker, defender ):
    BasicAttack( attacker, defender )

# Normal cat attack. No skills.
def BasicAttack( attacker, defender ):
    global battle
    global logstack
    # Accuracy check, 25% chance to miss by default reduced by accuracy and increased by enemy accuracy.
    # But at least 10
    hit = random.randint( 1, 100 ) + ( attacker.acc - defender.acc )
    hit = max( hit, 10 ) # Always 10% chance to hit at least
    hit = min( hit, 95 ) # Always 5% chance to miss at least

    # If hit
    if random.randint( 1, 100 ) < hit:
        damage = attacker.att - defender.de
        damage = damage * ( random.randint( 7, 15 ) / 10 ) # Random offest
        damage = max( 1, int(damage) ) # At least 1, and rounded

        # Returns False if target is dead
        if DealDamage( attacker.name, defender, damage ):
            Debug( f"BASIC ATTACK: {attacker.name}")
        else:
            battle = False
    else:
        logstack.append(f"{attacker.name} missed")
        Debug( f"BASIC ATTACK MISSED: {attacker.name}")

# Deal damage to target; returns whether should continue or not (dead or not)
# Returns False if target is dead
def DealDamage( attacker, target, damage ):
    global logstack
    target.hp -= damage
    Debug( f"TOOK DAMAGE: {target.name}")
    logstack.append( f"{attacker} dealt {damage} damage" )
    if target.hp < 1:
        input("battle end")
        return False
    else:
        return True
    
# Manages turn order, speed of actions and tempo overflow
def DoTempo(attacker, defender):
    tempo = True
    while tempo:
        if attacker.tempo >= defender.sp: # C1 has 2 tempo, C2 has 1. C1 acts
            Debug(f"ATTACK TEMPO START: {attacker.tempo} against {defender.sp}")
            attacker.tempo = max( 0, attacker.tempo - defender.sp ) # C1 loses tempo equal to C2 speed, but not less than 0
            Debug(f"ATTACKS: {attacker.name}; TEMPO: {attacker.tempo} against {defender.sp}")
            DoTurn( attacker, defender )
        else: # C1 has acted twice. It now regains tempo equal to its speed and passes
            Debug(f"OVERFLOWED; {attacker.tempo} against {defender.sp}")
            attacker.tempo += attacker.sp
            Debug(f"OVERFLOW: {attacker.name} TEMPO now: {attacker.tempo} against {defender.sp}")
            tempo = False

# Start
global battle
battle = True
side = 0 # One attacks, then the other

while battle:
    
    side += 1
    clear()
    
    Debug("START")

    logstack = []
    
    if side % 2 == 0:
        Debug(f"TURN OF: {kitty1.name} ")
        DoTempo( kitty1, kitty2)
    else:
        Debug(f"TURN OF: {kitty2.name} ")
        DoTempo( kitty2, kitty1 )
        
    # Text
    Debug("LEADERBOARD")
    leaderboard()
    PrintTable( logstack, 0.5 )

    # Just skip if nothing happened
    if len(logstack) > 0:
        input("")

