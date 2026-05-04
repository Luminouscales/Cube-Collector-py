def doprefixstats( prefixes, statstable ):
    match prefixes:
        case "Big":
            statstable[0] += 20
            statstable[1] += 5
            statstable[3] -= 2
        case "Small":
            statstable[0] -= 20
            statstable[1] -= 5
            statstable[3] += 2
        case "Fast" | "Quick":
            statstable[3] += 1
        case "Dynamic":
            statstable[3] += 2
        case "Shapeless" | "Intemporal" | "Abstract":
            statstable[3] += 3
        case "Slow":
            statstable[3] -= 3
        case "Happy" | "Merry":
            statstable[0] += 10
            statstable[3] += 2
        case "Sad":
            statstable[0] -= 5
            statstable[3] -= 1
        case "Bright":
            statstable[4] += 5
        case "Loud" | "Noisy":
            statstable[1] += 5
            statstable[4] -= 5
        case "Quiet":
            statstable[1] -= 5
            statstable[4] += 5
        case "Tall":
            statstable[1] += 5
        case "Short":
            statstable[3] += 1
        case "Thin" | "Light":
            statstable[2] -= 2
            statstable[3] += 1
        case "Thick" | "Heavy":
            statstable[2] += 5
            statstable[3] -= 2
        case "Hard":
            statstable[2] += 5
        case "Soft":
            statstable[2] -= 5
        case "Strong":
            statstable[1] += 10
        case "Weak":
            statstable[1] -= 10
        case "Sharp":
            statstable[4] += 10
            statstable[1] += 5
        case "World-Ending":
            statstable[0] += 50
            statstable[1] += 20
            statstable[2] += 10
            statstable[3] += 3
            statstable[4] -= 25
        case "Dull":
            statstable[4] -= 10
        case "New" | "Healthy" | "True" | "Expensive" | "Right" | "Optimized" | "Efficient":
            statstable[0] += 10
            statstable[4] += 2
            statstable[1] += 2
            statstable[2] += 2
            statstable[3] += 1
        case "Old" | "Sick" | "False" | "Cheap" | "Wrong" | "Shitty" | "Useless" | "Pathetic":
            statstable[0] -= 10
            statstable[4] -= 2
            statstable[1] -= 2
            statstable[2] -= 2
            statstable[3] -= 1
        case "Wise" | "Calm":
            statstable[4] += 15
        case "Foolish":
            statstable[4] -= 5
        case "Brave":
            statstable[3] += 2
            statstable[1] += 5
            statstable[2] += 5
            statstable[0] += 10
        case "Cowardly":
            statstable[3] -= 1
            statstable[2] -= 5
        case "Brilliant":
            statstable[0] += 20
            statstable[4] += 4
            statstable[1] += 4
            statstable[2] += 4
            statstable[3] += 1
        case "Supreme":
            statstable[0] += 25
            statstable[4] += 6
            statstable[1] += 6
            statstable[2] += 6
            statstable[3] += 2
        case "Unreal" | "Ascended" | "Godly":
            statstable[0] += 30
            statstable[4] += 8
            statstable[1] += 8
            statstable[2] += 8
            statstable[3] += 3
        case "Dumb" | "Stupid":
            statstable[4] -= 10
        case "Kind":
            statstable[1] -= 2
            statstable[0] += 5
        case "Cruel" | "Evil":
            statstable[1] += 5
        case "Polite":
            statstable[1] -= 2
        case "Rude" | "Scary" | "Angry":
            statstable[3] += 1
            statstable[1] += 2
        case "Boring":
            statstable[3] -= 5
        case "Safe":
            statstable[0] += 10
            statstable[2] += 5
        case "Dangerous":
            statstable[1] += 10
            statstable[3] += 2
        case "Hungry":
            statstable[1] -= 2
            statstable[2] -= 2
        case "Full":
            statstable[3] -= 1
            statstable[2] += 5
        case "Profaned":
            statstable[0] += 10
            statstable[1] += 10
            statstable[2] -= 10
            statstable[3] += 2
            statstable[4] -= 15
        case "Auric" | "Draconic":
            statstable[0] += 20
            statstable[1] += 10
            statstable[2] += 10
            statstable[3] -= 4
            statstable[4] -= 20
        case "Calamitous":
            statstable[1] += 30
            statstable[2] -= 15
            statstable[4] -= 25
        case "Cobalt":
            statstable[0] += 5
            statstable[1] += 2
            statstable[2] += 2
            statstable[3] += 1
            statstable[4] += 2
        case "Mythril":
            statstable[0] += 10
            statstable[1] += 3
            statstable[2] += 3
            statstable[3] += 2
            statstable[4] += 3
        case "Titanium":
            statstable[0] += 15
            statstable[1] += 5
            statstable[2] += 5
            statstable[3] += 3
            statstable[4] += 5
        case "Iron" | "Galvanized":
            statstable[0] += 3
            statstable[1] += 1
            statstable[2] += 1
            statstable[3] += 1
            statstable[4] += 1
        case "Plastic":
            statstable[0] -= 3
            statstable[1] -= 1
            statstable[2] -= 1
            statstable[3] -= 1
            statstable[4] -= 1
        case "Shattered":
            statstable[2] -= 10
        case "Rusty":
            statstable[2] -= 5
            statstable[1] -= 5
        case "Feline" | "Kitty" | "Clever":
            statstable[4] += 5
            statstable[3] += 2
        case "Perseverant":
            statstable[0] += 20
            statstable[2] += 10


allskills = [ 
    "Swipe", # 50% more damage
    "Scratch", # Attack twice
    "Pounce", # Guaranteed hit
    "Tear", # Ignores 20 def
    "Flicker", # -+50% damage
    "Lick", #heal 10% hp
    "Hiss", #give attack to self

]