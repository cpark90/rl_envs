from .random_walk import *

from gymnasium.envs.registration import register

register(
    id='random_walk-v0',
    entry_point='envs.random_walk:RandomWalkEnv',
)