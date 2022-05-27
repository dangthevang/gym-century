from gym.envs.registration import register

register(
    id='gym_century-v0',    
    entry_point='gym_century.envs:CenturyEnv',
)