import scripts.data as d
import scripts.funcs as f

import os, json

inventory = d.inventory
global loaded_cats

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

def arenarun():
    global loaded_cats
    f.clear()

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

    print("FIXME arena text")
    print("List of fighters, active/time of recovery")
    print("Enemy list")
    print("use")

    # Print list of available cats
    if os.path.exists("scripts/save/arena_cats.json") == False:
        print("FIXME no cats")
    else:
        with open("scripts/save/arena_cats.json", "r") as file:
            data = json.load( file )
        loaded_cats = [Cat(**cat_data) for cat_data in data]

        for cat in loaded_cats:
            print( cat.name )


    print("\n")

    while True:
        plinput = input("use")
        
        match plinput:
            case "exit" | "e": return
            case "use": case_use()

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

    import scripts.rollcatsforarena as r

    fullcat = r.rollcat(name)
    print(fullcat.att)

    loaded_cats.append( fullcat )
    print( loaded_cats )

arenarun()