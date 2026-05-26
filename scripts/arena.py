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

import os, json, math

inventory = d.inventory
global loaded_cats

catdir = "scripts/save/arena_cats.json"
endir = "scripts/save/arena_enemies.json"

class Cat:
    def __init__(self, name, hp, att, de, sp, acc, skills, tempo, defeated):
        self.name = name
        self.hp = hp
        self.att = att
        self.de = de
        self.sp = sp
        self.acc = acc
        self.skills = skills
        self.tempo = tempo
        self.defeated = defeated

class CatEnemy:
    def __init__(self, name, hp, att, de, sp, acc, skills, tempo, defeated):
        self.name = name
        self.hp = hp
        self.att = att
        self.de = de
        self.sp = sp
        self.acc = acc
        self.skills = skills
        self.tempo = tempo
        self.defeated = defeated

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

    while True:

        f.clear()

        maincat()

        print("FIXME arena text")
        print("List of fighters, active/time of recovery")
        print("Enemy list")
        print("use, exit, enemies")

        # Check if to refresh (roll new enemies, heal ally):
        if d.TimePassedBool( d.dates[4][1], 15 ) or os.path.exists(endir) == False:
            r.rollcatenemies()
            d.dates[4][1] = d.TimeNow()
            d.savetime()

            # Refresh all ally cats
            if os.path.exists(catdir):
                with open(catdir, "r") as file:
                    data = json.load( file )
                    loaded_cats = [Cat(**cat_data) for cat_data in data]
                for cat in loaded_cats:
                    cat.defeated = False
                

        # Read new enemies
        times = d.ReturnTimeUntil( d.dates[4][1] )
        print(f"Time until reset: {times[0]} {times[1]}")

        with open(endir, "r") as file:
            data = json.load( file )
        global enemy_cats
        enemy_cats = [CatEnemy(**cat_data) for cat_data in data]
        saveall()

        

        # Print list of available cats
        if os.path.exists(catdir) == False:
            loaded_cats = []
            print("FIXME no cats")
            saveall()
        else:
            with open(catdir, "r") as file:
                data = json.load( file )
            loaded_cats = [Cat(**cat_data) for cat_data in data]
            saveall()

            i = 0
            for cat in loaded_cats:
                i += 1

                if cat.defeated:
                    defd = "[RESTING]"
                else:
                    defd = ""

                print( f"{i}. {cat.name} | {cat.hp}HP {cat.att}ATT {cat.de}DEF {cat.acc}ACC {len(cat.skills)} skills | {defd}" )

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

    pram = d.ReturnPram( inventory[index][0] )

    match pram:
        case 1: price = 500
        case 2: price = 2500
        case 3: price = 10000
        case 4: price = 20000
        case 5: price = 100000
        case 6: price = 500000
        case _: price = math.floor( math.pow(7, pram) )
    
    if last == "Kitty" and len(catname) > 1 and d.inventory[0][1] >= price:
        gladiatecat(inventory[index][0])
        d.InvDelete( index, 1 )
        d.addcredits( -price )
        input("done")
    else:
        input(f"FIXME not kitty or not prefixed or need {price} Credits")
        f.clear()

def gladiatecat(name):
    global loaded_cats

    if not loaded_cats:
        loaded_cats = []

    fullcat = r.rollcat(name)

    loaded_cats.append( fullcat )

    saveall()

def tryfight():
    global enemy_cats

    plinput = input("player")
    player = int(plinput)
    plinput = input("enemy")
    enemy = int(plinput)

    playercat = loaded_cats[player-1]
    enemycat = enemy_cats[ enemy-1 ]

    hpsave1 = playercat.hp
    tpsave1 = playercat.tempo
    attsave1 = playercat.att
    hpsave2 = enemycat.hp
    tpsave2 = enemycat.tempo
    attsave2 = enemycat.att

    # Don't let fight if one cat is defeated
    if playercat.defeated or enemycat.defeated:
        input("one cat is unavailable")
    else:
        import scripts.kittyarena3
        # If True: your cat won, else lost
        if scripts.kittyarena3.startfight( playercat, enemycat ):
            playercat.hp = hpsave1
            playercat.tempo = tpsave1
            playercat.att = attsave1
            enemycat.hp = hpsave2
            enemycat.tempo = tpsave2
            enemycat.att = attsave2

            prefixes = enemycat.name.strip().split(' ')
            prefixes.pop( len(prefixes ) - 1 )
            pram = len(prefixes)

            match pram:
                case 1: credits = 250
                case 2: credits = 1000
                case 3: credits = 2500
                case 4: credits = 7500

            # Set enemy as defeated
            enemy_cats[ enemy-1 ].defeated = True
            saveall()

            input( f"your cat won {credits} credits" )
            d.addcredits( credits )

        else:
            playercat.hp = hpsave1
            playercat.tempo = tpsave1
            playercat.att = attsave1
            enemycat.hp = hpsave2
            enemycat.tempo = tpsave2
            enemycat.att = attsave2

            loaded_cats[player-1].defeated = True
            saveall()
            input("your cat lost")

def saveall():
    global loaded_cats
    global enemy_cats

    if len(loaded_cats) > 0:
        with open(catdir, "w") as f:
            json.dump([cat.__dict__ for cat in loaded_cats], f, indent=4)

    with open(endir, "w") as f:
        json.dump([cat.__dict__ for cat in enemy_cats], f, indent=4)


# Enemies tab. Display time until reset, given enemies
def hub_enemies():
    global loaded_cats
    while True:
        f.clear()

        i = 0
        for cat in enemy_cats:
            i += 1

            if cat.defeated:
                display = "DEFEATED"
            else:
                display = cat.name

            print( f"{i}. {display}" )

        plinput = input("")
        match plinput:
            case "exit" | "e": return
            case "fight": tryfight()



# FIXME
# Clean up code
# Wierd qol bugs