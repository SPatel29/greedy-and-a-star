import sys


class Problem:  # think we need adjacency matrix in this class?


    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
        self.actions = []  # set of actions for each state in the state space

    @staticmethod
    def read_file(file):
        lines = []
        with open(file, 'r') as f:

            lines.append(f.readline())


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
        #problem = Problem(initial_state, goal_state)
    else:
        raise Exception('ERROR: Not enough or too many arguments')


if __name__ == '__main__':
    main()