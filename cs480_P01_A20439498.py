from msilib.schema import ProgId
from queue import Queue
from sre_parse import State
import sys
import csv
from webbrowser import get
import numpy as py
from queue import PriorityQueue


class Problem:  # think we need adjacency matrix in this class?

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

class Node:

    def __init__(self, state, parent=None, action_taken=None, path_cost=0):
        # state = the state to which the node belongs
        # parent = node in the tree that GENERATED this node. I.e should be a REFERENCE to parent node
        # action = the action that was applied to the PARENTS state to generate this node. I.e applied stateTo to stateFrom
        # path_cost = TOTAL COST of the path from the initial node to this node. I.e path cost from iniitial node to this node being generated
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.path_cost = path_cost


def best_first_search(problem, f):
    # TODO:
    # Create Node class
    # Create Prio Queue
    #   queue is ordered by f with a node object as an element. F is our eval function

    node = Node(problem.initial)
    frontier = PriorityQueue()
    reached = {}
    if f == "greedy":
        # the priority queue is a tuple of (straight_line_distance, node).
        # priority queue is ordered (arranged) by straight_line_distance. Least distance is front.
        frontier.put(
            (problem.straight_line_state_space[problem.initial][problem.goal], node))
        reached[problem.initial] = node
        while not frontier.empty():
            node = frontier.get()
            if problem.is_goal(node[1].state):
                return node
            

        

    else:  # A*
        # the above is a tuple of (straight_line_distance, node).
        # priority queue is ordered (arranged) by node path cost + straight_line_distance. 
        # Least number is front
        frontier.put(
            (problem.straight_line_state_space[problem.initial][problem.goal] + node.path_cost, node))
        reached[problem.initial] = node
        while not frontier.empty():
            pass
        
            
        
        

    return False


def main():
    if len(sys.argv) == 3:
        initial_state = ("AL")
        goal_state = ("IL")
        problem = Problem(initial_state, goal_state)
        problem.generate_state_space(
            "greedy-and-a-star/driving(1).csv", "greedy-and-a-star/straightline(1).csv")
        # problem = Problem(initial_state, goal_state)
        best_first_search(problem, "greedy")
        #lst = problem.actions("WY")
        #problem.get_line_distance("WY", lst)
    else:
        raise Exception('ERROR: Not enough or too many arguments')


if __name__ == '__main__':
    main()
