import json, random, os, time

debug = False

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

def Logstack(text):
    global logstack
    logstack.append( text )

def DoTurn( attacker, defender ):
    # EACH skill has a % chance of activating. First one to activate does that instead of basicattack
    skillproc = False
    for skill in attacker.skills:
        if random.randint( 1, 100 ) < 6:
            Debug( f"SKILL: {skill}")
            RunSkill( skill, attacker, defender )
            skillproc = True
            break
    if not skillproc:
        BasicAttack( attacker, defender )

#/----------------------------/
# SKILLS
#/----------------------------/

def RunSkill( skill, attacker, defender ):
    match skill:
        case "Swipe": skillSwipe( attacker, defender )
        case "Scratch": skillScratch( attacker, defender )
        case "Pounce": skillPounce( attacker, defender )
        case "Tear": skillPounce( attacker, defender )
        case "Flicker": skillFlicker( attacker, defender )
        case "Lick": skillLick( attacker )
        case "Hiss": skillHiss( attacker )
    
# For skills. Returns if should hit or not
def skill_hitchance(chance):
    if random.randint( 1, 100 ) < chance:
        return True
    else:
        return False

# Swipe for 50% more dmg
def skillSwipe( attacker, defender ):
    Logstack( f"{attacker.name} swiped at the enemy!")
    if skill_hitchance( CalcAcc(attacker, defender) ):
        DealDamage( attacker.name, defender, CalcDamage( attacker, defender, attboost=1.5 ) )
    else:
        Logstack( "Swipe missed!" )

# Scratch
def skillScratch( attacker, defender ):
    Logstack( f"{attacker.name} scratched at the enemy!")
    for i in range( 2 ):
        if skill_hitchance( CalcAcc(attacker, defender) ):
            DealDamage( attacker.name, defender, CalcDamage( attacker, defender ) )
        else:
            Logstack( "Scratch missed!" )

# Tear
def skillTear(attacker, defender):
    Logstack( f"{attacker.name} tears the enemy!")
    if skill_hitchance( CalcAcc(attacker, defender) ):
        DealDamage( attacker.name, defender, CalcDamage( attacker, defender, defignore=20 ) )
    else:
        Logstack( "Tear missed!" )

# Flicker
def skillFlicker(attacker, defender):
    Logstack( f"{attacker.name} licks itself...")
    if skill_hitchance( CalcAcc(attacker, defender) ):
        offset = random.randint( 5, 20 ) / 10
        DealDamage( attacker.name, defender, CalcDamage( attacker, defender, attboost=offset ) )
    else:
        Logstack( "Flicker missed!" )

# Lick
def skillLick(attacker):
    Logstack( f"{attacker.name} licks itself...")
    HealTarget( attacker, int(attacker.hp/10))

# Pounce
def skillPounce( attacker, defender ):
    Logstack( f"{attacker.name} pounced at the enemy!")
    DealDamage( attacker.name, defender, CalcDamage( attacker, defender ) )

# Pounce
def skillHiss( attacker ):
    attacker.att += 10
    Logstack( f"{attacker.name} hissed at the enemy and gained 10 attack!")
    

# Normal cat attack. No skills.
def BasicAttack( attacker, defender ):
    global battle
    global logstack

    # If hit
    if random.randint( 1, 100 ) < CalcAcc( attacker, defender ):
        DealDamage( attacker.name, defender, CalcDamage(attacker, defender) )
    else:
        Logstack(f"{attacker.name} missed")
        Debug( f"BASIC ATTACK MISSED: {attacker.name}")

# Returns attack - defense damage
# attboost: boost raw damage by percentage
# attbonus: boost raw damage by flat amount
# defignore: percentage of defence to ignore
# defdecr: amount of defence to ignore
def CalcDamage(attacker, defender, attboost=1, attbonus=0, defignore=1, defdecr=0 ):
    damage = attacker.att * attboost + attbonus 
    damage -= defender.de * defignore - defdecr
    damage = damage * ( random.randint( 7, 15 ) / 10 ) # Random offest
    damage = max( 1, int(damage) ) # At least 1, and rounded

    return damage

# Returns C1speed - C2speed
# force: guaranteed hit
def CalcAcc(attacker, defender, force=False):
    # Accuracy check, 25% chance to miss by default reduced by accuracy and increased by enemy accuracy.
    # But at least 10
    if force:
        return 100
    else:
        hit = random.randint( 1, 100 ) + ( attacker.acc - defender.acc )
        hit = max( hit, 10 ) # Always 10% chance to hit at least
        hit = min( hit, 95 ) # Always 5% chance to miss at least

    return hit

# Deal damage to target; returns whether should continue or not (dead or not)
# Returns False if target is dead
def DealDamage( attacker, target, damage ):
    global logstack
    global battle
    target.hp -= damage
    Debug( f"TOOK DAMAGE: {target.name}")
    Logstack( f"{attacker} dealt {damage} damage" )
    if target.hp < 1:
        input("battle end")
        battle = False
    else:
        battle = True
    
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

def HealTarget( target, amount ):
    target.hp += amount
    Logstack( f"{target.name} healed itself for {amount} health!" )

#/----------------------------/
# START
#/----------------------------/
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