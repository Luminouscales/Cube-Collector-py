# Combine cats here for prefixes
# One prefix: 10
# Two prefix: 2

# Pick two cats from index input
# See if enough amount
# See if unprefixed cats
# Get prefixes from first, then second: combine into same string
# Add to inventory
# Easy

import scripts.data as d
import scripts.funcs as f
import random

inventory = d.inventory

# Random after forge dialogue
dialogue = [ "Whew! Nothing quite gets me going like sweat soaking my fur. A Prefixsmith never really gets used to the heat.", 
    "All in a day's work! Could you fetch some milk from the fridge? Yes, it's on the house!",
    "...why, of course! The process could never work if the cats didn't want to comply in the first place.",
    "A reforged cat is always compatible with its... sum elements, even if it take some time for them to adjust.",
    "Hey, never ask a lady cat her prefixes! But if you really wanna know... I've had about a thousand. Impressive, right?",
    "Dude, have they reopened the Colosseum yet? I wanna test some of my kitties - better yet, fix my own highscore!",
    ]


def forge():

    firstenter = True # For dialogue

    while True:
        f.clear()
        print("    ,-. __ .-,")
        print("  --;`. '   `.'")
        print("   / (  ^__^  )")
        print("  ;   `(_`'_)' /")
        print("  '  ` .`--'_,  ;")
        print("~~`-..._)))(((.'")
        if firstenter:
            print("Welcome to my Forge! They know me as the Lady of the Hammer around here. I know how to combine cats of similar elusive properties into " \
            "a single feline, shaped to your liking. It takes 10 cats each of single prefix, or 2 of double prefix - but no more!\n")
        else:
            print( f"{dialogue[random.randint(0,len(dialogue)-1)]}\n"  )

        inptable = input("forge [index] [index] | or exit\n\n")
        inptable = inptable.strip().split('\t')

        command = inptable[0]
        match command:
            case "exit" | "e": return
            case "forge": forge_forge(inptable[1], inptable[2])


def forge_forge(index1, index2):
    index1 = int(index1)
    index2 = int(index2)

    cat1 = inventory[index1][0]
    cat1count = inventory[index1][1]
    cat2 = inventory[index2][0]
    cat2count = inventory[index2][1]

    catstbl = [ cat1, cat2 ]
    prefixcount = []

    step1 = True
    # See if unaffixed kitty
    for cat in catstbl:
        cattable = cat.strip().split(' ')
        prefixamount = len(cattable) - 1
        # Prefixes can't be more than two
        if prefixamount > 2:
            step1 = False
            input("A cat fit for reforging may not have more than two prefixes.")
            break
        prefixcount.append( prefixamount )
        if cattable[prefixamount] != "Kitty":
            step1 = False
            input("Unfortunately even I do not wield the power to reforge affixed cats... not yet, at least!")
            break

    if step1:
        # Check if equal prefixes
        if prefixcount[0] != prefixcount[1]:
            input("Each side must have an equal amount of prefixes, otherwise the synchronization can't happen.")
            return
        else:

            # See if there's enough cats to forge
            if prefixamount == 2:
                neededcount = 2
            else:
                neededcount = 10

            if cat1count < neededcount or cat2count < neededcount:
                input( "It seems we are still lacking cats for the procedure..." )
            else:
                prefixes1 = cat1.strip().split(' ')
                prefixes1 = prefixes1[0:len(prefixes1)-1]

                prefixes2 = cat2.strip().split(' ')
                prefixes2 = prefixes2[0:len(prefixes2)-1]

                forgecat = ' '.join(prefixes1) + ' ' + ' '.join(prefixes2) + ' Kitty'

                # Delete sufficient cats
                inventory[index1][1] -= neededcount
                # If sold all, delete
                if inventory[index1][1] < 1:
                    inventory.pop( index1 )
                    # Fix for pop bug
                    if index1 < index2:
                        index2 -= 1
                inventory[index2][1] -= neededcount
                # If sold all, delete
                if inventory[index2][1] < 1:
                    inventory.pop( index2 )

                d.addcube( forgecat, text=False )
                d.saveinv()

                for _ in range(1,4):
                    input("...")

                input( f"I have forged you the {forgecat}!" )
                firstenter = False