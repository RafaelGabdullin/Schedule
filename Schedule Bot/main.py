import telebot
import config
from datetime import timedelta, datetime
from telebot import types
from config import Helper
from config_second import get_tok
from datetime import datetime
import threading
from work_with_time import TimeCount
from wr_to_file import Filehelper
from deadline_wr_to_file import DeadlineWriter
import pickle
  	
bot = telebot.TeleBot(get_tok())#777288479
today = datetime.now()

def main_thred_func():
    tim = TimeCount()


x = threading.Thread(target=main_thred_func)
x.start()
class Bottele:

    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id,'\com - общая команда\n\com_kr - запись новой контрольной на сл неделю\n\com_hw_{} - запись дз\n(m - матан,a - алгем,d - дискретка,h - история)' )
    
    @bot.message_handler(commands=['start']) 
    def start_tr(message):
        data = Filehelper.file_get('./id_list.txt')
        if message.chat.id not in data:
            data.append(message.chat.id)
            Filehelper.file_wr(data,'./id_list.txt')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_1 = types.KeyboardButton("Расписание 📖")
        item_2 = types.KeyboardButton("Домашние задания 📊")
        item_3 = types.KeyboardButton("Сроки контрольных 🧨")
        item_4 = types.KeyboardButton("Зачеты/Экзамены 🤯")
        markup.add(item_1, item_2, item_3, item_4)

        bot.send_message(message.chat.id,'Привет 🤚', reply_markup=markup)
        #bot.send_message(message.chat.id,str(message.chat.id))


    @bot.message_handler(content_types=['text'])
    def start(message):
        if message.text[:4] != '\com':
            
            if message.chat.type == 'private':
                if message.text == "Расписание 📖":
                    keyboard = types.InlineKeyboardMarkup()
                    item_1_0 = types.InlineKeyboardButton("Понедельник", callback_data='monday')
                    item_1_1 = types.InlineKeyboardButton("Вторник", callback_data='tuesday')
                    item_1_2 = types.InlineKeyboardButton("Среда", callback_data='wednesday')
                    item_1_3 = types.InlineKeyboardButton("Четверг", callback_data='thursday')
                    item_1_4 = types.InlineKeyboardButton("Пятница", callback_data='friday')

                    keyboard.add(item_1_0, item_1_1, item_1_2, item_1_3, item_1_4)
                    bot.send_message(message.chat.id, "Выбери день недели:", reply_markup=keyboard)
                if message.text == "Домашние задания 📊":
                    bot.send_message(message.chat.id, Helper.homework_prepair())
                    
                if message.text == "Сроки контрольных 🧨":                   
                    data = Helper.kr_deadlines()
                    bot.send_message(message.chat.id, data)
                        
                if message.text == "Зачеты/Экзамены 🤯":
                    bot.send_message(message.chat.id, exams())
            if message.chat.type == '/wr':
                bot.send_message(message.chat.id, "Команда")
        else:
            if '\com_kr' in message.text:
                DeadlineWriter.wrk_with_text_deadline_kr(message.text)
            elif '\com_hw_m' in message.text:
                DeadlineWriter.wrk_with_text_deadline_hw_m(message.text)
            elif '\com_hw_a' in message.text:
                DeadlineWriter.wrk_with_text_deadline_hw_a(message.text)
            elif '\com_hw_d' in message.text:
                DeadlineWriter.wrk_with_text_deadline_hw_d(message.text)
            elif '\com_hw_h' in message.text:
                DeadlineWriter.wrk_with_text_deadline_hw_h(message.text)

    @bot.callback_query_handler(func=lambda call: True)
    def one_two(call):
        if call.message:
            if call.data == 'monday':
                bot.send_message(call.message.chat.id, Helper.monday())
            if call.data == 'tuesday':
                bot.send_message(call.message.chat.id, Helper.tuesday())
            if call.data == 'wednesday':
                bot.send_message(call.message.chat.id, Helper.wednesday())
            if call.data == 'thursday':
                bot.send_message(call.message.chat.id, Helper.thursday())
            if call.data == 'friday':
                bot.send_message(call.message.chat.id, Helper.friday())
                

                        
bot.polling(none_stop=True)
