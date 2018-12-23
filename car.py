import numpy

def compute_utility(states, terminalCoordinates, transitionStates, reward):
    initialUtility = numpy.zeros((gridSize, gridSize))
    stopValue = numpy.float64(0.1 * (1 - 0.9)/ 0.9)
    while True:
        utilityMatrix = initialUtility.copy()
        delta = numpy.float64(0)
        for state in states:
            possibleStates = transitionStates[state]
            maxVal = numpy.float64(-99999)
            for action in range(len(actions)):
                actionDir, val = get_action_value(possibleStates, action, utilityMatrix) 
                if maxVal == val and actionDir < prevActionDir :
                    maxVal = val
                    prevActionDir = actionDir
                elif maxVal < val:
                    maxVal = val
                    prevActionDir = actionDir
            initialUtility[state] = reward[state] + 0.9 * maxVal
            delta = max(delta, abs(initialUtility[state] - utilityMatrix[state]))
        initialUtility[(terminalCoordinates[1],terminalCoordinates[0])] = 99
        if delta < stopValue:
            return utilityMatrix

def get_action_value(actionsList, action, utility):
    if action == 0:
        return action, numpy.float64(utility[actionsList[0]] * 0.7 + 0.1 * (utility[actionsList[1]] + utility[actionsList[2]] + utility[actionsList[3]]))
    if action == 1:
        return action, numpy.float64(utility[actionsList[1]] * 0.7 + 0.1 * (utility[actionsList[0]] + utility[actionsList[2]] + utility[actionsList[3]]))
    if action == 2:
        return action, numpy.float64(utility[actionsList[2]] * 0.7 + 0.1 * (utility[actionsList[0]] + utility[actionsList[1]] + utility[actionsList[3]]))
    if action == 3:
        return action, numpy.float64(utility[actionsList[3]] * 0.7 + 0.1 * (utility[actionsList[0]] + utility[actionsList[1]] + utility[actionsList[2]]))
    return -1, -1

def get_policy_matrix(utility, transitionStates, states):
    policyMatrix = {}
    for state in states:
        neighbors = transitionStates[state]
        maxVal = numpy.float64(-99999)
        maxState = -1
        for action in range(len(actions)):
            dir, val = get_action_value(neighbors, action, utility)
            if maxVal == val and maxState > dir:
                maxVal = val
                maxState = dir
            elif maxVal < val:
                maxVal = val
                maxState = dir
        policyMatrix[state] = maxState
    return policyMatrix


def calculate_transition_states(states, gridSize):
    transitionStates = {}
    for state in states:
        transitionStates[state] = get_transition_for_state(state)
    return transitionStates

def get_transition_for_state(state):
    x = state[0]
    y = state[1]
    up = x -1
    down = x +1
    left = y -1
    right = y + 1
    dir = []
    if up < 0:
        up = 0
    if down >= gridSize:
        down = gridSize -1
    if left < 0:
        left = 0
    if right >= gridSize:
        right = gridSize -1
    dir.append((up, y))
    dir.append((down, y))
    dir.append((x, right))
    dir.append((x, left))
    return dir

def turn_left(dir):
    if dir == 0:
        return 3
    if dir == 1:
        return 2
    if dir == 2:
        return 0
    if dir == 3:
        return 1
    return -1

def turn_right(dir):
    if dir == 0:
        return 2
    if dir == 1:
        return 3
    if dir == 2:
        return 1
    if dir == 3:
        return 0
    return -1

if __name__ == '__main__':
    inputFile = open("input.txt", "rt")
    outputFile = open("output.txt", "w")
    gridSize = int(inputFile.readline())
    numOfCars = int(inputFile.readline())
    numOfObstacles = int(inputFile.readline())
    grid = numpy.zeros((gridSize, gridSize))
    grid.fill(-1)
    startPositions = []
    terminalPositions = []
    for k in range(numOfObstacles):
        coordinates = inputFile.readline().strip().split(',')
        grid[int(coordinates[0])][int(coordinates[1])] = -101 
    for k in range(numOfCars):
        startPositions.append(inputFile.readline().strip().split(','))
    for k in range(numOfCars):
        terminalPositions.append(inputFile.readline().strip().split(','))    
    actions = ["N","S","E","W"]
    result = ""
    for k in range(numOfCars):
        totalReward = 0
        rewardsList = {}
        newGrid = grid.copy()
        terminalCoordinates = terminalPositions[k]
        terminalCoordinates = ((int(terminalCoordinates[0]),int(terminalCoordinates[1])))
        newGrid[terminalCoordinates[0]][terminalCoordinates[1]] = 99
        startCoordinates = startPositions[k]
        current = (int(startCoordinates[1]), int(startCoordinates[0]))
        if current == (terminalCoordinates[1],terminalCoordinates[0]): #When the current location is the terminal state
            result = result + "100\n"
            continue
        states = []
        reward = {}
        for x in range(gridSize):
            for y in range(gridSize):
                if (x,y) != terminalCoordinates:
                    states.append((y, x))
                reward[(y,x)] = newGrid[x][y]
        transitionStates = calculate_transition_states(states, gridSize)
        utility = compute_utility(states, terminalCoordinates, transitionStates, reward)
        policyMatrixVal = get_policy_matrix(utility, transitionStates, states)
        terminalCoordinates = (terminalCoordinates[1],terminalCoordinates[0])
        for j in range(10):
            rewardVal = 0            
            i = 0
            numpy.random.seed(j)
            current = (int(startCoordinates[1]), int(startCoordinates[0]))
            swerve = numpy.random.random_sample(1000000)
            while current != terminalCoordinates:
                possibleStates = transitionStates[current]
                currentDir = policyMatrixVal[current]
                if swerve[i] > 0.7:
                    if swerve[i] > 0.8:
                        if swerve[i] > 0.9:
                            currentDir = turn_right(turn_right(currentDir))
                        else:
                            currentDir = turn_right(currentDir)
                    else:
                        currentDir = turn_left(currentDir)
                if possibleStates[currentDir]  != terminalCoordinates:
                        rewardVal = rewardVal + reward[possibleStates[currentDir]]
                i+=1
                current = possibleStates[currentDir]
            rewardsList[j] = rewardVal + reward[terminalCoordinates] 
            totalReward = totalReward + rewardsList[j]
        result = result + str(int(numpy.floor(totalReward/10))) + "\n"
    outputFile.write(result)
    outputFile.close()
    inputFile.close()