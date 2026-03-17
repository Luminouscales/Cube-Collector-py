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
import scripts.inventory as inv

inventory = d.inventory

def forge():
    print("FIXME forge text")
    inptable = input("input index index")
    inptable = inptable.strip().split('\t')

    command = inptable[0]
    match command:
        case "exit" | "e": return
        case "forge": forge_forge(inptable[1], inptable[2])


def forge_forge(index1, index2):
    index1 = int(index1)
    index2 = int(index2)

    cat1 = inventory[index1][0]
    cat2 = inventory[index2][0]

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
            prefixes1 = cat1.strip().split(' ')
            prefixes1 = prefixes1[0:len(prefixes1)-1]

            prefixes2 = cat2.strip().split(' ')
            prefixes2 = prefixes2[0:len(prefixes2)-1]

            forgecat = ' '.join(prefixes1) + ' ' + ' '.join(prefixes2) + ' Kitty'
            input( forgecat )

forge()