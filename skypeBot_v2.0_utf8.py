#!/bin/env python
# -*- coding: utf-8 -*-

import Skype4Py
import sys
import time
import datetime
from json import load
from urllib2 import urlopen
from optparse import OptionParser
import random
import calendar

def weather_funk():

   weather_data = urlopen('http://openweathermap.org/data/2.1/find/name?q=kiev')
   j = load(weather_data)
   if j['count'] > 0:
      city = str(j['list'][0]['name']) + '\n'
      temp = j['list'][0]['main']['temp'] - 272.15
      temp_str = "Temp: " + str("%.2f" %temp) + '\n'
      sky = str(j['list'][0]['weather'][0]['description']) + '\n'
      url = str(j['list'][0]['url']) + '\n'
      weather_msg =city + temp_str + sky + url

   curency_data = urlopen('http://rate-exchange.appspot.com/currency?from=USD&to=UAH')
   j = load(curency_data)
   curency_msg = '\nFrom %s to %s rate %f' % (j[u"from"], j[u"to"], j[u"rate"])
   msg = weather_msg + curency_msg
      
   return msg
   

def find_chat(s, chat_topic='Flood SUPPORT'):

   for chat in range(len(s.Chats)):
      if s.Chats[chat].Type == "MULTICHAT" and s.Chats[chat].Topic == chat_topic:
         chat_num = chat
         break
   return chat_num

def week_day():

   now = datetime.datetime.now()
   day_name = now.strftime("%a")
   return day_name

def last_monday():

   cal = calendar.Calendar(0)
   month = cal.monthdatescalendar(datetime.datetime.now().year, datetime.datetime.now().month)
   lastweek = month[-1]
   monday = lastweek[0]
   if str(monday) == str(datetime.datetime.now().strftime('%Y-%m-%d')):
      is_last = True
   else:
      is_last = False

   return is_last

def send_message(s, msg=None, chat_name='Flood SUPPORT'):

   if msg is None:
      msg = 'No message. Why?'

   chatID = find_chat(s, chat_name)
   s.Chats[chatID].SendMessage(msg)
   for count in range(220):
      last_mess = s.Chats[chatID].Messages[0].Body
      if last_mess == u'дякую' or last_mess == u'спасибо' or last_mess == 'thanks':
        rand = random.randint(0, 2)
        chatID = find_chat(s)
        if rand == 0:
           s.Chats[chatID].SendMessage("Пожалуйста повелитель :)")
        elif rand == 1:
           s.Chats[chatID].SendMessage("Кинь лучше 10грн на 0936361474 :)")
        elif rand == 2:
           s.Chats[chatID].SendMessage("Спасибо в карман не положишь :)")
        break
      else:
        time.sleep(1)


def main():

    s = Skype4Py.Skype()
    s.Attach()

    usage = "usage: %prog [options] [msg] [chat topic]"
    parser = OptionParser(usage)

    parser.add_option("-m", "--message", dest="message",
                      help="send 'message' to the chat", metavar="'msg_text'")
    parser.add_option("-c", "--chat-topic", dest="topic",
                      help="chat topic", metavar="'topic'")
    parser.add_option("-f", "--friday",
                  action="store_true", dest="friday", default=False, help="friday message")
    parser.add_option("-w", "--weather", action="store_true", dest="weather",
                      default=False, help="message about weather")

    (options, args) = parser.parse_args()
    if options.message:
        if options.topic:
           print "sending '%s' to %s"  % (options.message, options.topic)
           send_message(s, options.message, options.topic)
        else:
           send_message(s, options.message)
    if options.friday:
        msg = '''Всем привет.
:)
Сегодня пятница, а это значит, что пора внести потраченное на выполнение работы время в Project Server.
Ваш покорный слуга Бот помнит об этом и никогда не устанет напоминать :)
!!!Project Server!!!'''
        send_message(s, msg)

    if options.weather:
        msg = weather_funk()
        send_message(s, msg)
        
    if last_monday():
        msg = '''Кстати, сегодня последний понедельник этого месяца.
        Забукайте время :)'''
        send_message(s, msg)


if __name__ == "__main__":
    print 'Hello'
    sys.exit(main())
