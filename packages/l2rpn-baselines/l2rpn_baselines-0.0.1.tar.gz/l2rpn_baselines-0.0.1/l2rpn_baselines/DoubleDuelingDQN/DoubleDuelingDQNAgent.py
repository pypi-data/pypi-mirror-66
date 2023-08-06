# Copyright (c) 2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of L2RPN Baselines, L2RPN Baselines a repository to host baselines for l2rpn competitions.

import os
import json
import numpy as np
import tensorflow as tf

from grid2op.Agent import AgentWithConverter
from grid2op.Converter import IdToAct

from l2rpn_baselines.DoubleDuelingDQN.ReplayBuffer import ReplayBuffer
from l2rpn_baselines.DoubleDuelingDQN.DoubleDuelingDQN import DoubleDuelingDQN

INITIAL_EPSILON = 0.9
FINAL_EPSILON = 0.0
DECAY_EPSILON = 1024*32
STEP_EPSILON = (INITIAL_EPSILON-FINAL_EPSILON)/DECAY_EPSILON
DISCOUNT_FACTOR = 0.99
REPLAY_BUFFER_SIZE = 1024*64
UPDATE_FREQ = 32
UPDATE_TARGET_HARD_FREQ = 5
UPDATE_TARGET_SOFT_TAU = 0.01


class DoubleDuelingDQNAgent(AgentWithConverter):
    def __init__(self,
                 env,
                 action_space,
                 name=__name__,
                 num_frames=4,
                 is_training=False,
                 batch_size=32,
                 lr=1e-5):
        # Call parent constructor
        AgentWithConverter.__init__(self, action_space,
                                    action_space_converter=IdToAct)

        # Store constructor params
        self.env = env
        self.name = name
        self.num_frames = num_frames
        self.is_training = is_training
        self.batch_size = batch_size
        self.lr = lr
        
        # Declare required vars
        self.Qmain = None
        self.obs = None
        self.state = []
        self.frames = []

        # Declare training vars
        self.replay_buffer = None
        self.done = False
        self.frames2 = None
        self.epoch_rewards = None
        self.epoch_alive = None
        self.Qtarget = None
        self.epsilon = 0.0

        # Setup inital state
        self._reset_state()
        self._reset_frame_buffer()
        # Compute dimensions from intial state
        self.observation_size = self.state.shape[0]
        self.action_size = self.action_space.size()

        # Load network graph
        self.Qmain = DoubleDuelingDQN(self.action_size,
                                      self.observation_size,
                                      num_frames = self.num_frames,
                                      learning_rate = self.lr)
        # Setup training vars if needed
        if self.is_training:
            self._init_training()

    def _init_training(self):
        self.epsilon = INITIAL_EPSILON
        self.frames2 = []
        self.epoch_rewards = []
        self.epoch_alive = []
        self.replay_buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)
        self.Qtarget = DoubleDuelingDQN(self.action_size,
                                        self.observation_size,
                                        num_frames = self.num_frames,
                                        learning_rate = self.lr)

    def _reset_state(self):
        # Initial state
        self.obs = self.env.current_obs
        self.state = self.convert_obs(self.obs)
        self.done = False

    def _reset_frame_buffer(self):
        # Reset frame buffers
        self.frames = [self.state.copy() for i in range(self.num_frames)]
        if self.is_training:
            self.frames2 = [self.state.copy() for i in range(self.num_frames)]

    def _save_current_frame(self, state):
        self.frames.append(state.copy())
        if len(self.frames) > self.num_frames:
            self.frames.pop(0)

    def _save_next_frame(self, next_state):
        self.frames2.append(next_state.copy())
        if len(self.frames2) > self.num_frames:
            self.frames2.pop(0)

    def _save_hyperparameters(self, steps):
        r_instance = self.env.reward_helper.template_reward
        hp = {
            "lr": self.lr,
            "batch_size": self.batch_size,
            "stack_frames": self.num_frames,
            "iter": steps,
            "e_start": INITIAL_EPSILON,
            "e_end": FINAL_EPSILON,
            "e_decay": DECAY_EPSILON,
            "discount": DISCOUNT_FACTOR,
            "buffer_size": REPLAY_BUFFER_SIZE,
            "update_freq": UPDATE_FREQ,
            "update_hard": UPDATE_TARGET_HARD_FREQ,
            "update_soft": UPDATE_TARGET_SOFT_TAU,
            "reward": dict(r_instance)
        }
        hp_filename = "{}-hypers.json".format(self.name)
        hp_path = os.path.join("./logs", hp_filename)
        with open(hp_path, 'w') as fp:
            json.dump(hp, fp=fp, indent=2)

    ## Agent Interface
    def convert_obs(self, observation):
        # Made a custom version to normalize per attribute
        #return observation.to_vect()
        li_vect=  []
        for el in observation.attr_list_vect:
            v = observation._get_array_from_attr_name(el).astype(np.float)
            v_fix = np.nan_to_num(v)
            v_norm = np.linalg.norm(v_fix)
            if v_norm > 1e4:
                v_res = (v_fix / v_norm) * 10.0
            else:
                v_res = v_fix
            li_vect.append(v_res)
        return np.concatenate(li_vect)

    def convert_act(self, action):
        return super().convert_act(action)

    def reset(self):
        self._reset_state()
        self._reset_frame_buffer()

    def my_act(self, state, reward, done=False):
        self._save_current_frame(state)
        a, _ = self.Qmain.predict_move(np.array(self.frames))
        return a
    
    def load_network(self, path):
        self.Qmain.load_network(path)
        if self.is_training:
            self.Qmain.update_target_hard(self.Qtarget.model)

    def save_network(self, path):
        self.Qmain.save_network(path)

    ## Training Procedure
    def train(self, num_pre_training_steps, num_training_steps):
        # Make sure we can fill the experience buffer
        if num_pre_training_steps < self.batch_size * self.num_frames:
            num_pre_training_steps = self.batch_size * self.num_frames

        # Loop vars
        num_steps = num_pre_training_steps + num_training_steps
        step = 0
        self.epsilon = INITIAL_EPSILON
        alive_steps = 0
        total_reward = 0
        self.done = True

        self.tf_writer = tf.summary.create_file_writer("./logs/{}".format(self.name), name=self.name)
        self._save_hyperparameters(num_steps)
        
        # Training loop
        while step < num_steps:
            # Init first time or new episode
            if self.done:
                self.env.reset() # This shouldn't raise
                self._reset_state()
                self._reset_frame_buffer()
            if step % 1000 == 0:
                print("Step [{}] -- Random [{}]".format(step, self.epsilon))

            # Choose an action
            if step <= num_pre_training_steps:
                a = self.Qmain.random_move()
            elif len(self.frames) < self.num_frames:
                a = self.Qmain.random_move()
            elif np.random.rand(1) < self.epsilon:
                a = self.Qmain.random_move()
            else:
                a, _ = self.Qmain.predict_move(np.array(self.frames))

            # Convert it to a valid action
            act = self.convert_act(a)
            # Execute action
            new_obs, reward, self.done, info = self.env.step(act)
            new_state = self.convert_obs(new_obs)
            if info["is_illegal"] or info["is_ambiguous"] or \
               info["is_dispatching_illegal"] or info["is_illegal_reco"]:
                print (a, info)

            # Save current observation to stacking buffer
            self._save_current_frame(self.state)
            self._save_next_frame(new_state)

            # Save to experience buffer
            if len(self.frames) == self.num_frames:
                self.replay_buffer.add(np.array(self.frames),
                                       a, reward, self.done,
                                       np.array(self.frames2))

            # Perform training when we have enough experience in buffer
            if step > num_pre_training_steps:
                training_step = step - num_pre_training_steps
                # Slowly decay chance of random action
                if self.epsilon > FINAL_EPSILON:
                    self.epsilon -= STEP_EPSILON
                # Make sure we dont go below final epsilon
                if self.epsilon < FINAL_EPSILON:
                    self.epsilon = FINAL_EPSILON

                # Perform training at given frequency
                if step % UPDATE_FREQ == 0 and self.replay_buffer.size() >= self.batch_size:
                    # Sample from experience buffer
                    s_batch, a_batch, r_batch, d_batch, s1_batch = self.replay_buffer.sample(self.batch_size)
                    # Perform training
                    self._batch_train(s_batch, a_batch, r_batch, d_batch, s1_batch, step)
                    # Update target network towards primary network
                    self.Qmain.update_target_soft(self.Qtarget.model, tau=UPDATE_TARGET_SOFT_TAU)

                # Every UPDATE_TARGET_HARD_FREQ trainings, update target completely
                if step % (UPDATE_FREQ * UPDATE_TARGET_HARD_FREQ) == 0:
                    self.Qmain.update_target_hard(self.Qtarget.model)

            total_reward += reward
            if self.done:
                self.epoch_rewards.append(total_reward)
                self.epoch_alive.append(alive_steps)
                print("Survived [{}] steps".format(alive_steps))
                print("Total reward [{}]".format(total_reward))
                alive_steps = 0
                total_reward = 0
            else:
                alive_steps += 1
            
            # Save the network every 1000 iterations
            if step > 0 and step % 1000 == 0:
                self.Qmain.save_network(self.name + ".h5")

            # Iterate to next loop
            step += 1
            self.obs = new_obs
            self.state = new_state

        # Save model after all steps
        self.Qmain.save_network(self.name + ".h5")

    def _batch_train(self, s_batch, a_batch, r_batch, d_batch, s2_batch, step):
        """Trains network to fit given parameters"""
        Q = np.zeros((self.batch_size, self.action_size))

        # Reshape frames to 1D
        input_size = self.observation_size * self.num_frames
        input_t = np.reshape(s_batch, (self.batch_size, input_size))
        input_t_1 = np.reshape(s2_batch, (self.batch_size, input_size))

        # Batch predict
        Q = self.Qmain.model.predict(input_t, batch_size = self.batch_size)
        Q1 = self.Qmain.model.predict(input_t_1, batch_size = self.batch_size)
        Q2 = self.Qtarget.model.predict(input_t_1, batch_size = self.batch_size)

        # Compute batch Qtarget using Double DQN
        for i in range(self.batch_size):
            doubleQ = Q2[i, np.argmax(Q1[i])]
            Q[i, a_batch[i]] = r_batch[i]
            if d_batch[i] == False:
                Q[i, a_batch[i]] += DISCOUNT_FACTOR * doubleQ

        # Batch train
        loss = self.Qmain.model.train_on_batch(input_t, Q)

        # Log some useful metrics every even updates
        if step % (2 * UPDATE_FREQ) == 0:
            with self.tf_writer.as_default():
                mean_reward = np.mean(self.epoch_rewards)
                mean_alive = np.mean(self.epoch_alive)
                if len(self.epoch_rewards) >= 100:
                    mean_reward_100 = np.mean(self.epoch_rewards[-100:])
                    mean_alive_100 = np.mean(self.epoch_alive[-100:])
                else:
                    mean_reward_100 = mean_reward
                    mean_alive_100 = mean_alive
                tf.summary.scalar("mean_reward", mean_reward, step)
                tf.summary.scalar("mean_alive", mean_alive, step)
                tf.summary.scalar("mean_reward_100", mean_reward_100, step)
                tf.summary.scalar("mean_alive_100", mean_alive_100, step)
                tf.summary.scalar("loss", loss, step)
            print("loss =", loss)
