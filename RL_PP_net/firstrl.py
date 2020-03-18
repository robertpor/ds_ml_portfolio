#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 19:20:22 2020

@author: robertpormetter
"""

import gym
import numpy as np
import matplotlib.pyplot as plt


env = gym.make("MountainCar-v0")
# env.reset()

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 26000

SHOW_EVERY = 200

DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

epsilon = 0.5
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // 2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)


q_table = np.random.uniform(low = -2, high = 0, size = (DISCRETE_OS_SIZE + [env.action_space.n]))

ep_rewards = []
aggr_ep_rewards = {"ep": [], "avg":[], "min":[], "max":[]}



def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(np.int))

for episode in range(EPISODES):
    episode_reward = 0
    if episode % SHOW_EVERY == 2:
        print(episode)
        render = True
    else:
        render = False
        
    discrete_state = get_discrete_state(env.reset())
    done = False
    
    while not done:
        action = np.argmax(q_table[discrete_state])
        new_state, reward, done, _ = env.step(action)
        episode_reward += reward
        new_discrete_state = get_discrete_state(new_state)
        if render:
            env.render()
        if not done:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state + (action,)]
            
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state + (action, )] = new_q
            
        elif new_state[0] >= env.goal_position:
            print("We made it on episode", episode)
            q_table[discrete_state + (action, )] = 0
        
        discrete_state = new_discrete_state
        
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        epsilon -= epsilon_decay_value

    ep_rewards.append(episode_reward)

    if not episode % SHOW_EVERY:
        average_reward = sum(ep_rewards[-SHOW_EVERY:]) / len(ep_rewards [-SHOW_EVERY:])
        aggr_ep_rewards["ep"].append(episode)
        aggr_ep_rewards["avg"].append(average_reward)
        aggr_ep_rewards["min"].append(min(ep_rewards[-SHOW_EVERY:]))
        aggr_ep_rewards["max"].append(max(ep_rewards[-SHOW_EVERY:]))
        
        print("Episode:", episode, "Avg:", average_reward, "Min:",min(ep_rewards[-SHOW_EVERY:]), "Max:", max(ep_rewards[-SHOW_EVERY:])  )
        
        

        
        
env.close()


plt.plot(aggr_ep_rewards["ep"], aggr_ep_rewards["avg"], label = "avg")
plt.plot(aggr_ep_rewards["ep"], aggr_ep_rewards["min"], label = "min")
plt.plot(aggr_ep_rewards["ep"], aggr_ep_rewards["max"], label = "max")
plt.legend(loc = 4)
plt.show()

