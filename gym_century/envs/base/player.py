from re import S

import numpy as np
from gym_century.envs.base import error


class Player():
    tt = 0
    def __init__(self, name):
        self.name = name
        self.__stt = Player.tt+1
        Player.tt = self.__stt
        self.reset

    def reset(self):
        self.__score = 0

        # B-G-R-Y
        self.__coin = [0,0]
        self.__stock = []
        self.__card_effect = []
        self.__card_used = []
        self.__card_score = []
    @property
    def score(self):
        return  self.__score
    @score.setter
    def setScore(self,value):
        self.__score = value
    
    @property
    def coin(self):
        return  self.__coin
    @coin.setter
    def setCoin(self,value):
        self.__coin = value

    @property
    def stock(self):
        return self.__stock
    # @stock.setter
    def setStock(self,value):
        self.__stock = value

    @property
    def card_effect(self):
        return self.__card_effect
    # @card_effect.setter
    def setCardEffeft(self,value):
        self.__card_effect= value
    @property
    def card_used(self):
        return self.__card_used
    @property
    def card_score(self):
        return self.__card_score

    def action_real(self, state,  card=None, times=1, stocks=[], stocks_return=[]):
        if card == None:
            self.ResetListCard()
            return
        
        position = self.GetPositionCard(state, card)
        if position[0] == False and position[1] == False:
            self.GetCardCardEffect(state, card, stocks, stocks_return)
            return
        elif position[0] == False and position[1] == True:
            self.GetCardScore(state, card)
            return
        elif position[0] == True and position[1] == False:
            self.UseCardEffect(state, card, times, stocks, stocks_return)
            return

    def ResetListCard(self):
        for card in self.__card_used:
            self.__card_effect.append(card)
            self.__card_used.remove(card)

    def ReturnStock(self, stocks_return):
        self.__stock = self.__stock - stocks_return

    def CheckReturnStock(self, stocks, stock_return):
        if sum(self.__stock+stocks) > 10:
            arr = self.__stock+stocks-stock_return
            for i in arr:
                if i < 0:
                    return False
        return True

    def GetStock(self, stocks, stocks_return):
        if self.CheckReturnStock(stocks, stocks_return):
            self.__stock = self.__stock + stocks
            if sum(self.__stock) >10:
                self.ReturnStock(stocks_return)

    def CheckGetCardScore(self, card):
        for stock in range(len(card.stock_buy)):
            if card.stock_buy[stock] > self.__stock[stock]:
                return False
        return True

    def GetCardScore(self, state, card):
        position = self.GetPositionCard(state, card)
        if position[0] == True:
            error.RecommendColor("The "+str(card.id) +
                                 " da duoc ban lay tu cac turn truoc do roi")
        else:
            index = position[3]
            if self.CheckGetCardScore(card):
                self.__card_score.append(card)
                try:
                    if state["Board"].dict_Card_Stocks_Show["Coin"][index] >0:
                        self.__coin[index] +=1
                        self.__score+=(1-index)*2+1
                except:
                    pass
                self.__score += card.score
                self.ReturnStock(card.stock_buy)
                state["Board"].UpdateListCardScore(card,position[3])
            else:
                error.RecommendColor(
                    "Ban dang yeu cau lay the"+str(card.id)+" diem du ban khong du nguyen lieu")
    def GiveBackForGetCard(self,stocks_return,index):
        stock_for_board = np.array([0,0,0,0])
        for stock in range(len(stocks_return)-1,-1,-1):
            while index >0 and stocks_return[stock] != 0:
                stock_for_board[stock] +=1
                stocks_return[stock] -=1
                index -=1
        return stock_for_board

    def CheckGetCardEffect(self, index,stocks,stocks_return):
        stock_for_board = self.GiveBackForGetCard(stocks_return,index)
        for i in self.stock-stock_for_board:
            if i <0:
                return False
        if sum(self.stock + stocks - stocks_return) >10:
            return False
        return True

    def GetCardCardEffect(self, state, card, stocks, stocks_return):
        position = self.GetPositionCard(state, card)
        if position[0] == True:
            error.RecommendColor("The "+str(card.id) +
                                 " da duoc ban lay tu cac turn truoc do roi")
        else:
            index = position[3]
            stock_receive = state["Board"].dict_Card_Stocks_Show["Stock"][index]
            if self.CheckGetCardEffect(index,stock_receive, stocks_return.copy()):
                stock_for_board = self.GiveBackForGetCard(stocks_return.copy(),index)
                self.__stock = self.__stock + stock_receive
                if sum(self.stock) > 10:
                    self.ReturnStock(stocks_return)
                else:
                    self.ReturnStock(stock_for_board)
                # print(stock_for_board)
                state["Board"].UpdateListCardEffect(index, stock_for_board)
                self.__card_effect.append(card)
            else:
                error.RecommendColor("Ban dang yeu cau lay the"+str(card.id) +
                                     " diem du ban khong du nguyen lieu hoac tra nguyen lieu chua dung")

    def CheckUseCardEffect(self, state, card, times, stocks, stocks_return):
        position = self.GetPositionCard(state, card)
        if position[0] == False:
            error.errorColor("Ban chua so huu the"+card.id)
            return False
        else:
            type_ = 0
            if card.upgrade == 0:
                stock_curent = self.stock
                stock_give_back = card.stock_give_back
                stock_receive = card.stock_receive
                if sum(stock_give_back) != 0:
                    for index in range(len(stock_curent)):
                        if stock_curent[index] < stock_give_back[index]*times:
                            error.errorColor("So lan su dung qua muc cho phep")
                            return False
                else:
                    times = 1
                return self.CheckReturnStock(stock_receive*times, stock_give_back*times +stocks_return), type_
            else:
                type_ = 1
                build = 0
                if sum(stocks) != sum(stocks_return):
                    return False,type_
                for i in range(1,len(stocks)):
                    build += stocks_return[i-1]*i - stocks[i-1]*i
                if build>=card.upgrade:
                    return False,type_
                return True,type_


    def UseCardEffect(self, state, card, times,stocks, stocks_return):
        check, t = self.CheckUseCardEffect(state, card, times, stocks, stocks_return)
        if check == True:
            if sum(card.stock_give_back) == 0:
                times = 1
            if t == 0:
                self.__stock = self.__stock + card.stock_receive*times - card.stock_give_back*times
                if sum(self.__stock) >10:
                    self.ReturnStock(stocks_return)
            else:
                self.__stock = self.__stock + stocks - stocks_return
            self.__card_used.append(card)
            self.__card_effect.remove(card)
        else:
            error.errorColor("Loi khong su dung duoc the "+str(card.id))

    def GetPositionCard(self, state, card):
        '''return mine: Boolean, cardscore: Boolean, used: Boolean, [index]'''
        for key in state["Board"].dict_Card_Stocks_Show.keys():
            index = 0
            for c in state["Board"].dict_Card_Stocks_Show[key]:
                if key.find("Card")!=-1:
                    if card.id == c.id:
                        if key == "Card_Score":
                            return False, True, False, index
                        else:
                            return False, False, False, index
                    index += 1
        for c in self.__card_effect:
            if card.id == c.id:
                return True, False, False
        for c in self.__card_used:
            if card.id == c.id:
                return True, False, True
        for c in self.__card_score:
            if card.id == c.id:
                return True, True, True
        error.errorColor("The" + str(card.id) +
                         " chua xuat hien tren ban hoac da duoc nguoi khac su dung!!!!")
