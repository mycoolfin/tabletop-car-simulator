import controller.vehicle as vehicle
import math

msgHeader = "[AGENT]: "

class Agent():
    def __init__(self, ID, agentType="Regular", vehicleType="car", strategyFile=None):
        self.ID = str(ID)
        self.visMode = agentType

        if vehicleType.lower() == "car":
            self.vehicle = vehicle.Car(self)
        elif vehicleType.lower() == "truck":
            self.vehicle = vehicle.Truck(self)
        elif vehicleType.lower() == "motorcycle":
            self.vehicle = vehicle.Motorcycle(self)
        elif vehicleType.lower() == "bicycle":
            self.vehicle = vehicle.Bicycle(self)
        else:
            print(msgHeader + "Could not initialise Agent " + self.ID + " with vehicle type '" + vehicleType + "'.")
            self.vehicle = vehicle.Car(self)

        self.worldKnowledge = {'waypoints': [],
                               'obstacles': [],
                               'map_params': []}
        self.strategy = None
        if strategyFile is not None:
            try:
                with open(strategyFile, "r") as f:
                    self.strategy = f.read()
                print(msgHeader + "Successfully loaded the strategy file for Agent " + self.ID + ".")
            except:
                print(msgHeader + "Could not open the strategy file for Agent " + self.ID + ". (Fatal)")
                exit()

    def update_world_knowledge(self, worldData):
        # TODO: Work on this.
        for key in self.worldKnowledge:
            if key in worldData:
                self.worldKnowledge[key] = worldData[key]

    def make_decision(self):
        if self.strategy is not None:
            # TODO: Should probably find a more secure way to run custom agent scripts.
            exec(self.strategy)
        else:
            self.default_strategy()

    def default_strategy(self):
        pass
