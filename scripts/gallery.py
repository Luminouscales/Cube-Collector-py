# Display fav cats or items

import scripts.data as d
import scripts.inventory as inv

gallerypath = d.savepath + "gallery.txt"

gallery = []
with open( gallerypath, 'r' ) as file:
    for line in file:
        row = line.strip().split('\n')
        gallery.append( row[0] )

def inp_gallery():

    print( "\n_                ___       _.--.")
    print("\`.|\..----...-'`   `-._.-'_.-'`")
    print("/  ' `         ,       __.--'")
    print(")/' _/     \   `-_,   /")
    print('`-"" `"\_  ,_.-;_.-\_ ",')
    print("    _.-'_./   {_.'   ; /")
    print("   {_.-``-'         {_/")

    print("\nKITTY GALLERY OF BEST, PRETTIEST CATS:")
    if len(gallery) > 0:
        for cat in gallery:
            print( "|| " + cat )
        print( "FIXME gallery text" )
    else:
        print( "FIXME gallery: no cats" )

    galleryinput = input("")
    match galleryinput:
        case "submit": gallery_submit()
        case "pull": gallery_pull()
        case "exit" | "e": return

def gallery_save():
    with open( gallerypath, 'w' ) as file:
        for cat in gallery:
            file.write( cat + '\n' )


def gallery_submit():
    index = int( input("index") )
    gallery.append( d.inventory[index][0] )
    inv.case_delete( index, 1, False )

    gallery_save()

    inp_gallery()

def gallery_pull():
    index = int( input("index") )
    d.addcube( gallery[index - 1], 1, False, False )
    gallery.pop( index - 1 )

    gallery_save()

    inp_gallery()