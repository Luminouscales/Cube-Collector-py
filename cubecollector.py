# 2026.03.05 Refactored version, mostly

import os

verdate = "26.03.05"

# When the player inputs "help". Lists an explanation of the game and commands.
def helpguide():
    inputs1( input("Available commands: \ninventory\nregistry\nstore\njobs\ndailybox\ntreats\ngallery\n") )

# "debug" input to make the program close so I can run commands
def debug():
    pass

# Place to earn cash
def jobs():
    os.system('cls')
    plinput = input( "Welcome to the jobs section! You can earn cash here. Choose an activity to take your time!\nguessgame\n" )
    if plinput.lower() == "exit":
        return
    elif plinput.lower() == "guessgame":
        guessgame()

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
    st.inp_store()

def dailybox():
    import scripts.dailybox as db
    db.dailybox()

def treatsrun():
    import scripts.treats as tr
    tr.treats()

def gallery():
    import scripts.gallery
    scripts.gallery.inp_gallery()

# List of inputs for the player to utilise.
player_inputs = {
    "help": helpguide,
    "inventory": inp_inv, "inv": inp_inv,
    "registry": inp_reg, "reg": inp_reg,
    "store": inp_store, "shop": inp_store,
    "jobs": jobs,
    "dailybox": dailybox,
    "treats": treatsrun, "tr": treatsrun,
    "meow": freecash,
    "gallery": gallery
}

# Input def for main inputs
def inputs1( player_input ):
    player_input = player_input.lower() # .lower() for ignoring capitalisation
    if player_input in player_inputs:
        # Check if it's inventory to apply its bool correctly
        player_inputs[player_input]()
    else:
        player_input = inputs1( input("Meow, I don't get what you're saying... ") )

while True:
    os.system('cls')

    print( "           __..--''``---....___   _..._    __" )
    print(  "/// //_.-'    .-/';  `        ``<._  ``.''_ `. / // /" )
    print( '///_.-" _..--."_    |                    `( ) ) // //' )
    print( "/ (_..-' // (< _     ;_..__               ; `' / ///" )
    print( " / // // //  `-._,_)' // / ``--...____..-' /// / //" )

    inputs1( input( 'Meow! Welcome to Kitty Collector version ' + verdate + '. For help, type "help".\n' ) )








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