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
	f = open(map_info_path, 'rb')
	waypoints = eval(f.read())
	world = World(agents, vehicles, waypoints, map_parameters)

	# Display the car loading screen.
	display.connectingToCarsScreen()

	# Initialise car communicator.
	comms = CarCommunicator(vehicles)

	# Event loop.
	print(msgHeader + "Entering main loop.")
	while True:
		# Check if tracker is still connected.
		if not vision.client.isConnected or not display.isDisplaying:
			break
		car_locations = vision.locateCars()
		world.update(car_locations)
		display.update(world.getWorldData())
		for agent in agents:
			agent.update_world_knowledge(world.getWorldData())
	for agent in agents:
		agent.stop()
	print(msgHeader + "Quitting.")