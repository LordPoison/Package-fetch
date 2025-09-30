import numpy
from FourRooms import FourRooms
import matplotlib.pyplot as mplt
import sys

def boltzmann_exploration(Q, currentPack, currentPos, temperature, min_temp=0.1, decay_rate=0.95, episode=0):
    current_temp = max(min_temp, temperature * (decay_rate ** episode))
    
    q_val = [Q[currentPos[0]][currentPos[1]][currentPack][a] for a in range(4)]
    
    if all(q == q_val[0] for q in q_val):
        return numpy.random.randint(0, 4)
    
    # Apply softmax with temperature
    q_new = numpy.exp((numpy.array(q_val) - max(q_val)) / current_temp)
    prob = q_new / numpy.sum(q_new)
    
    return numpy.random.choice(4, p=prob)

def main():
    # Create FourRooms Object
    if '--stochastic' in sys.argv:
        fourRoomsObj = FourRooms('multi',True)
    else:
        fourRoomsObj = FourRooms('multi')
    aTypes = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']

    print('Agent starts at: {0}'.format(fourRoomsObj.getPosition()))
    
    Q = numpy.zeros((13,13,4,4))

    Learning_R= 0.4 # alpha
    disF = 0.95 # gamma


    # Parameters for boltsman
    iTemp = 2.0
    minTemp = 0.1
    tDecay = 0.995
    
    epochs = 1000

    for i in range(epochs):
        fourRoomsObj.newEpoch()
        isTerminal = False
        actions = 0

        currentPos = fourRoomsObj.getPosition()
        currentPack = fourRoomsObj.getPackagesRemaining()

        while not isTerminal:

            action = boltzmann_exploration(Q, currentPack, currentPos,iTemp, minTemp, tDecay, i)

            gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(action)
            actions+=1

            
            if gridType >0:
               reward =20
            elif isTerminal and packagesRemaining==0:
               reward=100
            else:
               reward=-1

            oldState = Q[currentPos[0]][currentPos[1]][currentPack][action]

            if not isTerminal:
                maxQ = max([Q[newPos[0]][newPos[1]][packagesRemaining][a] for a in range(4)])
            else:
                maxQ = 0

            Q[currentPos[0]][currentPos[1]][packagesRemaining][action] = oldState + Learning_R*(reward+disF * maxQ - oldState)

            print("Agent took {0} action and moved to {1} of type {2}".format (aTypes[action], newPos, gTypes[gridType]))

            currentPos = newPos
            currentPack = packagesRemaining

            if actions>200:
                break

     # Show Path
    fourRoomsObj.showPath(-1,"Scenario2.png")
    # Don't forget to call newEpoch when you start a new simulation run
    

   

if __name__ == "__main__":
    main()