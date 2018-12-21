import numpy as np
import tensorflow as tf

# np.random.seed(2)
# tf.set_random_seed(2)  # reproducible

MAX_EPISODE = 10
MAX_EP_STEPS = 1000  # maximum time step in one episode
GAMMA = 0.9  # reward discount in TD error
LR_A = 0.001  # learning rate for actor
LR_C = 0.01

#############################################################################################################
# Setting up the environment for the VRP problem
# States: 1(depot) + num_stations
# Features: 4
# (1) Geopoints - (lat, lnb)
# (2) Demand - 0/1
# (3) Occupied seats
#############################################################################################################


class VRP_env(object):

    def __init__(self, nS, depot_geopoints, stations_geopoints, distance_matrix, station_action_response,
                 fuel_cost_per_unit, vehicle_cost, total_seats):
        self.nS = nS
        self.depot_geopoints = depot_geopoints
        self.stations_geopoints = stations_geopoints
        self.demand = np.ones(nS+1, dtype=int)
        self.demand[0] = 0
        self.fuel_cost_per_unit = fuel_cost_per_unit
        self.vehicle_cost = vehicle_cost
        self.vehicle_seats = total_seats
        self.vehicle_occupied_seats = 0
        self.state = np.array([0.0, 0.0, 0, self.vehicle_seats])
        self.state_id = 0
        self.distance_matrix = distance_matrix
        self.station_action_response = station_action_response
        self.time_steps = 0

    def reset(self):
        self.state = np.array([0.0, 0.0, 4, self.vehicle_seats])
        self.state_id = 0
        self.demand = np.ones(self.nS, dtype=int)
        return np.array(self.state)

    def reward(self, from_state_id, to_state_id):

        if self.vehicle_occupied_seats == self.vehicle_seats:
            return 0
        unoccupied_seats = self.vehicle_seats - self.vehicle_occupied_seats
        if from_state_id != to_state_id:
            unoccupied_seats -= 1

        required_route = self.distance_matrix[from_state_id, to_state_id]
        dist = required_route['dist']
        time = required_route['time']
        reward = -(0.3 * dist * self.fuel_cost_per_unit + 0.3 * time + 0.2 * unoccupied_seats + 0.2 * self.vehicle_cost)
        return reward

    def step(self, action):
        done = False
        self.time_steps += 1
        info = dict()
        info["time_steps"] = self.time_steps

        from_state_id = self.state_id
        to_state_id = self.state_id = action

        r = self.reward(from_state_id, to_state_id)

        # print("Action: ", action, ", Seats occupied: ", self.vehicle_occupied_seats)
        if action == 0:
            self.vehicle_occupied_seats = 0
        elif self.vehicle_occupied_seats < self.vehicle_seats:
            self.vehicle_occupied_seats += 1
            self.demand[action] = 0

        if self.vehicle_occupied_seats == self.vehicle_seats:
            r += self.reward(to_state_id, 0)
            self.state_id = 0
            self.vehicle_occupied_seats = 0

        # print(self.demand)
        if sum(self.demand) == 0:
            done = True
            if self.state_id != 0:
                r += self.reward(to_state_id, 0)
                self.state_id = 0
                self.vehicle_occupied_seats = 0

        to_station = self.stations_geopoints[self.state_id - 1]
        obs = np.array([to_station[0], to_station[1], int(self.demand[action-1]), int(self.vehicle_occupied_seats)])

        return obs, r, done, info
