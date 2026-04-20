import keyboard, random

#while True:
    #keyboard.wait("up")
    #print("ya")

# 1234 up down left right

arrows = [ "↑", "↓", "←", "→"  ]

chain = ""
for i in range(1,11):
    chain = chain + str( random.randint(1,4) )

print(chain)

errors = 0

for i in chain:
    goodarrow = int(i)-1
    print( arrows[goodarrow] )

    while True:
        if keyboard.is_pressed("up"):
            if goodarrow == 0:
                pass
            else:
                errors += 1
        elif keyboard.is_pressed("down"):
            if goodarrow == 1:
                pass
            else:
                errors += 1
        elif keyboard.is_pressed("left"):
            if goodarrow == 2:
                pass
            else:
                errors += 1
        elif keyboard.is_pressed("right"):
            if goodarrow == 3:
                pass
            else:
                errors += 1

print(errors)