import scripts.data as d
import scripts.funcs as f

inventory = d.inventory

def arenarun():
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
    
    if last == "Kitty":

    else:
        input("FIXME not kitty")
        f.clear()

def gladiatecat(name):


arenarun()