import numpy as np
import tensorflow as tf
from vrp.model.vrp_env import VRP_env
from vrp.model.actor import Actor
from vrp.model.critic import Critic


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


test_set1 = dict()
test_set1['nS'] = 12
test_set1['nV'] = 4
test_set1['depot'] = (0.0, 0.0)
test_set1['stations'] = [(-13.0, -5.0), (-12.0, -9.0), (-11.0, -7.0), (-10.0, -8.0),
                         (-2.0, 15.0), (-1.0, 13.0), (3.0, 17.0), (4.0, 14.0),
                         (15.0, 3.0), (16.0, -1.0), (17.0, 2.0), (18.0, -3.0)
                         ]
test_set1['distance_matrix'] = np.zeros((test_set1['nS'] + 1, test_set1['nS'] + 1), dtype=dict)
for i in range(test_set1['nS'] + 1):
    for j in range(test_set1['nS'] + 1):
        test_set1['distance_matrix'][i, j] = dict()

test_set1['distance_matrix'][0, 0] = {'dist': 0.0, 'time': 0.0}

for i in range(1, test_set1['nS'] + 1):
    manhattan_dist = manhattan_distance(test_set1['stations'][i - 1], test_set1['depot'])
    curr_dict1, curr_dict2 = dict(), dict()
    curr_dict1['dist'] = manhattan_dist  # + np.random.randint(-20, 50) * 0.1
    curr_dict1['time'] = curr_dict1['dist'] * 2 + np.random.randint(-5, 5) * 0.1
    curr_dict2['dist'] = manhattan_dist  # + np.random.randint(-20, 50) * 0.1
    curr_dict2['time'] = curr_dict2['dist'] * 2 + np.random.randint(-5, 5) * 0.1
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
cutoff_dist = 100
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
test_set1['total_seats'] = 4

np.random.seed(2)
tf.set_random_seed(2)  # reproducible
MAX_EPISODE = 3000
MAX_EP_STEPS = 1000   # maximum time step in one episode
GAMMA = 0.9     # reward discount in TD error
LR_A = 0.0003    # learning rate for actor
LR_C = 0.003
N_F = 4
N_A = 13

sess = tf.Session()

actor = Actor(sess, n_features=N_F, n_actions=N_A, lr=LR_A)
critic = Critic(sess, n_features=N_F, lr=LR_C)     # we need a good teacher, so the teacher should learn faster than the actor
DISPLAY_REWARD_THRESHOLD = 200
sess.run(tf.global_variables_initializer())

for i_episode in range(MAX_EPISODE):
    t = 0
    track_r = []

    env = VRP_env(test_set1['nS'], test_set1['depot'], test_set1['stations'], test_set1['distance_matrix'],
                  test_set1['station_action_response'], test_set1['fuel_cost_per_unit'], test_set1['vehicle_cost'],
                  test_set1['total_seats'])
    s = np.array([0.0, 0.0, 0, 4])
    actions_chosen = [0]
    while True:

        a = actor.choose_action(s, env.demand, env.distance_matrix[env.state_id])
        actions_chosen.append(a)
        s_, r, done, info = env.step(a)
        if env.state_id != a:
            actions_chosen.append(env.state_id)

        track_r.append(r)

        td_error = critic.learn(s, r, s_)  # gradient = grad[r + gamma * V(s_) - V(s)]
        actor.learn(s, a, td_error)  # true_gradient = grad[logPi(s,a) * td_error]

        s = s_
        t += 1

        if done or t >= MAX_EP_STEPS:

            ep_rs_sum = sum(track_r)

            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.95 + ep_rs_sum * 0.05
            # if running_reward > DISPLAY_REWARD_THRESHOLD: RENDER = True  # rendering
            print(actions_chosen)
            print("episode:", i_episode, "  reward:", int(running_reward), " time:", int(t))
            print("________________________________________________________________________________")
            break
