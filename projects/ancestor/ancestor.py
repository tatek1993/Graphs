# we are going to use dft, because we want to move vertically and not width wise
class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


def earliest_ancestor(ancestors, starting_node):
    # create a graph
    graph = {}
    e_a_path = []
    # print(starting_node)
    # create a loop
    for parent, child in ancestors:
        ### we want children to have a list of parents
        ### maybe make each child an array to make key value pairs?
        if child not in graph:
            graph[child] = []
        ### where key is child, and value is parent???
        graph[child].append(parent)

    # create visited set
    visited = set()

    # create a stack and append the starting node
    s = Stack()
    s.push([starting_node])

    # while stack is not empty
    while s.size() > 0:
        ### pop
        # change node to path
        path = s.pop()
        print(path)
        # our vertex in that path
        v = path[-1]
        # if not in visited
        if v not in visited:
            ### add to visited
            visited.add(v)

            # if the path is longer than the eapath, or length is the same and the value is smaller
            if len(path) > len(e_a_path) or (len(path) == len(e_a_path)
                                             and path[-1] < e_a_path[-1]):
                e_a_path = path
                print("newrecord", e_a_path)

            if v in graph:
                print('parents of ', v, ':', graph[v])
                for parent in graph[v]:

                    # make a copy of the path
                    path_copy = list(path)
                    # append parent
                    path_copy.append(parent)
                    # push path_copy
                    s.push(path_copy)

    if len(e_a_path) != 1:
        return e_a_path[len(e_a_path) - 1]
    else:
        return -1
    # max path len = 1
    # earliest ancestor = -1 right before while loop

    # append smallest value to stack??? That would be the eldest ancestor
    # s.append(graph[node][0])???
