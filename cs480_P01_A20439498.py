from msilib.schema import ProgId
import sys
import csv
import numpy as py


class Problem:  # think we need adjacency matrix in this class?

    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
        # all possible states environment can be in. Contains driving file data
        self.state_space = {}

    def generate_state_space(self, file):
        col_lst = []
        row_lst = []
        data_lst = []

        with open(file, 'r') as f:
            data = list(csv.reader(f, delimiter=','))
        data = py.array(data)
        data_lst = data.tolist()  # a list within a list. Each sublist is a line from file

        col_lst = data_lst[0][1:]
        for element in data_lst[1:]:
            row_lst.append(element[0])

        for element in data_lst[1:]:  # element is a list
            self.state_space[element[0]] = {}  # create nested dictionary
            for i in range(len(element)):
                # if not row header (i.e is a driving distance)
                if element[i] not in row_lst:
                    self.state_space[element[0]
                                     ][col_lst[i-1]] = int(element[i])
                    # element[0] is the row header for each line. col)lst[i] is the col header from col_list
                    # subtract by one because we do not want we are skipping over first index of element since it
                    # does not contain a data value. the first index contains the row header, not numeber distance
        print(self.state_space["WA"]["ID"])
    def get_cost(self, state_from, state_to):
        return self.state_space[state_from][state_to]

    # returns a list of all possible states it can traverse.
    def actions(self, state):
        temp_lst = []
        for key, value in self.state_space[state].items():
            if value > 0:
                temp_lst.append(key)
        return temp_lst

    def get_initial_state(self):
        return self.initial

    def get_goal_state(self):
        return self.goal


class Node:

    def __init__(self, state):
        self.state = state


def main():
    if len(sys.argv) == 3:
        initial_state = (sys.argv[1])
        goal_state = (sys.argv[2])
        problem = Problem(initial_state, goal_state)
        problem.generate_state_space("greedy-and-a-star/driving(1).csv")
        # problem = Problem(initial_state, goal_state)
    else:
        raise Exception('ERROR: Not enough or too many arguments')


if __name__ == '__main__':
    main()
