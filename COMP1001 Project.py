def solver():
    """
    The body function designed to interconnect all functions.
    # Input: None
    # Output: None
    """
    allStates = genState() # Generate a list of all possible states
    # Each letter can either be "E"(east) or "W"(west)
    # The first letter in lower case simbolizes the position of the boat
    # The other 6 letters in uppercase represents following resprectively:
    # (Green Wife, Green Husband, Blue Wife, Blue Husband, Red Wife, Red Husband)

    print (allStates)
    
    graph = genGraph(allStates) 
    # Generate a dictionary where keys are all legal states, and its values are possible adjacent states 
    print (graph)
    path = findShortestPath(graph, "eEEEEEE", "wWWWWWW", path=[])
    # With given graph, finds a shortest path from the start ("eEEEEEE") to the end ("wWWWWWW")
    print (path)
    genTrip(path)
    # Print the path using readable sentences

def genState():
    """
    The function designed to create all illegal states in the problem
    # Input: None
    # Output: A list containing all illegal states
    """
    position = ("E","W") # people's position are represented by upper case
    boatPosition = ("e","w")# the boat's position are represented by lower case 
    allState = []
    for boat in boatPosition:
        for GW in position:
            for GH in position:
                for BW in position:
                    for BH in position:
                        for RW in position:
                            for RH in position:
                                aState = boat+GW+GH+BW+BH+RW+RH # Combine all of the letter into a single string
                                allState.append(aState)# Add the sting into the list
    return allState

def genGraph(allStates):
    """
    The fucntion designed to create the graph of the problem
    Input: A list, containing all illegal states
    Output: A dictionary, describing possible moves for each legal states
    """

    legalList = [] # Empty list for legal states
    graph = {}  # Empty Set for graph

    for i in range (len(allStates)): # for each illigal state
        if isStateLegal(allStates[i]) == True: # if state is legal
            legalList.append(allStates[i]) # add to legal list

    for item in legalList: #Create empty set for legal state as the key of the dictionary
        graph[item] = set()

    for item in legalList: # for each item in the list
        for i in range (len(legalList)):
            if isMoveLegal(item,legalList[i]) == True: # if two of legal states are neighbours 
                graph[item].add(legalList[i])  # add as the value of particular state 

    return graph

def isStateLegal(theState):
    """
    A function design to check where a state is legal or not.
    # Input: A string, which is a state from the problem.
    # Output: A boolean, return True if the state is legal, otherwise return False.
    """
    # Rule: A husband cannot let his wife be with another man without his presence.
    if (theState[1] != theState[2] ) and (theState[1] == theState[4] or theState[1] == theState[6]):
        return False
    elif (theState[3] != theState[4]) and (theState[3] == theState[2] or theState[3] == theState[6]):
        return False
    elif (theState[5] != theState[6]) and (theState[5] == theState[2] or theState[5] == theState[4]):
        return False
    elif theState == ('wEEEEEE') or theState == ('eWWWWWW'):
        return False
    # At start, the boat will not be in the other side,  At end, the last move will always take the boat to the west 
    else:
        return True

def isMoveLegal(current,target):

    """
    A function design to check whether two legal states can move from one to another.
    # Input: Two strings, both are legal states from the problem.
    # Output: A boolean, return Ture if two states are neignbour states, otherwise return False.
    """
    
    if current[0] != target[0]: 
    # 1st filter: check whether the boat is moving to the other side or not, return false if boat positions are same
        difference = 0
        for i in range(1, len(target)): # for loop to check each letter
            if current[i] != target[i]: # if distinct letters are found
                if target[i] == (target[0]).upper():
                # 2nd filter: check whether the distict letter is moveable (matches with the boat's direction) or not, 
                # return False if unmoveable letter targeted
                    difference += 1 # If true, count the people who is moving
                else:
                    return False    
        if difference == 1 or difference == 2:
        # 3rd filter: check whether the person/people are at least one, and at most two people drivingf
        # rule: the boat capacity is two and requires one person to drive the boat
            return True
        else:
            return False
    else:
        return False


def findShortestPath(graph, start, end, path=[]):
    """
    A function to find a shortest path from start to end on a graph
    This function is obtained from https://www.python.org/doc/essays/graphs/
    with one change due to the deprecation of the method has_key().

    Input: A graph, a starting node, an end node and an empty path
    Output: Return the shortest path in the form of a list.
    """

    path = path + [start]
    if start == end:
        return path
    #    if not graph.has_key(start):
    if not (start in graph):
        return None
    shortestPath = None
    for node in graph[start]:
        if node not in path:
            newpath = findShortestPath(graph, node, end, path)
            if newpath:
                if not shortestPath or len(newpath) < len(shortestPath):
                    shortestPath = newpath
    return shortestPath

def genTrip(path):
    stateDefinition = ["position","green wife","green husband","blue wife","blue husband","red wife","red husband"]
    # List defining each letter's representations in a state

    for state in range(1,len(path)): # starts from second state because first state (the start point, "eEEEEEE") is not required to be printed 
        # Set direction according to the boat position
        if path[state][0] == "w":
            directionFrom = "east"
            directionTo = "west"
        else:
            directionFrom = "west"
            directionTo = "east"

        firstObject = 0 
        secondObject = 0
        # This two integers will spot the person who is moving
        character = 1 # character representations of the people, as well as a integer to controls the infinate while loop
        while True:
            if path[state][character] != path[state-1][character]: # find a difference compare to the previous state from left to right
                firstObject = character #if found, break
                break
            else:
                character += 1 # incresing character make checking from left to right
        character = 6
        while True:
            if path[state][character] != path[state-1][character]: # find a difference compare to the previous state from right to left
                                                                   # if only one person moves, firstObject will be the same as second object
                secondObject = character #if found, break
                break
            else:
                character -= 1 # decresing character make checking from right to left
        
        if firstObject == secondObject: # if two values are the same, meaning only one moves
            print ("{!s} The {!s} goes form the {!s} to the {!s}.".format(str(state),stateDefinition[firstObject],directionFrom,directionTo))
        else: # when two people move
            print ("{!s} The {!s} and {!s} go from the {!s} to the {!s}.".format(str(state),stateDefinition[firstObject],stateDefinition[secondObject],directionFrom,directionTo))
solver()
