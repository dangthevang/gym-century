import numpy as np
class Card:
    tt = 0
    def __init__(self,id):
        self.__id = id
        self.stt = Card.tt+1
        Card.tt = self.stt

    @property
    def id(self):
        return self.__id
    @id.setter
    def setId(self,value):
        self.__id = value

class Card_Effect(Card):
    def __init__(self,id,upgrade,stock_give_back,stock_receive):
        super().__init__(id)
        self.__upgrade = upgrade
        self.__stock_give_back = stock_give_back
        self.__stock_receive = stock_receive
    @property
    def upgrade(self):
        return  self.__upgrade
    @upgrade.setter
    def setUpgrade(self,value):
        self.__upgrade = value
    
    @property
    def stock_give_back(self):
        return self.__stock_give_back
    # @stock_give_back.setter
    # def setStockGiveBack(self,new_dict):
    #     self.__stock_give_back.update(new_dict)
    
    @property
    def stock_receive(self):
        return self.__stock_receive
    # @stock_receive.setter
    # def setStockReceive(self,new_dict):
    #     self.__stock_receive.update(new_dict)
    
class Card_Score(Card):
    def __init__(self,id,score,stock_give_back):
        super().__init__(id)
        self.__score = score
        self.__stock_buy = stock_give_back

    @property
    def score(self):
        return self.__score
    @score.setter
    def setScore(self, value):
        self.__score = value
    
    @property
    def stock_buy(self):
        return self.__stock_buy
    @stock_buy.setter
    def setStockBuy(self,new_list):
        self.__stock_buy = new_list
