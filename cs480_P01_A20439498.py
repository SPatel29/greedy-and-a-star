from msilib.schema import ProgId
import sys
import csv
import numpy as py


class Problem:  # think we need adjacency matrix in this class?

    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
        self.state_space = {} #all possible states environment can be in. Contains driving file data

    def read_file(self, file):
        col_lst = []
        row_lst = []
        my_dict = {}

        with open(file, 'r') as f:
            data = list(csv.reader(f, delimiter=','))
        data = py.array(data)
        data_lst = []
        data_lst = data.tolist()    #a list within a list. Each sublist is a line from file

        col_lst = data_lst[0][1:]
        for element in data_lst[1:]:
            row_lst.append(element[0])

        for element in data_lst[1:]:    #element is a list
            self.state_space[element[0]] = {}   #create nested dictionary
            for i in range(len(element)):   
                if element[i] not in row_lst:
                    self.state_space[element[0]][col_lst[i-1]] = element[i]   #elemtn[0] is the row header for each line. col)lst[i] is the col header from col_list

        
        #TODO:
        #   get data from file
        #   
    def state_space(self, file):  # make the adjacency matrix. set of possible states environment can be in
        # x axis of state space (2D array) will be currenty looking state
        # y axis of state space (2D array) will be destination/next state
        pass

    def transitional_model(self):  # already 'built in' into the adjacency matrix
        pass

    def action_cost_function(self, state_a, state_b):  # function that reads you cost of going from state_a to state_b
        # action cost function is a mechanism  of reading the cost (weight) corresponding to two
        # states x and y (think row and column) from the corresponding cell in the adjcanecy matrix
        # i.e,
        # state[x][y] = cost
        # recall state space tree is a 2D array
        pass

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
        problem.read_file("greedy-and-a-star/driving(1).csv")
        # problem = Problem(initial_state, goal_state)
    else:
        raise Exception('ERROR: Not enough or too many arguments')


if __name__ == '__main__':
    main()
