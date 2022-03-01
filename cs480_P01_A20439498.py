import sys
import csv
import numpy
import time
from queue import PriorityQueue


class Problem:  

    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
        # all possible states environment can be in. Contains driving file data
        self.driving_state_space = {}
        self.straight_line_state_space = {}

    def generate_state_space(self, driving_file, straight_line_file):
        col_lst = []
        row_lst = []
        with open(driving_file, 'r') as f:
            # a list within a list. Each sublist is a line from file
            driving_data = list(csv.reader(f, delimiter=','))

        col_lst = driving_data[0][1:]
        for element in driving_data[1:]:
            row_lst.append(element[0])

        for element in driving_data[1:]:  # element is a list
            # create nested dictionary
            self.driving_state_space[element[0]] = {}
            for i in range(len(element)):
                # if not row header (i.e is a driving distance)
                if element[i] not in row_lst:
                    self.driving_state_space[element[0]
                                             ][col_lst[i-1]] = int(element[i])
                    # element[0] is the row header for each line. col)lst[i] is the col header from col_list
                    # subtract by one because we do not want we are skipping over first index of element since it
                    # does not contain a data value. the first index contains the row header, not numeber distance

        # Below is the straight line
        with open(straight_line_file, 'r') as f:
            # a list within a list. Each sublist is a line from file
            line_data = list(csv.reader(f, delimiter=','))

        for element in line_data[1:]:  # element is a list
            # create nested dictionary
            self.straight_line_state_space[element[0]] = {}
            for i in range(len(element)):
                # if not row header (i.e is a straight line distance)
                if element[i] not in row_lst:
                    self.straight_line_state_space[element[0]
                                                   ][col_lst[i-1]] = int(element[i])

    def get_cost(self, state_from, state_to):
        return self.straight_line_state_space[state_from][state_to]

    # returns a list of all possible states it can traverse.
    def actions(self, state):
        temp_lst = []
        for key, value in self.driving_state_space[state].items():
            if value >= 0:
                temp_lst.append(key)
        return temp_lst

    # lst is all possible states it can traverse. state is current node
    def get_line_distance(self, state):
        possible_actions = self.actions(state)
        temp_lst = []
        for element in possible_actions:
            temp_lst.append(self.straight_line_state_space[state][element])
        return temp_lst

    def get_initial_state(self):
        return self.initial

    def get_goal_state(self):
        return self.goal

    def is_goal(self, state):
        return state == self.goal


class Node:     # is also a linked list

    def __init__(self, state, parent=None, action_taken=None, path_cost=0):
        # state = the state to which the node belongs
        # parent = node in the tree that GENERATED this node. I.e should be a REFERENCE to parent node
        # action = the action that was applied to the PARENTS state to generate this node. I.e applied stateTo to stateFrom
        # path_cost = TOTAL COST of the path from the initial node to this node. I.e path cost from iniitial node to this node being generated
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.path_cost = path_cost

        # Going backward from the solution node and using PARENT pointers (self.parent) can recreate
        # the entier path from the initial node to the solution  node
        # this would be a linked list datastructure holding the path.
        # I.e self.parent can be considered as a linked list data structure

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def expand(problem, node):  # node is parent node. Is a tuple consiting of parent total cost and parent node object
    s = node[1].state
    # action is a list of state names it can traverse to
    for state_to in problem.actions(s):
        # cost to traverse that node alone
        node_cost = problem.driving_state_space[s][state_to]
        path_cost = node[1].path_cost + node_cost
        yield Node(state_to, node, node_cost, path_cost)


def best_first_search(problem, f):
    node = Node(problem.initial)
    frontier = PriorityQueue()
    reached = {}
    if f == "greedy":
        # add to prio queue as tuple of (straight line distance, node)
        frontier.put(
            (problem.straight_line_state_space[problem.initial][problem.goal], node))   
    else:
        # add to prio queue as tuple of (total path cost + straight line distance, node)
        frontier.put(
            (problem.straight_line_state_space[problem.initial][problem.goal] + node.path_cost, node))
    reached[problem.initial] = node
    while not frontier.empty():
        node = frontier.get()
        if problem.is_goal(node[1].state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child    # add or update existing node
                if f == "greedy":
                    frontier.put((problem.straight_line_state_space[s][problem.goal], child))
                else:
                    frontier.put(
                        (problem.straight_line_state_space[s][problem.goal] + child.path_cost, child))
    return False

def print_menu(inital_state, goal_state):
    print("Patel, Sunny, A20439498 solution: ")
    print("Initial State: ", inital_state)
    print("Goal State: ", goal_state, '\n\n')

def main():
    with open("driving(1).csv", 'r') as f:
            # a list within a list. Each sublist is a line from file
            driving_data = list(csv.reader(f, delimiter=','))

    col_lst = driving_data[0][1:]

    if len(sys.argv) == 3:
        initial_state = sys.argv[1]
        goal_state = sys.argv[2]
        if initial_state in col_lst and goal_state in col_lst:
            start = time.time()
            greedy_search = Problem(initial_state, goal_state)
            greedy_search.generate_state_space(
                "driving(1).csv", "straightline(1).csv")
            greedy_sol_node = best_first_search(greedy_search, "greedy")
            a_star_search = Problem(initial_state, goal_state)
            a_star_search.generate_state_space(
                "driving(1).csv", "straightline(1).csv")
            a_star_sol_node = best_first_search(a_star_search, "a*")
            print_menu(initial_state, goal_state)
            if greedy_sol_node:
                end = time.time()
                lst = []
                print("Greedy Best First Search: ")
                total_cost_path = greedy_sol_node[1].path_cost           
                while greedy_sol_node[1].parent:
                    lst.append(greedy_sol_node[1].state)
                    greedy_sol_node = greedy_sol_node[1].parent
                lst.append(greedy_sol_node[1].state)    # add inital state
                print("Solution path: ", lst[::-1]) #[::-1] needed to reverse it
                print("Number of states on path: ", len(lst))
                print("Path Cost: ", total_cost_path)
                print("Execution time: ", end - start, '\n')
                
            if a_star_sol_node:
                end = time.time()
                lst = []
                print("A* Search: ")
                total_cost_path = a_star_sol_node[1].path_cost
                while a_star_sol_node[1].parent:
                    lst.append(a_star_sol_node[1].state)
                    a_star_sol_node = a_star_sol_node[1].parent
                lst.append(a_star_sol_node[1].state)
                print("Solution path: ", lst[::-1])
                print("Number of states on path: ", len(lst))
                print("Path Cost: ", total_cost_path)
                print("Execution time: ", end - start, '\n')
            if not a_star_sol_node or not greedy_sol_node:      #if a star or greedy returns a false from search
                end = time.time()
                print("FAILURE: NO PATH FOUND")
                print("Number of states on path: 0")
                print("Path Cost: 0")
                print("Execution time: ", end - start, '\n')
        else:
            print("Please enter correct state names for your initial and goal states")
    else:
        raise Exception('ERROR: Not enough or too many arguments')


if __name__ == '__main__':
    main()
