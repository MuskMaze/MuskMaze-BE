from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import random




class Room(models.Model):
    #We have to create a room id
    # id_room= models.IntegerField(default=0)
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    # move_x = models.IntegerField(default=None)
    # move_y = models.IntegerField(default=None)
    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()


CHARACTER_TILES = {'wall': '.',
                   'floor': '1'}
 
 
# class World:
#     def __init__(self, width=25, height=25, max_rooms=100, min_room_xy=5,
#                  max_room_xy=5, rooms_overlap=False, random_connections=3,
#                  random_spurs=3, tiles=CHARACTER_TILES):
#         self.width = width
#         self.height = height
#         self.max_rooms = max_rooms
#         self.min_room_xy = min_room_xy
#         self.max_room_xy = max_room_xy
#         self.rooms_overlap = rooms_overlap
#         self.random_connections = random_connections
#         self.tiles = CHARACTER_TILES
#         self.level = []
#         self.room_list = []
#         self.corridor_list = []
#         self.tiles_level = []
 
#     def gen_room(self):
#         x, y, w, h = 0, 0, 0, 0
 
#         w = random.randint(self.min_room_xy, self.max_room_xy)
#         h = random.randint(self.min_room_xy, self.max_room_xy)
#         x = random.randint(1, (self.width - w - 1))
#         y = random.randint(1, (self.height - h - 1))
 
#         return [x, y, w, h]
 
#     def room_overlapping(self, room, room_list):
#         x = room[0]
#         y = room[1]
#         w = room[2]
#         h = room[3]
 
#         for current_room in room_list:
#             if (x < (current_room[0] + current_room[2]) and
#                 current_room[0] < (x + w) and
#                 y < (current_room[1] + current_room[3]) and
#                 current_room[1] < (y + h)):
#                 return True
#         return False
 
 
#     def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):
#         if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
#             return [(x1, y1), (x2, y2)]
#         else:
#             join = None
#             if join_type is 'either' and set([0, 1]).intersection(
#                  set([x1, x2, y1, y2])):
#                 join = 'bottom'
#             elif join_type is 'either' and set([self.width - 1,
#                  self.width - 2]).intersection(set([x1, x2])) or set(
#                  [self.height - 1, self.height - 2]).intersection(
#                  set([y1, y2])):
#                 join = 'top'
#             elif join_type is 'either':
#                 join = random.choice(['top', 'bottom'])
#             else:
#                 join = join_type
#             if join is 'top':
#                 return [(x1, y1), (x1, y2), (x2, y2)]
#             elif join is 'bottom':
#                 return [(x1, y1), (x2, y1), (x2, y2)]
 
#     def join_rooms(self, room_1, room_2, join_type='either'):
#         # sort by the value of x
#         sorted_room = [room_1, room_2]
#         sorted_room.sort(key=lambda x_y: x_y[0])
 
#         x1 = sorted_room[0][0]
#         y1 = sorted_room[0][1]
#         w1 = sorted_room[0][2]
#         h1 = sorted_room[0][3]
#         x1_2 = x1 + w1 - 1
#         y1_2 = y1 + h1 - 1
 
#         x2 = sorted_room[1][0]
#         y2 = sorted_room[1][1]
#         w2 = sorted_room[1][2]
#         h2 = sorted_room[1][3]
#         x2_2 = x2 + w2 - 1
#         y2_2 = y2 + h2 - 1
 
#         # overlapping on x
#         if x1 < (x2 + w2) and x2 < (x1 + w1):
#             jx1 = random.randint(x2, x1_2)
#             jx2 = jx1
#             tmp_y = [y1, y2, y1_2, y2_2]
#             tmp_y.sort()
#             jy1 = tmp_y[1] + 1
#             jy2 = tmp_y[2] - 1
 
#             corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
#             self.corridor_list.append(corridors)
 
#         # overlapping on y
#         elif y1 < (y2 + h2) and y2 < (y1 + h1):
#             if y2 > y1:
#                 jy1 = random.randint(y2, y1_2)
#                 jy2 = jy1
#             else:
#                 jy1 = random.randint(y1, y2_2)
#                 jy2 = jy1
#             tmp_x = [x1, x2, x1_2, x2_2]
#             tmp_x.sort()
#             jx1 = tmp_x[1] + 1
#             jx2 = tmp_x[2] - 1
 
#             corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
#             self.corridor_list.append(corridors)
 
#         # no overlap
#         else:
#             join = None
#             if join_type is 'either':
#                 join = random.choice(['top', 'bottom'])
#             else:
#                 join = join_type
 
#             if join is 'top':
#                 if y2 > y1:
#                     jx1 = x1_2 + 1
#                     jy1 = random.randint(y1, y1_2)
#                     jx2 = random.randint(x2, x2_2)
#                     jy2 = y2 - 1
#                     corridors = self.corridor_between_points(
#                         jx1, jy1, jx2, jy2, 'bottom')
#                     self.corridor_list.append(corridors)
#                 else:
#                     jx1 = random.randint(x1, x1_2)
#                     jy1 = y1 - 1
#                     jx2 = x2 - 1
#                     jy2 = random.randint(y2, y2_2)
#                     corridors = self.corridor_between_points(
#                         jx1, jy1, jx2, jy2, 'top')
#                     self.corridor_list.append(corridors)
 
#             elif join is 'bottom':
#                 if y2 > y1:
#                     jx1 = random.randint(x1, x1_2)
#                     jy1 = y1_2 + 1
#                     jx2 = x2 - 1
#                     jy2 = random.randint(y2, y2_2)
#                     corridors = self.corridor_between_points(
#                         jx1, jy1, jx2, jy2, 'top')
#                     self.corridor_list.append(corridors)
#                 else:
#                     jx1 = x1_2 + 1
#                     jy1 = random.randint(y1, y1_2)
#                     jx2 = random.randint(x2, x2_2)
#                     jy2 = y2_2 + 1
#                     corridors = self.corridor_between_points(
#                         jx1, jy1, jx2, jy2, 'bottom')
#                     self.corridor_list.append(corridors)
 
 
#     def gen_level(self):
 
#         # build an empty dungeon, blank the room and corridor lists
#         for i in range(self.height):
#             self.level.append(['wall'] * self.width)
#         self.room_list = []
#         self.corridor_list = []
 
#         max_iters = self.max_rooms * 5
 
#         for a in range(max_iters):
#             tmp_room = self.gen_room()
 
#             if self.rooms_overlap or not self.room_list:
#                 self.room_list.append(tmp_room)
#             else:
#                 tmp_room = self.gen_room()
#                 tmp_room_list = self.room_list[:]
 
#                 if self.room_overlapping(tmp_room, tmp_room_list) is False:
#                     self.room_list.append(tmp_room)
 
#             if len(self.room_list) >= self.max_rooms:
#                 break
 
#         # connect the rooms
#         for a in range(len(self.room_list) - 1):
#             self.join_rooms(self.room_list[a], self.room_list[a + 1])
 
#         # do the random joins
#         for a in range(self.random_connections):
#             room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
#             room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
#             self.join_rooms(room_1, room_2)
#         # fill the map
#         # paint rooms
#         for room_num, room in enumerate(self.room_list):
#             for b in range(room[2]):
#                 for c in range(room[3]):
#                     self.level[room[1] + c][room[0] + b] = 'floor'
#         # paint corridors
#         for corridor in self.corridor_list:
#             x1, y1 = corridor[0]
#             x2, y2 = corridor[1]
#             for width in range(abs(x1 - x2) + 1):
#                 for height in range(abs(y1 - y2) + 1):
#                     self.level[min(y1, y2) + height][
#                         min(x1, x2) + width] = 'floor'
 
#             if len(corridor) == 3:
#                 x3, y3 = corridor[2]
 
#                 for width in range(abs(x2 - x3) + 1):
#                     for height in range(abs(y2 - y3) + 1):
#                         self.level[min(y2, y3) + height][
#                             min(x2, x3) + width] = 'floor'

#     def gen_tiles_level(self):
#         count = 0
#         for row_num, row in enumerate(self.level):
#             tmp_tiles = []
#             for col_num, col in enumerate(row):
#                 if col == 'wall':
#                     tmp_tiles.append(self.tiles['wall'])
#                 if col == 'floor':
#                     tmp_tiles.append(self.tiles['floor'])
#                     count += 1
 
#             self.tiles_level.append(''.join(tmp_tiles))
#         return(self.tiles_level)





