
msgHeader = "[WORLD]: "

class World():
    def __init__(self, agents, vehicles, waypoints):
        self.worldData = {'agents': agents, 'vehicles': vehicles, 'waypoints': waypoints}
        print(msgHeader + "Initialisation complete.")

    # Update the world state.
    def update(self, car_locations):
        for known_vehicle in self.worldData['vehicles']:
            updated = False
            for observed_car in car_locations:
                if observed_car['ID'] == known_vehicle.owner.ID:
                    known_vehicle.position = observed_car['position']
                    known_vehicle.orientation = observed_car['orientation']
                    #If car has no current waypoint, assign it to the nearest one
                    if (known_vehicle.waypoint_index == None):
                        dists = [0] * len(self.worldData['waypoints'])
                        if (self.worldData['waypoints'] != []):
                            closest_wp = 0
                            index = 0
                            for wp in self.worldData['waypoints']:
                                dx = known_vehicle.position[0] - wp[0]
                                dy = known_vehicle.position[1] - wp[1]
                                dists[index] = dx*dx + dy*dy
                                if (dists[index] < dists[closest_wp]):
                                    closest_wp = index
                                    index += 1
                            known_vehicle.waypoint_index = closest_wp
                        else:
                            print("No Waypoints Loaded")
                    updated = True
                    break
            if not updated:
                known_vehicle.position = (None, None)
                known_vehicle.orientation = None

    def getWorldData(self):
        return self.worldData
