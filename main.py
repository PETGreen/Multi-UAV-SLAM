from environment import Environment
from robot import searchAStar
import random
import queue as q
import numpy as np

np.set_printoptions(threshold = np.nan, suppress = True, linewidth = 300)

"""Code below this line is code for multi-robot search"""

robotCount = 2
newInfo = []
stuck = []

#Initilize environment (SIZE, Wall%, # of Robots)
World = Environment((20,20), .50, robotCount)
print("World Map:\n", World.envMatrix)
for i in range(robotCount):
    World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix)
    World.robots[i].getGoals()
    newInfo.append(False)
    stuck.append(False)
    print("Local Map", i,"\n", World.robots[i].localMap)

trace = False
count = 0
#Run loop while any robots are not stuck
while (False in stuck):
    for i in range(robotCount):

        """Goals Update"""
        #If the current goal is no longer unknown, get new goal. Goal initializes as origin.
        if (World.robots[i].localMap[World.robots[i].goal[0]][World.robots[i].goal[1]] != 3) or newInfo[i]:
            legalGoal = False
            while not legalGoal and not stuck[i]:
                #Are there any remaining goals?
                if len(World.robots[i].goalsList) > 0:
                    #Do we have new info but havnt reached the current goal?
                    if not newInfo[i]:
                        #Get new goal from goals list
                        World.robots[i].goal = World.robots[i].getNextGoal()
                    newInfo[i] = False
                    #Is the current goal still unknown?
                    if World.robots[i].localMap[World.robots[i].goal[0]][World.robots[i].goal[1]] == 3:
                        #A* search to get path to goal
                        Search0 = searchAStar(World.robots[i].location, World.robots[i].goal, World.robots[i].localMap)
                        solution = Search0.solve()
                        World.robots[i].currentPath = q.Queue()
                        for step in solution:
                            World.robots[i].currentPath.put(step)
                            legalGoal = True
                    # else:
                    #     print("Removing goal: {}".format(World.robots[i].goal))
                else:
                    #If no remaining goals, consider the robot stuck
                    stuck[i] = True

        """Movement update"""
        if not stuck[i]:
            nextMove = World.robots[i].currentPath.get()
            #Only move to the next location if it is empty
            if World.robots[i].localMap[nextMove[0]][nextMove[1]] == 0:
                direction = [nextMove[0] - World.robots[i].location[0], nextMove[1] - World.robots[i].location[1]]
                World.robots[i].move(nextMove)
                World.updateEnvMatrix(i, direction)
                World.robots[i].updateMap(World.robotsLocation[i], World.envMatrix)
                World.robots[i].getGoals()
            else:
                newInfo[i] = True
    if trace:
        print("World Map:\n", World.envMatrix)
        for i in range(robotCount):
            print("Local Map", i,"\n", World.robots[i].localMap)
        input('waiting')
print("World Map:\n", World.envMatrix)
for i in range(robotCount):
    print("Local Map", i,"\n", World.robots[i].localMap)



"""Code below this line works for one robot only"""
"""#Initilize environment (SIZE, Wall%, # of Robots)
Env1 = Environment((96, 96), .2, 1)
Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
Env1.robots[0].getGoals()

print("World Map:\n", Env1.envMatrix)
print("Local Map:\n", Env1.robots[0].localMap)

trace = False
newInfo = False
stuck = False
while not stuck: #Loop until robot has no unknown locations


    #If the current goal is no longer unknown, get new goal. Goal initializes as origin.
    if (Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] != 3) or newInfo:
        legalGoal = False
        while not legalGoal and not stuck:
            if len(Env1.robots[0].goalsList) > 0:
                if not newInfo:
                    Env1.robots[0].goal = Env1.robots[0].getNextGoal()
                newInfo = False
                if Env1.robots[0].localMap[Env1.robots[0].goal[0]][Env1.robots[0].goal[1]] == 3:
                    Search0 = searchAStar(Env1.robots[0].location, Env1.robots[0].goal, Env1.robots[0].localMap)
                    solution = Search0.solve()
                    Env1.robots[0].currentPath = q.Queue()
                    for i in solution:
                        Env1.robots[0].currentPath.put(i)
                        legalGoal = True
                # else:
                #     print("Removing goal: {}".format(Env1.robots[0].goal))
            else:
                stuck = True

    if trace:
        print("World Map:\n", Env1.envMatrix)
        print("Local Map:\n", Env1.robots[0].localMap)
        print("World Location:", Env1.robotsLocation[0])
        print("Relative Location:", Env1.robots[0].location)
        print("Current Goal", Env1.robots[0].goal)
        print("Goals list", Env1.robots[0].goalsList)
        input('waiting...')
    nextMove = Env1.robots[0].currentPath.get()
    if Env1.robots[0].localMap[nextMove[0]][nextMove[1]] == 0:
        direction = [nextMove[0] - Env1.robots[0].location[0], nextMove[1] - Env1.robots[0].location[1]]
        Env1.robots[0].move(nextMove)
        Env1.updateEnvMatrix(0, direction)
        Env1.robots[0].updateMap(Env1.robotsLocation[0], Env1.envMatrix)
        Env1.robots[0].getGoals()
    else:
        newInfo = True

print("World Map:\n", Env1.envMatrix)
print("Local Map:\n", Env1.robots[0].localMap)"""
