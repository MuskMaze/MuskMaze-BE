

from django.contrib.auth.models import User
from adventure.models import Player, Room

Room.objects.all().delete()

# let's create the rooms
r_outside = Room(title="Outside the Sci-Fi Headquarter of SpaceX",
                description="East of you, SpaceX entrance is laid with prototypes of Merlin Engine")
r_lobby = Room(title="Lobby",
                description="The lobby is brightly lit with red and white lights lining the walls")
# r_overlook = Room(title="The Dome",
#                 description="The Dome is the shape of an oval cut in half, with glass ceiling look at the galaxy above and beyond")
r_ornament = Room(title="Hangings",
                description="With the dome hangs a booster stage of first Falcon 9 Rocket")
r_center = Room(title="Focus",
                description="There, in the middle of it all, lies a Dragon Capsule that took astronauts to ISS for the first time")
r_treasure = Room(title="Unknown",
                description = "We do not know the location of this room and will find it in objects but, this is where Elon will build Improbability Drive")


r_outside.save()
r_lobby.save()
# r_overlook.save()
r_ornament.save()
r_center.save()
r_treasure.save()

r_outside.connectRooms(r_lobby, "n")
r_lobby.connectRooms(r_outside, "s")

r_lobby.connectRooms(r_ornament, "n")
r_ornament.connectRooms(r_lobby, "s")

r_ornament.connectRooms(r_center, "w")
r_center.connectRooms(r_ornament, "e")

r_center.connectRooms(r_treasure, "w")
r_treasure.connectRooms(r_center, "e")


players = Player.objects.all()
for p in players:
    p.currentRoom=r_outside.id
    p.save() 
