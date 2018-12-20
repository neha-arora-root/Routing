import numpy as np
import tensorflow as tf

np.random.seed(2)
tf.set_random_seed(2)  # reproducible

MAX_EPISODE = 10
MAX_EP_STEPS = 1000  # maximum time step in one episode
GAMMA = 0.9  # reward discount in TD error
LR_A = 0.001  # learning rate for actor
LR_C = 0.01


# Setting up the environment for the VRP problem
class VRP_env(object):

    def __init__(self, nS, depot_geopoints, nV, distance_matrix, station_action_response, fuel_cost_per_unit,
                 vehicle_cost, total_seats):
        self.nS = nS
        self.nV = nV
        self.depot_geopoints = depot_geopoints
        self.demand = np.zeros(nS)
        for i in range(nS):
            self.demand[i] = 1
        self.state = np.zeros(nV)
        self.fuel_cost_per_unit = fuel_cost_per_unit
        self.vehicle_cost = vehicle_cost
        self.total_seats = np.zeros(nV)
        self.vehicle_occupied = np.zeros(nV)
        for i in range(nV):
            self.state[i] = depot_geopoints
            self.total_seats[i] = total_seats[i]
        self.distance_matrix = distance_matrix
        self.station_action_response = station_action_response
        self.time_steps = 0

    def reward(self, from_state, to_state):
        occupied_seats = self.vehicle_occupied[from_state]
        unoccupied_seats = self.total_seats[i] - occupied_seats
        if occupied_seats == 0:
            return 0
        required_route = self.distance_matrix[from_state + 1, to_state + 1]
        dist = required_route['dist']
        time = required_route['time']
        reward = -(0.3 * dist + 0.2 * time + 0.1 * unoccupied_seats + 0.2 * self.fuel_cost + 0.2 * self.vehicle_cost)
        return reward

    def step(self, vehicles, actions):
        obs = list()
        for i in range(len(actions)):
            curr_action = actions[i]
            if curr_action is None:
                obs[i] = 0
                continue
            to_station = curr_action
            obs[i] = to_station
            from_station = self.state[i]
            self.vehicle_occupied[from_state] += 1
            r = reward(from_station, curr_action)
            self.state[from_station] = curr_action
            self.demand[from_station] = 0
        done = False
        if sum(self.demand) == 0:
            done = True
        self.time_steps += 1
        info = dict()
        info["time_steps": self.time_steps]

        return obs, r, done, info


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


test_set1 = dict()
test_set1['nS'] = 12
test_set1['nV'] = 4
test_set1['depot'] = (0.0, 0.0)
test_set1['stations'] = [(-4, 1), (-4, -1), (-3, 1), (-3, -1),
                         (-1, 5), (-1, 4), (1, 5), (1, 4),
                         (3, 1), (3, -1), (4, 1), (4, -1)
                         ]
test_set1['distance_matrix'] = np.zeros((test_set1['nS'] + 1, test_set1['nS'] + 1), dtype=dict)
for i in range(test_set1['nS'] + 1):
    for j in range(test_set1['nS'] + 1):
        test_set1['distance_matrix'][i, j] = dict()

test_set1['distance_matrix'][0, 0] = {'dist': 0.0, 'time': 0.0}

for i in range(1, test_set1['nS'] + 1):
    manhattan_dist = manhattan_distance(test_set1['stations'][i - 1], test_set1['depot'])
    curr_dict1, curr_dict2 = dict(), dict()
    curr_dict1['dist'] = manhattan_dist + np.random.randint(-20, 50) * 0.1
    curr_dict1['time'] = curr_dict1['dist'] * 2 + np.random.randint(-10, 30) * 0.1
    curr_dict2['dist'] = manhattan_dist + np.random.randint(-20, 50) * 0.1
    curr_dict2['time'] = curr_dict2['dist'] * 2 + np.random.randint(-10, 30) * 0.1
    test_set1['distance_matrix'][0, i] = curr_dict1
    test_set1['distance_matrix'][i, 0] = curr_dict2

    for j in range(1, test_set1['nS'] + 1):
        if i == j:
            test_set1['distance_matrix'][i, j] = {'dist': 0.0, 'time': 0.0}
        else:
            manhattan_dist = manhattan_distance(test_set1['stations'][i - 1], test_set1['stations'][j - 1])
            curr_dict = dict()
            curr_dict['dist'] = manhattan_dist + np.random.randint(-20, 50) * 0.1
            curr_dict['time'] = curr_dict['dist'] * 2 + np.random.randint(-10, 30) * 0.1
            test_set1['distance_matrix'][i, j] = curr_dict

test_set1['station_action_response'] = dict()
test_set1['station_action_response'][0] = list(np.arange(test_set1['nS']) + 1)
cutoff_dist = 10
for i in range(test_set1['nS']):
    from_station = i + 1
    actions_list = [0]
    for j in range(test_set1['nS']):
        if i == j:
            continue
        to_station = j + 1
        curr_route = test_set1['distance_matrix'][from_station, to_station]
        if 'dist' in curr_route:
            if curr_route['dist'] <= cutoff_dist:
                actions_list.append(j + 1)

    test_set1['station_action_response'][from_station] = actions_list

test_set1['fuel_cost_per_unit'] = 2.0
test_set1['vehicle_cost'] = 25.0
test_set1['total_seats'] = [4] * test_set1['nV']
