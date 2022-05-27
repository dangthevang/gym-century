import copy
from gym_century.envs.base import error
from gym_century.envs.base.card  import Card_Effect,Card_Score
import numpy as np
import pandas as pd
import json
import copy
import random
def formatList(s):
    s = s.split(",")
    arr = []
    for i in s:
        arr.append(int(i))
    return np.array(arr)
class Board:
    def __init__(self,amount_player):
        self.name = "Board"
        self.__player = amount_player
        self.reset()
        
    def reset(self):
        self.__list_card_basic = []
        # self.max_init_stock = 7
        self.__dict_Card_Stocks_Show = {
            "Coin":[self.__player*2,self.__player*2],
            'Card_Score': [],
            'Card_Effect': [],
            "Stock" : np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        }
        self.__dict_Card_Stocks_UpsiteDown = {
            'Card_Score': [],
            'Card_Effect': []
        }
    @property
    def list_card_basic(self):
        return self.__list_card_basic.copy()
    @list_card_basic.setter
    def setListCardBasic(self, value):
        self.__list_card_basic = value

    @property
    def dict_Card_Stocks_Show(self):
        return copy.deepcopy(self.__dict_Card_Stocks_Show)
    @dict_Card_Stocks_Show.setter
    def setDict_Card_Stocks_Show(self,new_dict):
        self.__dict_Card_Stocks_Show.update(new_dict)


    @property
    def dict_Card_Stocks_UpsiteDown(self):
        return  copy.deepcopy(self.__dict_Card_Stocks_UpsiteDown)
    @dict_Card_Stocks_UpsiteDown.setter
    def setDict_Card_Stocks_UpsiteDown(self,new_dict):
        self.__dict_Card_Stocks_UpsiteDown.update(new_dict)

    def deleteCardInUpsiteDown(self, key, card_stock):
        try:
            self.__dict_Card_Stocks_UpsiteDown[key].remove(card_stock)
        except:
            pass      

    def appendUpCard(self, key, card_stock):
        try:
            self.__dict_Card_Stocks_Show[key].append(card_stock)
            self.deleteCardInUpsiteDown(key, card_stock)
        except:
            error.RecommendColor("Hết thẻ rồi, Không thêm nguyên liệu được nữa đâu")
    
    def deleteUpCard(self, key, card_stock):
        try:
            a = self.__dict_Card_Stocks_UpsiteDown[key][0]
        except:
            a = None
        if a != None:
            self.__dict_Card_Stocks_Show[key] = [a if i.id == card_stock.id else i for i in self.__dict_Card_Stocks_Show[key] ]
            self.deleteCardInUpsiteDown(key,a)
        else:
            card = self.equal(card_stock,key)
            self.__dict_Card_Stocks_Show[key].remove(card)

    def init_board(self):
        self.reset()
        with open('gym_century/envs/data/card.json') as datafile:
            data = json.load(datafile)
        for id_Card in data:
            card = data[id_Card]
            if card["Type"] == "B":
                A = Card_Effect(id_Card,int(card["UG"]),formatList(card["GB"]),formatList(card["RC"]))
                self.__list_card_basic.append(A)
            if card["Type"] == "G":
                A = Card_Effect(id_Card,int(card["UG"]),formatList(card["GB"]),formatList(card["RC"]))
                self.__dict_Card_Stocks_UpsiteDown["Card_Effect"].append(A)
            if card["Type"] == "S":
                A = Card_Score(id_Card,int(card["Score"]),formatList(card["GB"]))
                self.__dict_Card_Stocks_UpsiteDown["Card_Score"].append(A)
    def setup(self):
        for i in self.__dict_Card_Stocks_UpsiteDown.keys():
            random.shuffle(self.__dict_Card_Stocks_UpsiteDown[i])
        for key in self.__dict_Card_Stocks_UpsiteDown.keys():
            for i in range(5):
                self.__dict_Card_Stocks_Show[key].append(self.__dict_Card_Stocks_UpsiteDown[key][0])
                self.__dict_Card_Stocks_UpsiteDown[key].remove(self.__dict_Card_Stocks_UpsiteDown[key][0])
        self.__dict_Card_Stocks_Show["Card_Effect"].append(self.__dict_Card_Stocks_UpsiteDown["Card_Effect"][0])
        self.__dict_Card_Stocks_UpsiteDown["Card_Effect"].remove(self.__dict_Card_Stocks_UpsiteDown["Card_Effect"][0])

    def UpdateListCardScore(self,card,index):
        try:
            self.__dict_Card_Stocks_Show["Coin"][index] -=1
        except:
            pass
        card = self.__dict_Card_Stocks_Show["Card_Score"][index]
        self.__dict_Card_Stocks_Show["Card_Score"].remove(card)
        self.__dict_Card_Stocks_Show["Card_Score"].append(self.__dict_Card_Stocks_UpsiteDown["Card_Score"][0])
        self.__dict_Card_Stocks_UpsiteDown["Card_Score"].remove(self.__dict_Card_Stocks_UpsiteDown["Card_Score"][0])
    
    def UpdateListCardEffect(self,index,stocks):
        A = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        index_current = 0
        for i in range(len(stocks)-1,-1,-1):
            n = stocks[i]
            while n >0:
                B = np.array([0,0,0,0])
                B[i] = 1
                A[index_current] = A[index_current]+B
                n -= 1
                index_current +=1
        card = self.__dict_Card_Stocks_Show["Card_Effect"][index]
        self.__dict_Card_Stocks_Show["Stock"] = np.delete(self.__dict_Card_Stocks_Show["Stock"], index, 0)
        self.__dict_Card_Stocks_Show["Stock"] = np.concatenate((self.__dict_Card_Stocks_Show["Stock"], [np.array([0,0,0,0])]))
        self.__dict_Card_Stocks_Show["Stock"] = self.__dict_Card_Stocks_Show["Stock"] + A
        self.__dict_Card_Stocks_Show["Card_Effect"].remove(card)
        self.__dict_Card_Stocks_Show["Card_Effect"].append(self.__dict_Card_Stocks_UpsiteDown["Card_Effect"][0])
        self.__dict_Card_Stocks_UpsiteDown["Card_Effect"].remove(self.__dict_Card_Stocks_UpsiteDown["Card_Effect"][0])
    
    def hien_the(self):
        for i in self.__dict_Card_Stocks_Show.keys():
            if len(i) >5:
                print(i,end=":    ")
                for j in self.__dict_Card_Stocks_Show[i]:
                    print(j.stt-1, end="            ")
                print()
            else:
                print(i,end=":      ")
                for j in self.__dict_Card_Stocks_Show[i]:
                    print(j, end="     ")
                print()

# B = Board(4)
# B.init_board()
# B.setup()
# B.hien_the()