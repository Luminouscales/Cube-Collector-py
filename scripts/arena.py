# Okay we can gladiate and load cats, stats and all
# That's ready. We don't have enemies yet
# "enemies" command to display enemies tab?

# When you go into enemies: every 15 min, roll new ones
# Enemies need to have a "defeated" bool
# First do it simple. First 4: one prefix; next 3: double; next 2: triple; last: quad

# First, make a func to roll and save enemy cats

import scripts.data as d
import scripts.funcs as f
import scripts.rollcatsforarena as r

import os, json

inventory = d.inventory
global loaded_cats

catdir = "scripts/save/arena_cats.json"

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

def maincat():
    print("          _W        W_")
    print("        _) \\      // (_")
    print("      _)    \\    //    (_")
    print("    _)    )\  \  /  /(    (_")
    print("  _)     / )\  \/  /( \     (_")
    print("_)       /  )\,..,/(  \       (_")
    print("_)       \ / _ ) (_ \ /       (_")
    print(" )_       \ (@)  (@) /       _(")
    print("  )_       \_   Y  _/       _(")
    print("   )_        \__-_/        _(")
    print("    )_       /    \       _(")
    print("     )_     |      |     _(")

def arenarun():
    global loaded_cats
    f.clear()

    maincat()

    print("FIXME arena text")
    print("List of fighters, active/time of recovery")
    print("Enemy list")
    print("use, exit, enemies")

    # Print list of available cats
    if os.path.exists(catdir) == False:
        print("FIXME no cats")
    else:
        with open(catdir, "r") as file:
            data = json.load( file )
        loaded_cats = [Cat(**cat_data) for cat_data in data]

        for cat in loaded_cats:
            print( cat.name )

    while True:
        plinput = input("\n\n")
        
        match plinput:
            case "exit" | "e": return
            case "use": case_use()
            case "enemies" | "en": hub_enemies()

def case_use():
    plinput = input("index")
    index = int(plinput)
    catname = inventory[index][0].strip().split(' ')
    last = catname[ len(catname) - 1 ]
    
    if last == "Kitty" and len(catname) > 1:
        gladiatecat(inventory[index][0])
    else:
        input("FIXME not kitty or not prefixed")
        f.clear()

def gladiatecat(name):
    global loaded_cats

    fullcat = r.rollcat(name)

    loaded_cats.append( fullcat )

    with open(catdir, "w") as f:
        json.dump([cat.__dict__ for cat in loaded_cats], f, indent=4)

# Enemies tab. Display time until reset, given enemies
def hub_enemies():
    while True:
        f.clear()
        maincat()
        print("")

        # Check if to roll for new enemies:
        if d.TimePassedBool( d.dates["newenemies"], 15 ):
            r.rollcatenemies()

        # Read new enemies
        times = d.ReturnTimeUntil( d.dates["newenemies"] )
        print("Time until reset:")


arenarun()