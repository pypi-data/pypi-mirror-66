# Copyright (c) 2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of L2RPN Baselines, L2RPN Baselines a repository to host baselines for l2rpn competitions.

import numpy as np
import tensorflow as tf

from grid2op.Agent import AgentWithConverter
from grid2op.Converter import IdToAct

from ExperienceBuffer import ExperienceBuffer
from DoubleDuelingRDQN import DoubleDuelingRDQN

INITIAL_EPSILON = 0.99
FINAL_EPSILON = 0.001
DECAY_EPSILON = 1024*32
STEP_EPSILON = (INITIAL_EPSILON-FINAL_EPSILON)/DECAY_EPSILON
DISCOUNT_FACTOR = 0.99
REPLAY_BUFFER_SIZE = 4096
UPDATE_FREQ = 64
UPDATE_TARGET_HARD_FREQ = 5
UPDATE_TARGET_SOFT_TAU = 0.01

class DoubleDuelingRDQNAgent(AgentWithConverter):
    def __init__(self,
                 env,
                 action_space,
                 name=__name__,
                 trace_length=1,
                 batch_size=1,
                 is_training=False,
                 lr=1e-5):
        # Call parent constructor
        AgentWithConverter.__init__(self, action_space,
                                    action_space_converter=IdToAct)

        # Store constructor params
        self.env = env
        self.name = name
        self.trace_length = trace_length
        self.batch_size = batch_size
        self.is_training = is_training
        self.lr = lr
        
        # Declare required vars
        self.Qmain = None
        self.obs = None
        self.state = []
        self.mem_state = None
        self.carry_state = None

        # Declare training vars
        self.exp_buffer = None
        self.done = False
        self.epoch_rewards = None
        self.epoch_alive = None
        self.Qtarget = None

        # Compute dimensions from intial state
        self.obs = self.env.reset()
        self.state = self.convert_obs(self.obs)
        self.observation_size = self.state.shape[0]
        self.action_size = self.action_space.size()

        # Load network graph
        self.Qmain = DoubleDuelingRDQN(self.action_size,
                                       self.observation_size,
                                       learning_rate = self.lr)
        # Setup inital state
        self._reset_state()
        # Setup training vars if needed
        if self.is_training:
            self._init_training()


    def _init_training(self):
        self.exp_buffer = ExperienceBuffer(REPLAY_BUFFER_SIZE, self.batch_size, self.trace_length)
        self.done = True
        self.epoch_rewards = []
        self.epoch_alive = []
        self.Qtarget = DoubleDuelingRDQN(self.action_size,
                                         self.observation_size,
                                         learning_rate = self.lr)

    def _reset_state(self):
        # Initial state
        self.obs = self.env.current_obs
        self.state = self.convert_obs(self.obs)
        self.done = False
        self.mem_state = np.zeros(self.Qmain.h_size)
        self.carry_state = np.zeros(self.Qmain.h_size)

    def _register_experience(self, episode_exp, episode):
        missing_obs = self.trace_length - len(episode_exp)

        if missing_obs > 0: # We are missing exp to make a trace
            exp = episode_exp[0] # Use inital state to fill out
            for missing in range(missing_obs):
                # Use do_nothing action at index 0
                self.exp_buffer.add(exp[0], 0, exp[2], exp[3], exp[4], episode)

        # Register the actual experience
        for exp in episode_exp:
            self.exp_buffer.add(exp[0], exp[1], exp[2], exp[3], exp[4], episode)

    def _save_hyperparameters(self):
        r_instance = self.env.reward_helper.template_reward
        hp = {
            "lr": self.lr,
            "batch_size": self.batch_size,
            "trace_len": self.trace_length,
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
        return observation.to_vect()

    def convert_act(self, action):
        return super().convert_act(action)

    def reset(self):
        self._reset_state()

    def my_act(self, state, reward, done=False):
        data_input = np.array(state)
        data_input.reshape(1, 1, self.observation_size)
        self.Qmain.trace_length.assign(1)
        self.Qmain.dropout_rate.assign(0.0)
        a, _, m, c = self.Qmain.predict_move(data_input, self.mem_state, self.carry_state)
        self.mem_state = m
        self.carry_state = c

        return a
    
    def load_network(self, path):
        self.Qmain.load_network(path)
        if self.is_training:
            self.Qmain.update_target_hard(self.Qtarget.model)

    def save_network(self, path):
        self.Qmain.save_network(path)

    ## Training Procedure
    def train(self, num_pre_training_steps, num_training_steps):
        # Loop vars
        num_steps = num_pre_training_steps + num_training_steps
        step = 0
        epsilon = INITIAL_EPSILON
        alive_steps = 0
        total_reward = 0
        episode = 0
        episode_exp = []

        self.tf_writer = tf.summary.create_file_writer("./logs/{}".format(self.name), name=self.name)
        self._save_hyperparameters()
        
        self._reset_state()
        # Training loop
        while step < num_steps:
            # New episode
            if self.done:
                self.env.reset() # This shouldn't raise
                self._reset_state()
                # Push current episode experience to experience buffer
                self._register_experience(episode_exp, episode)
                # Reset current episode experience
                episode += 1
                episode_exp = []

            if step % 1000 == 0:
                print("Step [{}] -- Random [{}]".format(step, epsilon))

            # Choose an action
            if step <= num_pre_training_steps:
                a, m, c = self.Qmain.random_move(self.state, self.mem_state, self.carry_state)
            else:
                a, _, m, c = self.Qmain.bayesian_move(self.state, self.mem_state, self.carry_state, epsilon)

            # Update LSTM state
            self.mem_state = m
            self.carry_state = c

            # Convert it to a valid action
            act = self.convert_act(a)
            # Execute action
            new_obs, reward, self.done, info = self.env.step(act)
            new_state = self.convert_obs(new_obs)
            
            # Save to current episode experience
            episode_exp.append((self.state, a, reward, self.done, new_state))

            # Train when pre-training is over
            if step > num_pre_training_steps:
                # Slowly decay dropout rate
                if epsilon > FINAL_EPSILON:
                    epsilon -= STEP_EPSILON
                if epsilon < 0.0:
                    epsilon = 0.0

                # Perform training at given frequency
                if step % UPDATE_FREQ == 0 and self.exp_buffer.can_sample():
                    # Sample from experience buffer
                    batch = self.exp_buffer.sample()
                    # Perform training
                    training_step = step - num_pre_training_steps
                    self._batch_train(batch, training_step)
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

    def _batch_train(self, batch, step):
        """Trains network to fit given parameters"""
        Q = np.zeros((self.batch_size, self.action_size))
        batch_mem = np.zeros((self.batch_size, self.Qmain.h_size))
        batch_carry = np.zeros((self.batch_size, self.Qmain.h_size))

        input_size = self.observation_size
        m_data = np.vstack(batch[:, 0])
        m_data = m_data.reshape(self.batch_size, self.trace_length, input_size)
        t_data = np.reshape(np.vstack(batch[:, 4]), [self.batch_size, self.trace_length, input_size])
        t_data = t_data.reshape(self.batch_size, self.trace_length, input_size)
        m_input = [batch_mem, batch_carry, m_data]
        t_input = [batch_mem, batch_carry, t_data]

        # Batch predict
        self.Qmain.trace_length.assign(self.trace_length)
        self.Qmain.dropout_rate.assign(0.0)
        self.Qtarget.trace_length.assign(self.trace_length)
        self.Qtarget.dropout_rate.assign(0.0)

        Q, _, _ = self.Qmain.model.predict(m_input, batch_size = self.batch_size)
        Q1, _, _ = self.Qmain.model.predict(t_input, batch_size = self.batch_size)
        Q2, _, _ = self.Qtarget.model.predict(t_input, batch_size = self.batch_size)

        # Compute batch Double Q update to Qtarget
        for i in range(self.batch_size):
            idx = i * (self.trace_length - 1)
            doubleQ = Q2[i, np.argmax(Q1[i])]
            a = batch[idx][1]
            r = batch[idx][2]
            d = batch[idx][3]
            Q[i, a] = r
            if d == False:
                Q[i, a] += DISCOUNT_FACTOR * doubleQ

        # Batch train
        batch_x = [batch_mem, batch_carry, m_data]
        batch_y = [Q, batch_mem, batch_carry]
        loss = self.Qmain.model.train_on_batch(batch_x, batch_y)
        loss = loss[0]

        # Log some useful metrics
        print("loss =", loss)
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
