from controller.agent import Agent
from controller.vision import Vision
from controller.world import World
from controller.display import Display
from controller.zenwheels.cars import *
from controller.zenwheels.comms import CarCommunicator
import time

msgHeader = "[MAIN]: "

def main(map_image_path, map_info_path, car_parameters, map_parameters):
    print("")
    print("========================================")
    print("         TABLETOP CAR SIMULATOR         ")
    print("========================================")
    print("")

    print(msgHeader + "Begin initialisation.")

    # Initialise display.
    display = Display(map_image_path=map_image_path)

    # Initialise vision server.
    display.connectingToTrackerScreen()
    vision = Vision()

    while True:
        # Check that the tracker is calibrated.
        corners = vision.confirm_calibrated()
        # Display the calibration screen.
        if corners is None:
            display.calibrationScreen()
        else:
            display.calibrationScreen(corners=corners)
            time.sleep(3)
            break

    # Initialise agents and their vehicles.
    agents = []
    vehicles = []
    for car in car_parameters:
        enabled = car[2]
        if not enabled:
            continue
        agentID = MAC_TO_ID[car[1]]
        agent = Agent(agentID, agentType=car[4], vehicleType=car[5], strategyFile=car[3])
        agents.append(agent)
        vehicles.append(agent.vehicle)

    if not agents:
        print(msgHeader + "No cars enabled. Exiting...")
        exit()

    # Initialise world.
    #f = open(map_info_path,'rb')
    #waypoints = eval(f.read())
    waypoints = None
    world = World(agents, vehicles, waypoints, map_parameters)

    ## Display the car loading screen.
    #display.connectingToCarsScreen()

    ## Initialise car communicator.
    #comms = CarCommunicator(vehicles)

    #while True:
    #    # Display the identifying cars screen.
    #    display.identifyingCarsScreen(world.getWorldData()['agents'])
    #    numCarsFound = vision.confirm_identified()
    #    if numCarsFound is None:
    #        continue
    #    elif numCarsFound != len(agents):
    #        print(msgHeader + "Number of cars found (" + str(numCarsFound)
    #              + ") does not match the number of cars enabled (" + str(len(agents)) + "). Exiting...")
    #        exit()
    #    else:
    #        break

    # Event loop.
    print(msgHeader + "Entering main loop.")
    while True:
        car_locations = vision.locateCars()
        world.update(car_locations)
        display.update(world.getWorldData())
        for agent in agents:
            agent.update_world_knowledge(world.getWorldData())
            agent.make_decision()

