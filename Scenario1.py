import numpy
import sys
from FourRooms import FourRooms
import matplotlib.pyplot as mplt


def epsilon_decay(Q,currentPack,currentPos, initial_epsilon, min_epsilon, decay_rate, episode):
    epsilon = max(min_epsilon, initial_epsilon * (decay_rate ** episode))
    
    if numpy.random.random() < epsilon:
        action = numpy.random.randint(0, 4)
    else:
        action = numpy.argmax([Q[currentPos[0]][currentPos[1]][currentPack][a] for a in range(4)])
    return action

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
        fourRoomsObj = FourRooms('simple',True)
    else:
        fourRoomsObj = FourRooms('simple')
    aTypes = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']

    print('Agent starts at: {0}'.format(fourRoomsObj.getPosition()))
    
    Q = numpy.zeros((13,13,2,4))

    Learning_R= 0.1 # alpha
    disF = 0.8 # gamma

    #Parameters for epsilon decay
    iEpsilon =0.9
    minEpsi=0.05
    decay = 0.99

    # Parameters for boltsman
    iTemp = 2.0
    minTemp = 0.1
    tDecay = 0.995

    graph =[]
    
    epochs = 1000

    for i in range(epochs):
        fourRoomsObj.newEpoch()
        isTerminal = False
        actions = 0

        currentPos = fourRoomsObj.getPosition()
        currentPack = fourRoomsObj.getPackagesRemaining()

        while not isTerminal:
            action = epsilon_decay(Q,currentPack,currentPos,iEpsilon,minEpsi,decay,i)
            #action = boltzmann_exploration(Q, currentPack, currentPos,iTemp, minTemp, tDecay, i)

            gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(action)
            actions+=1

            if gridType >0:
               reward =20
            elif isTerminal:
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

            if actions>100:
                break
        graph.append(actions)

     # Show Path
    # fourRoomsObj.showPath(-1,"Scenario1_Boltzman.png")
    fourRoomsObj.showPath(-1,"Scenario1_EpsilonDecay.png")
    
    try:
        mplt.figure(figsize=(10,6))
        mplt.plot(graph)
        mplt.xlabel("Epoch")
        mplt.ylabel("Steps")
        mplt.title("Epsilon Decay")
        mplt.savefig("Epsilon Decay.png")
        # mplt.title("Boltzman")
        # mplt.savefig("Boltzman.png")
    except ImportError:
        print("Aint plotting")

    

   

if __name__ == "__main__":
    main()