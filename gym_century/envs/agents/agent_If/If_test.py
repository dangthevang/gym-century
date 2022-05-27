from ...base.player import Player
import random
import math


class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def action(self,  state):
        # try:
        card = state["Board"].dict_Card_Stocks_Show["Card_Score"][3]
        # print(card)
        # except:
        #     card = None
        times = 1
        stocks = [0,0,0,0]
        stocks_return = [0,0,0,3]
        return  card,times,stocks, stocks_return
