from room import Room
from player import Player
from world import World
import time

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
last_unexplored_room = []

breadcrumbs = []


# adds a room to visited
def add_to_visited(current_room):
    # add the current room id to visited if it is not there already
    if current_room.id not in visited:
        visited[current_room.id] = {}
        # for each exit in the current room, use the exit direction as the key, and set the value of each to '?'
        for e in current_room.get_exits():
            visited[current_room.id][e] = '?'


# use this fn to return to the last place that has unexplored exits
def travel_reverse():
    # while the current room id is not the most recent element appended to l_u_r
    while player.current_room.id != last_unexplored_room[-1]:
        # remove and return the last element of breadcrumbs
        crumb = breadcrumbs.pop()
        # use that crumb (which is a direction) to move the player
        player.travel(crumb)
        # add that direction to our traversal_path
        traversal_path.append(crumb)

    # we remove the room from l_u_r each time we back track
    last_unexplored_room.pop()


def get_unexplored_exits():
    # find the exits for the current room
    exits = player.current_room.get_exits()
    # remove all exits that have already been visited
    # filter the exit list to only include exits with a value of '?'
    return [e for e in exits if visited[player.current_room.id][e] == '?']


add_to_visited(player.current_room)

# while the length of visited < the # of rooms in room_graph i.e. we have not visited all rooms
while len(visited) < len(room_graph):

    # while there are still unexplored exits in the current room
    while len(get_unexplored_exits()) > 0:

        exits = get_unexplored_exits()
        # figure out the next room the player is moving to
        # exits is a list of directions we can move. The first element is the direction we move in
        direction = exits[0]

        # if theres more than one way we can move, we must remember this room because we must return here to explore other exits
        if len(exits) > 1:
            # only add a room to l_u_r if it is not already there
            if player.current_room.id not in last_unexplored_room:
                # we're appending all rooms with unexplored exits
                last_unexplored_room.append(player.current_room.id)

        # remember the last room we were in to establish connection later
        prevroom = player.current_room
        reverse = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

        # travel
        player.travel(direction)

        traversal_path.append(direction)

        # add to visited
        add_to_visited(player.current_room)

        # make the room connections
        # in the previous room, moving in the direction we were given takes us to our current room
        visited[prevroom.id][direction] = player.current_room.id
        # in our current room, moving in the opposite direction will take us to the previous room
        visited[player.current_room.id][reverse[direction]] = prevroom.id

        # leave a trail of breadcrumbs to backtrack later. These are the directions on how to get back to where we started
        breadcrumbs.append(reverse[direction])

    if len(last_unexplored_room) == 0:
        # we are done! :O
        pass
    else:
        travel_reverse()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
