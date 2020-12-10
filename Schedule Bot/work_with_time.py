from datetime import datetime
import telebot
from config_second import get_tok
from telebot import types
from wr_to_file import Filehelper

class TimeCount:
    def __init__(self):
        self.bot = telebot.TeleBot(get_tok())
        self.lst = {
            0:((16,56),),
            1:((11,40),),
            2:((22,45),(13,20)),
            3:((11,40),(13,20),(15,30),(21,30)),
            4:((11,40),(13,20),(12,30))
            #5:((19,31),(19,4),(19,5),(19,6))
            }
        self.lst_of_deadline = Filehelper.file_get('./deadlines_kr.txt')
        self.per = 0
        self.per_for_cond = True
        self.per_for_weekend_cond = True
        self.reset_time_per = False
        self.main_alg()
        
    def main_alg(self):
        while True:
            #print(self.reset_time_per)
            if self.per_for_cond and self.per_for_weekend_cond:
                self.check_evday_time()
            if self.reset_time_per:
                #print('work')
                self.reset()
            self.check_kr_deadlines()
                
    def check_evday_time(self):        
        now = datetime.now()
        #print(self.lst[now.weekday()][self.per][1])
        if now.weekday() != 6:
            try:
                if now.hour == self.lst[now.weekday()][self.per][0] and now.minute == self.lst[now.weekday()][self.per][1]:
                    #print('123131')
                    if now.hour == 15 and now.minute == 39:
                        #print('234232')
                        if now.weekday() == 0:
                            self.send_to_all('Пора скинуть алгем')
                        if now.weekday() == 4:
                            self.send_to_all('Пора скинуть матан')
                        self.per += 1
                    else:
                        #print('dewdewdew')
                        self.send_to_all('Пора спать орк, завтра с Альянсом битва')
                        self.per += 1 
            except:
                self.per_for_cond = False
                self.reset_time_per = True
                #print('ошибка')
        else:
            self.per_for_weekend_cond = False
            self.reset_time_per = True

    def check_kr_deadlines(self):
        now = datetime.now()
        #print('check')
        
        for i in self.lst_of_deadline:
            try:
                for ii, jj in i.items():
                    if now.hour == ii.hour and now.minute == ii.minute:
                        self.send_to_all('пора бы подготовиться к {0}'.format(jj[6:]))
            except:
                pass

    def send_to_all(self, per):      #187465541 - Рафа
        data = Filehelper.file_get('./id_list.txt')        
        for i in data:
            self.bot.send_message(i,per)
        

    def reset(self):
        now = datetime.now()
        if now.hour == 23 and now.minute == 59:
            self.per_for_cond = True
            self.per_for_weekend_cond = True
            self.reset_time_per = False
            data = Filehelper.file_get('./deadlines_kr.txt')
            self.lst_of_deadline = data