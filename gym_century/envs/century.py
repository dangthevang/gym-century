import gym
import random
from gym_century.envs.base.card import Card,Card_Score,Card_Effect
from gym_century.envs.base.board import Board
from gym_century.envs.base.player import Player
from gym_century.envs.agents import interface_agent
from gym_century.envs.base import error
import numpy as np
amount_player = 4

class CenturyEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.amount_player = amount_player
        self.board = Board(amount_player)
        self.player = None
        self.state = {}

    def step(self, action):
        self.close()
        if self.End_Game == True:
            self.turn = self.turn+1
            return self,None,True,None
        else:
            if isinstance(action, int)==True:
                try:
                    action = self.player[self.turn % self.amount_player].transform(self.state,action)
                except:
                    error.errorColor("Action Khong hop le(truong hop bajn khong the lam gi khac)")
                    return self.state,None,None,None
            card = action[0]
            times = action[1]
            stocks = action[2]
            stocks_return = action[3]
            self.state["Turn"] = self.turn+1
            self.player[self.turn % self.amount_player].action_real(self.state,  card, times, stocks, stocks_return)
            self.turn = self.turn+1
            return self,None,None,None

    def reset(self):
        self.turn = 0
        self.amount_player = amount_player
        self.player = random.sample(interface_agent.createListPlayer(), k=self.amount_player)
        for p in self.player:
            p.reset()
        self.pVictory = None
        self.End_Game = False
        self.state = {
            "Turn" : 0,
            "Board": self.board,
            "Player": self.player,
            "Victory": self.pVictory
        }
        self.setup_board()

    def render(self, mode='human', close=False):
        print("Turn", self.turn," -------------------------------------------------------")
        self.board.hien_the()
        print()
        for p in self.player:
            print(p.name,p.score,p.stock,end = "   ")
            print("Card Effect",[i.id for i in p.card_effect ],end ="  " )
            print("Card used",[i.id for i in p.card_used  ],end ="  " )
            print("Card Score",[i.id for i in p.card_score  ] )
        print("--------------------------------------------------------")
    
    def setup_board(self):
        self.board.reset()
        self.board.init_board()
        self.board.setup()
        for i in range(len(self.player)):
            t = np.array([0,0,(i+1)//4,4-(i+1)//4])
            # t = [10,10,10,10]
            self.player[i].setStock(t)
            self.player[i].setCardEffeft(self.board.list_card_basic)

    def close(self):
        for p in self.player:
            if len(p.card_score) >= 6-self.amount_player//4:
                arr_point = [i.score for i in self.player]
                max = max(arr_point)
                for i in range(len(arr_point)):
                    if arr_point[i] == max:
                        self.End_Game = True
                        self.pVictory = self.player[i]
                        return
