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
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
last_unexplored_room = []
starting = True
breadcrumbs = []


# adds a room to visited
def add_to_visited(current_room):
    if current_room.id not in visited:
        visited[current_room.id] = {}
        for e in current_room.get_exits():
            visited[current_room.id][e] = '?'
    # print('added to visited')


def travel_reverse():
    while player.current_room.id != last_unexplored_room[-1][0]:
        # print("bc", breadcrumbs)

        crumb = breadcrumbs.pop()
        player.travel(crumb)
        print('room id', player.current_room.id)
        traversal_path.append(crumb)
    # print('travel reverse')


def get_unexplored_exits():
    # find the exits for the current room
    exits = player.current_room.get_exits()
    res = [e for e in exits if visited[player.current_room.id][e] == '?']
    print('GUE', res)
    return res


add_to_visited(player.current_room)

while len(visited) < len(room_graph):
    while len(player.current_room.get_exits()) > 1 or starting == True:
        time.sleep(0.2)
        starting = False

        exits = get_unexplored_exits()
        # figure out the next room the player is moving to
        # exist is a list of directions we can move. The first element is the direction we move in
        direction = exits[0]
        # if theres more than one way we can move
        if len(exits) > 1:
            # we slice off the first element, because we will visit that one
            exits = exits[1:]
            for e in exits:
                # we are adding exits with a '?' (exits we did not visit) to last_unexplored_room
                if visited[player.current_room.id][e] == '?':
                    # we're appending all other possible exits
                    last_unexplored_room.append((player.current_room.id, e))
                    # print("lur", last_unexplored_room)

        # move to the room in that direction
        prevroom = player.current_room
        reverse = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

        # travel
        player.travel(direction)
        print('ROOM ID', player.current_room.id)
        traversal_path.append(direction)
        # print('move')

        # add to visited
        add_to_visited(player.current_room)
        # print('add to visited 2')

        # make the room connections
        visited[prevroom.id][direction] = player.current_room.id
        visited[player.current_room.id][reverse[direction]] = prevroom.id
        breadcrumbs.append(reverse[direction])
        # print('make room connections')

    if len(last_unexplored_room) == 0:
        # we will return traversal_path here, signifying that we are done! :O
        pass
        print(len(traversal_path))
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
