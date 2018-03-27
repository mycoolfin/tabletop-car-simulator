from controller.agent import Agent
from controller.vision import Vision
from controller.world import World
from controller.display import Display
from controller.zenwheels.cars import *
from controller.zenwheels.comms import CarCommunicator


def main(map_image_path, map_info_path, car_parameters):
    print("")
    print("========================================")
    print("         TABLETOP CAR SIMULATOR         ")
    print("========================================")
    print("")

    # Initialise vision server.
    vision = Vision()

    # Initialise display.
    display = Display(map_image_path=map_image_path)

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

    # Initialise world.
    world = World(agents, vehicles)

    # Initialise car communicator.
    comms = CarCommunicator(vehicles)

    # Event loop.
    while True:
        car_locations = vision.locateCars()
        world.update(car_locations)
        display.update(world.getWorldData())
        for agent in agents:
            agent.update_world_knowledge(world.getWorldData())
            agent.make_decision()
