import gym
import gym_century
import pandas as pd
import time

env = gym.make('gym_century-v0')
def main():
    env.reset() 
    start_time = time.time()
    while env.turn <100:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if done == True:
            break
    for i in range(4):
        # print(env.turn//4)
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
    print(env.pVictory)
    print(time.time()-start_time)
if __name__ == '__main__':
    main()