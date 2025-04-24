from collections import deque
import sys

# we use this to represent the state of the vacuum world
class WorldState:
    def __init__(self, world, column, row, solution):
        self.world = world
        self.column = column
        self.row = row
        self.solution = solution

# generateVariables takes in a list of lists and returns starting position, size of world
def generateVariables(world, rows, columns):
    startRow = None
    startColumn = None
    # we're brute forcing to find the vacuum by checking every possible spot
    for row in range(rows):
        for column in range(columns):
            if world[row][column] == '@':
                startRow = row
                startColumn = column
                break
    return startColumn, startRow, columns, rows

# Function to check if a move is valid, takes in a potential move and the limit of the world.
def isValid(x, y, worldx, worldy):
    # if the potential move is bigger than the world or less than zero, illegal
    return 0 <= x < worldx and 0 <= y < worldy

# Function to print the board, takes in a worldstate
# !!!!!!!!! DELETE LATER PLEASE SEE THIS !!!!!!!!!!!!!!!!!!!!!!!!!!
def printWorld(world: WorldState):
    for row in world.world:
        print(' '.join(map(str, row)))
    print("--------")

# function to check if the solution has been reached so we can terminate, takes in a list of lists
def isSolution(world):
    for inner_list in world:
        for item in inner_list:
            # Found a '*', so return False immediately
            if item == '*':
                return False
    # If the loops complete without finding '*', return True aka, solution found
    return True

# function to do the actual DFS, takes in a world state and the size of the world
def DFS(world: WorldState, columnLimit, rowLimit):
    # All possible moves in order of Left, Right, Down, Up
    rowMoves = [0, 0, 1, -1]
    columnMoves = [-1, 1, 0, 0]
    directionNames = ["W", "E", "S", "N"]
    numberExpanded = 0
    numberGenerated = 0

    stack = []
    visited = set()
    stack.append(world)

    while stack:
        curr = stack.pop()
        numberExpanded = numberExpanded + 1
        printWorld(curr)

        if isSolution(curr.world):
            return curr.solution, numberGenerated, numberExpanded

        # this for loop goes through 0-3 which is all valid directions, checks if direction is legal,
        # then it moves vacuum, vacuums if needed, and adds to stack + visited list if appropriate.
        for i in range(4):
            isVaccuummed = False
            newColumn = curr.column + columnMoves[i]
            newRow = curr.row + rowMoves[i]
            if isValid(newColumn, newRow, columnLimit, rowLimit) and curr.world[newRow][newColumn] != '#':
                numberGenerated = numberGenerated + 1
                # makes a complete copy of the world, then moves the robot
                newWorld = [rows[:] for rows in curr.world]
                newWorld[curr.row][curr.column] = '_'
                # if it is dirty vacuums it up, otherwise just move the robot
                if newWorld[newRow][newColumn] == '*':
                    isVaccuummed = True
                newWorld[newRow][newColumn] = '@'
                # Sets state to be added, it has to be a map of tuples because list is mutable
                worldTuple = (tuple(map(tuple, newWorld)), newRow, newColumn)
                # if state not in visited, put it into visited. Then add to stack. Also add to solution set
                if worldTuple not in visited:
                    newSolution = curr.solution + [directionNames[i]]
                    if isVaccuummed:
                        newSolution.append("V")
                    visited.add(worldTuple)
                    stack.append(WorldState(newWorld, newColumn, newRow, newSolution))
    print("no valid solution")
    sys.exit()

# function to do the actual BFS, takes in a world state and the size of the world
def BFS(world: WorldState, columnLimit, rowLimit):
    # All possible moves in order of Left, Right, Down, Up
    rowMoves = [0, 0, 1, -1]
    columnMoves = [-1, 1, 0, 0]
    directionNames = ["W", "E", "S", "N"]
    numberExpanded = 0
    numberGenerated = 0

    q = deque()
    visited = set()
    q.append(world)

    while q:
        curr = q.popleft()
        numberExpanded = numberExpanded + 1
        printWorld(curr)

        if isSolution(curr.world):
            return curr.solution, numberGenerated, numberExpanded

        # this for loop goes through 0-3 which is all valid directions, checks if direction is legal,
        # then it moves vacuum, vacuums if needed, and adds to stack + visited list if appropriate.
        for i in range(4):
            isVaccuummed = False
            newColumn = curr.column + columnMoves[i]
            newRow = curr.row + rowMoves[i]
            if isValid(newColumn, newRow, columnLimit, rowLimit) and curr.world[newRow][newColumn] != '#':
                numberGenerated = numberGenerated + 1
                # makes a complete copy of the world, then moves the robot
                newWorld = [rows[:] for rows in curr.world]
                newWorld[curr.row][curr.column] = '_'
                # if it is dirty vacuums it up, otherwise just move the robot
                if newWorld[newRow][newColumn] == '*':
                    isVaccuummed = True
                newWorld[newRow][newColumn] = '@'
                # Sets state to be added, it has to be a map of tuples because list is mutable
                worldTuple = (tuple(map(tuple, newWorld)), newRow, newColumn)
                # if state not in visited, put it into visited. Then add to stack. Also add to solution set
                if worldTuple not in visited:
                    newSolution = curr.solution + [directionNames[i]]
                    if isVaccuummed:
                        newSolution.append("V")
                    visited.add(worldTuple)
                    q.append(WorldState(newWorld, newColumn, newRow, newSolution))
    print("no valid solution")
    sys.exit()

# TODO : MAKE THIS WORK WITH ANY FILE NAME
if __name__ == '__main__':
    if len(sys.argv) == 3:
        algorithm = sys.argv[1]
        if algorithm not in ["uniform-cost", "depth-first"]:
            print("Please input a valid algorithm")
            sys.exit()
        worldFile = sys.argv[2]
    else:
        print("Invalid Number of Arguments")
        sys.exit()
    with open(worldFile, "r") as file:
        # World can now be accessed in terms of coordinates using WorldState.world[row][column]
        fileLines = [list(line.strip()) for line in file]
    # set all the important starting variables
    startColumn, startRow, columnLimit, rowLimit\
        = generateVariables(fileLines[2:], int(fileLines[1][0]), int(fileLines[0][0]))
    initialWorld = WorldState(fileLines[2:], startColumn, startRow, [])

    # DFS
    if algorithm == "depth-first":
        directions, generated, expanded = DFS(initialWorld, columnLimit, rowLimit)
        for direction in directions:
            print(direction)
        print("{} nodes generated".format(generated))
        print("{} nodes expanded".format(expanded))

    # BFS
    if algorithm == "uniform-cost":
        directions, generated, expanded = BFS(initialWorld, columnLimit, rowLimit)
        for direction in directions:
            print(direction)
        print("{} nodes generated".format(generated))
        print("{} nodes expanded".format(expanded))

