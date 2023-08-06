# Copyright (c) 2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of L2RPN Baselines, L2RPN Baselines a repository to host baselines for l2rpn competitions.

import numpy as np

from grid2op.Reward.BaseReward import BaseReward


class LinesReconnectedReward(BaseReward):
    """
    This reward computes a penalty
    based on the number of off cooldown disconnected lines
    """
    def __init__(self):
        BaseReward.__init__(self)
        self.reward_min = 0.0
        self.reward_max = 1.0
        self.penalty_max_at_n_lines = 2.0

    def __call__(self, action, env, has_error,
                 is_done, is_illegal, is_ambiguous):
        # Get obs from env
        obs = env.current_obs

        # All lines ids
        lines_id = np.array(list(range(env.n_line)))
        # Only off cooldown lines
        lines_off_cooldown = lines_id[
            np.logical_and(
                (obs.time_before_cooldown_line <= 0), # Can be acted on
                (obs.time_before_line_reconnectable <= 0) # Can be reconnected
            )
        ]

        n_penalties = 0.0
        for line_id in lines_off_cooldown:
            # Line could be reconnected but isn't
            if obs.line_status[line_id] == False:
                n_penalties += 1.0

        max_p = self.penalty_max_at_n_lines
        n_penalties = max(max_p, n_penalties)
        r = np.interp(n_penalties, [0.0, max_p],
                      [self.reward_max, self.reward_min])
        return r
