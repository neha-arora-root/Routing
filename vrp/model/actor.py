import tensorflow as tf
import numpy as np
import math


class Actor(object):

    def __init__(self, sess, n_features, n_actions, lr=0.01):
        self.sess = sess

        self.s = tf.placeholder(tf.float32, [1, n_features], "state")
        self.a = tf.placeholder(tf.int32, None, "act")
        self.td_error = tf.placeholder(tf.float32, None, "td_error")
        self.previous_action = 0

        with tf.variable_scope('Actor'):
            l1 = tf.layers.dense(
                inputs=self.s,
                units=24,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),    # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='l1'
            )

            self.acts_prob = tf.layers.dense(
                inputs=l1,
                units=n_actions,  # output units
                activation=tf.nn.softmax,   # get action probabilities
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='acts_prob'
            )

        with tf.variable_scope('exp_v'):
            log_prob = tf.log(self.acts_prob[0, self.a])
            self.exp_v = tf.reduce_mean(log_prob * self.td_error)  # advantage (TD_error) guided loss

        with tf.variable_scope('train'):
            self.train_op = tf.train.AdamOptimizer(lr).minimize(-self.exp_v)  # minimize(-exp_v) = maximize(exp_v)

    def learn(self, s, a, td):
        s = s[np.newaxis, :]
        feed_dict = {self.s: s, self.a: a, self.td_error: td}
        _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict)
        return exp_v

    def choose_action(self, s, demand, dist_time_map):
        s = s[np.newaxis, :]
        probs = self.sess.run(self.acts_prob, {self.s: s})   # get probabilities for all actions
        probs_states = list()
        for p in probs.ravel():
            probs_states.append(p)
        if max(probs_states) < 1e-5:
            min_prob_states = min(probs_states)
            for p in range(len(probs_states)):
                probs_states[p] = probs_states[p]/min_prob_states
            sum_prob_states = sum(probs_states)
            probs_states /= sum_prob_states
        probs_states[self.previous_action] = 0
        for d in range(len(demand)):
            if demand[d] == 0:
                probs_states[d] = 0
        if sum(probs_states) == 0:
            probs_states = demand
        probs_states = probs_states/sum(probs_states)
        # print(probs_states)
        choice = np.random.choice(np.arange(probs.shape[1]), p=probs_states)
        self.previous_action = choice
        return choice  # return a int
