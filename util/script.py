from util.map import World
from django.contrib.auth.models import User
from adventure.models import Player, Room
import random
Room.objects.all().delete()
Player.objects.all().delete()
(138, {'adventure.Room': 138})
CHARACTER_TILES = {'wall': '0',
                   'floor': '1'}
ancho = 20
alto = 15
gen = World(width=ancho, height=alto, max_rooms=15)
gen.gen_level()
a = gen.gen_tiles_level()

count=1
r=[None]*len(a[1])
for n in a[1]:
    r[count-1] = Room(id=count,move_x=n[0],move_y=n[1])
    r[count-1].save()
    count+=1
print(r)
for element in a[1]:
    east = (element[0] , element[1]+1)
    west = (element[0] , element[1]-1)
    north = (element[0]-1 , element[1])
    south = (element[0]+1, element[1])
   
    if east in a[1]:
        r[a[1].index(element)].connectRooms(r[a[1].index(east)],"e")
        
    if west in a[1]:
        r[a[1].index(element)].connectRooms(r[a[1].index(west)],"w")
        
    if north in a[1]:
        r[a[1].index(element)].connectRooms(r[a[1].index(north)],"n")
        
    if south in a[1]:
        r[a[1].index(element)].connectRooms(r[a[1].index(south)],"s")
        

players = Player.objects.all()
for p in players:
    p.currentRoom=r[random.randint(0,len(a[1]))].id
    p.save()

