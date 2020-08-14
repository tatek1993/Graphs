from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
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


def add_to_visited(current_room):
    visited[current_room.id] = {}
    for e in current_room.get_exits():
        visited[current_room.id][e] = '?'


def travel_reverse():
    while player.current_room.id != last_unexplored_room[-1][0]:
        print("bc", breadcrumbs)

        crumb = breadcrumbs.pop()
        player.travel(crumb)
        traversal_path.append(crumb)


add_to_visited(player.current_room)

while len(visited) < len(room_graph):
    while len(player.current_room.get_exits()) > 1 or starting == True:
        # find the exits for the current room
        exits = player.current_room.get_exits()
        starting = False

        # figure out the next room the player is moving to
        # exist is a list of directions we can move. The first element is the direction we move in
        direction = exits[0]
        # if theres more than one way we can move
        if len(exits) > 1:
            # we slice off the first element, be cause we will visit that one
            exits = exits[1:]
            for e in exits:
                if visited[player.current_room.id][e] == '?':
                    # we're appending all other possible exits
                    last_unexplored_room.append((player.current_room.id, e))
                    print("lur", last_unexplored_room)

        # move to the room in that direction
        prevroom = player.current_room
        reverse = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

        # travel
        player.travel(direction)
        traversal_path.append(direction)

        # add to visited
        add_to_visited(player.current_room)

        # make the room connections
        visited[prevroom.id][direction] = player.current_room.id
        visited[player.current_room.id][reverse[direction]] = prevroom.id
        breadcrumbs.append(reverse[direction])
        print(visited)

    if len(last_unexplored_room) == 0:
        # we will return traversal_path here, signifying that we are done! :O
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
