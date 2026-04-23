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

inventory = d.inventory

def forge():
    while True:
        f.clear()
        print("FIXME forge text")
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
            input("invalid, up to two prefixes")
            break
        prefixcount.append( prefixamount )
        if cattable[prefixamount] != "Kitty":
            step1 = False
            input("invalid, must be unaffixed kitty")
            break

    if step1:
        # Check if equal prefixes
        if prefixcount[0] != prefixcount[1]:
            input("invalid, must have equal affixes")
            return
        else:

            # See if there's enough cats to forge
            if prefixamount == 2:
                neededcount = 2
            else:
                neededcount = 10

            if cat1count < neededcount or cat2count < neededcount:
                input( "FIXME wrong cat amount" )
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

                input( f"I have forged you the {forgecat}!" )