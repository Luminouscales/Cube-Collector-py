# 2026.03.05 Refactored version, mostly

import random
import scripts.funcs as f
import scripts.gallery as gal

verdate = "23.04.2026"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# When the player inputs "help". Lists an explanation of the game and commands.
def helpguide():
    inputs1( input("Available commands: \ninventory\nregistry\nstore\njobs\ndailybox\ntreats\ngallery\nforge\n") )

# "debug" input to make the program close so I can run commands
def debug():
    pass

# Place to earn cash
def jobs():
    f.clear()
    plinput = input( "Welcome to the jobs section! You can earn cash here. Choose an activity to take your time!\nguessgame, typetiming, reflex, catbed\n" )
    match plinput.lower():
        case "exit": return
        case "guessgame": guessgame()
        case "typetiming": typetimingrun(1)
        case "reflex": reflexgame()
        case "catbed": catbedfile()

def guessgame():
    import scripts.guessgame as gg
    gg.guessgame()

def freecash():
    import scripts.data as d
    d.addcredits( 10000 )
    d.saveinv()

def inp_inv():
    import scripts.inventory as inv
    inv.inp_inv( True )

def inp_reg():
    import scripts.registry as reg
    reg.inp_reg()

def inp_store():
    import scripts.store as st
    st.store()

def dailybox():
    import scripts.dailybox as db
    db.dailybox()

def treatsrun():
    import scripts.treats as tr
    tr.treats()

def gallery():
    gal.inp_gallery()

def typetimingrun():
    import scripts.typetiming
    scripts.typetiming.typetiming()

def reflexgame():
    import scripts.reflex
    scripts.reflex.reflexrun()

def forge():
    import scripts.forge
    scripts.forge.forge()

def catbedfile():
    import scripts.catbed
    scripts.catbed.catbed()

# List of inputs for the player to utilise.
player_inputs = {
    "help": helpguide,
    "inventory": inp_inv, "inv": inp_inv, "i": inp_inv,
    "registry": inp_reg, "reg": inp_reg,
    "store": inp_store, "s": inp_store,
    "jobs": jobs,
    "dailybox": dailybox,
    "treats": treatsrun, "tr": treatsrun,
    "meow": freecash,
    "gallery": gallery,
    "forge": forge
}

# Gallery flavour texts
flavtext = [ "is looking at you expectantly...",
"is gazing at you with wide eyes...",
"is sleeping soundly on a high perch.",
"is tearing up the scratching post!",
"is chewing on a Treat Ticket",
"is chewing on a Kittycoin",
"is half-stuck in the cat dimension",
"is rearranging its fur schema",
"just de-ranked in Deadlock...",
"is playing WoW on your PC!",
"is planning a cat rebellion... eventually.",
"is smoking a cigarette",
"is smoking a fatass doink"
]

print(flavtext[0])

# Input def for main inputs
def inputs1( player_input ):
    player_input = player_input.lower() # .lower() for ignoring capitalisation
    if player_input in player_inputs:
        # Check if it's inventory to apply its bool correctly
        player_inputs[player_input]()
    else:
        player_input = inputs1( input("Meow, I don't get what you're saying... ") )

while True:
    f.clear()

    print( "           __..--''``---....___   _..._    __" )
    print(  "/// //_.-'    .-/';  `        ``<._  ``.''_ `. / // /" )
    print( '///_.-" _..--."_    |                    `( ) ) // //' )
    print( "/ (_..-' // (< _     ;_..__               ; `' / ///" )
    print( " / // // //  `-._,_)' // / ``--...____..-' /// / //" )

    # Gallery flavour text
    if len(gal.gallery) > 0 and random.randint(1,5) == 1:
        randcat = gal.gallery[random.randint(0, len(gal.gallery)-1) ]
        randtext = flavtext[random.randint(0, len(flavtext)-1)]
        print( f"The {randcat} {randtext}\n" )

    inputs1( input( 'Meow! Welcome to Kitty Collector version ' + verdate + '. For help, type "help".\n\n' ) )








# The Plaza
# You can open your dailybox there.
# You can also receive support from your fed cats here
    # At any time you can donate credits to feed cats. Afterwards, every day you get a portion of that money back, as thanks from the cats
    # Maybe this could also unlock stuff?
    # Think: you can unbox Treat Tickets which can be consumed for this stockpile


# You can also talk to the Phu'Sea (Fussy) Vendor here, who will seek Cats with certain Prefixes here every day.
    # You can match them partially or completely. A complete match for 2+ prefixes yields A LOT of cash since it's rare.
    # A partial match is still worth it though.
    # He accepts only one Prefix sale per day

# Continuity mechanics. Something to work for. Unlocks, investments
    # Something that upgrades the payout from Guessgame
    # Gives money for unlocking more and more of the registry