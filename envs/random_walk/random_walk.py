import sys
from six import StringIO
from string import ascii_uppercase
from typing import Optional

import numpy as np

import gymnasium as gym
from gymnasium import spaces, utils
from gymnasium.envs.toy_text.utils import categorical_sample


WEST, EAST = 0, 1


class RandomWalkEnv(gym.Env):

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, n_states=7, p_stay=0.0, p_backward=0.5, n_actions=2):

        # two terminal states added
        self.shape = (1, n_states + 2)

        # initial state is mid point
        self.start_state_index = self.shape[1] // 2

        self.number_of_state = number_of_state = np.prod(self.shape)
        self.number_of_action = number_of_action = n_actions

        self.model = {}
        for state in range(number_of_state):
            self.model[state] = {}
            for action in range(number_of_action):
                p_forward = 1.0 - p_stay - p_backward

                s_forward = np.clip(state - 1 if action == WEST else state + 1, 0, number_of_state - 1) if state != 0 and state != number_of_state - 1 else state
                s_backward = np.clip(state + 1 if action == WEST else state - 1, 0, number_of_state - 1) if state != 0 and state != number_of_state - 1 else state

                r_forward = 1.0 if state == number_of_state - 2 and s_forward == number_of_state - 1 else 0.0
                r_backward = 1.0 if state == number_of_state - 2 and s_backward == number_of_state - 1 else 0.0

                d_forward = state >= number_of_state - 2 and s_forward == number_of_state - 1 or state <= 1 and s_forward == 0
                d_backward = state >= number_of_state - 2 and s_backward == number_of_state - 1 or state <= 1 and s_backward == 0

                self.model[state][action] = [
                    (p_forward, s_forward, r_forward, d_forward),
                    (p_stay, state, 0.0, state == number_of_state - 1 or state == 0),
                    (p_backward, s_backward, r_backward, d_backward)
                ]

        self.isd = np.zeros(number_of_state)
        self.isd[self.start_state_index] = 1.0
        self.lastaction = None # for rendering

        self.action_space = spaces.Discrete(self.number_of_action)
        self.observation_space = spaces.Discrete(self.number_of_state)

        self.current_state = categorical_sample(self.isd, self.np_random)

    def step(self, action):
        transitions = self.model[self.current_state][action]
        i = categorical_sample([t[0] for t in transitions], self.np_random)
        p, state, r, d = transitions[i]
        self.current_state = state
        self.lastaction = action
        return (int(state), r, d, {"prob": p})

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        self.current_state = categorical_sample(self.isd, self.np_random)
        self.lastaction = None
        return int(self.current_state)

    def render(self, mode='human', close=False):
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        desc = np.asarray(['[' + ascii_uppercase[:self.shape[1] - 2] + ']'], dtype='c').tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        color = 'red' if self.current_state == 0 else 'green' if self.current_state == self.number_of_state - 1 else 'yellow'
        desc[0][self.current_state] = utils.colorize(desc[0][self.current_state], color, highlight=True)
        outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc)+"\n")

        if mode != 'human':
            return outfile