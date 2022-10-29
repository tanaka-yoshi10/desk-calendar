#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import calendar
import datetime
import dateutil.parser
import pprint
import jpholiday
from subprocess import check_output

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epd')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import google_calendar

logging.basicConfig(level=logging.DEBUG)

def timestamp(mess):
    nowtime = datetime.datetime.now()
    print("{}: {}".format(mess,nowtime.strftime('%T.%f')))

def draw_date(x, y):
    nowtime = datetime.datetime.now()
    current_date = nowtime.strftime('%Y年%m月%d日(%a)')
    drawblack.text((x, y), current_date, font = font24, fill = 0)

def draw_events_title(x, y):
    drawblack.text((x + 20, y), 'Events', font = font24, fill = 0)
    drawblack.text((x, y + 5), u'📃' ,font = Symb24, fill = 0)
    drawblack.line((x, y + 35, x + 100, y + 35), fill = 0)

def draw_events(x, y, max):
    events = google_calendar.google_calendar()
    now_date = datetime.date.today()
    days = [u'月', u'火', u'水', u'木', u'金', u'土', u'日']
    for date, list in events:
        print(date.strftime('%m/%D'))
        week = days[date.weekday()]
        label = ''
        if date == now_date:
          label = ' ★今日★'
        drawblack.text((x, y), date.strftime('%m/%d') + '(' + week + ')' + label, font = font24, fill = 0)
        y += 30
        for item in list:
            print(item['start'], item['summary'])
            start = item['event']['start'].get('dateTime')
            if start:
                time = item['datetime'].strftime('%H:%M ')
                end = item['event']['end'].get('dateTime')
                end_time = dateutil.parser.parse(end).strftime('- %H:%M ')
                time = time + end_time
            else:
                time = ''
            drawblack.text((x, y + 5), u'⭐' ,font = Symb24, fill = 0)
            drawblack.text((x + 25, y), time + item['summary'], font = font24, fill = 0)
            y += 30
        y += 10

def draw_current_time(x, y):
    nowtime = datetime.datetime.now()
    drawblack.text((x, y), nowtime.strftime('%H:%M'), font = font24, fill = 0)

def draw_calendar(initial_x, initial_y):
    delta_x = 45
    delta_y = 35

    days = [u'日', u'月', u'火', u'水', u'木', u'金', u'土']
    x = initial_x
    y = initial_y
    for day in days:
        drawblack.text((  x,  initial_y), day, font = font24, fill = 0)
        x += delta_x
    y += delta_y

    nowtime = datetime.datetime.now()

    x = initial_x
    calendar.setfirstweekday(calendar.SUNDAY)
    for week in calendar.monthcalendar(nowtime.year, nowtime.month):
        for day in week:
            if day > 0:
                drawblack.text((  x,  y), str(day).rjust(2), font = font24, fill = 0)
                if day == nowtime.day:
                    drawblack.rectangle((x, y + 35, x + 25, y + 37), fill = 0)
                if jpholiday.is_holiday(datetime.date(nowtime.year, nowtime.month, day)):
                    drawblack.arc((x - 4, y, x + 29, y + 37), 0, 360, fill = 0)
            x += delta_x
        x = initial_x
        y += delta_y

    if nowtime.day <= 20:
      return
      
    next_month = (nowtime.month % 12) + 1
    for week in calendar.monthcalendar(nowtime.year, next_month):
        for day in week:
            if day > 0:
                drawblack.text((  x,  y), str(day).rjust(2), font = font24, fill = 0)
                if jpholiday.is_holiday(datetime.date(nowtime.year, next_month, day)):
                    drawblack.arc((x - 4, y, x + 29, y + 37), 0, 360, fill = 0)
            x += delta_x
        x = initial_x
        y += delta_y

font48 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 48)
font24 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
font18 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 18)
Symb48 = ImageFont.truetype('/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf', 48)
Symb24 = ImageFont.truetype('/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf', 24)
Symb18 = ImageFont.truetype('/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf', 18)

try:
    epd = epd7in5.EPD()
    logging.info("init")
    epd.init()

    timestamp("make image           ")
    HBlackimage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)  # 298*126
    #HRedimage = Image.new('1', (epd7in5bc.EPD_WIDTH, epd7in5bc.EPD_HEIGHT), 255)  # 298*126

    timestamp("Drawing              ")
    drawblack = ImageDraw.Draw(HBlackimage)
    #drawry = ImageDraw.Draw(HRedimage)

    #draw_date(50, 10)
    #draw_calendar(10, 70)
    #drawblack.line((320, 0, 320, 600), fill = 0)
    #draw_events_title(10, 5)
    draw_events(10, 5, 13)
    #draw_current_time(740, 0)

    timestamp("epd.display          ")
    #epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    epd.display(epd.getbuffer(HBlackimage))
    timestamp("epd.sleep            ")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
