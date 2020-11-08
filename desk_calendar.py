#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import calendar
import datetime
import pprint
from subprocess import check_output

#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epd')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import google_calendar_2

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

def draw_events(x, y):
    list = google_calendar_2.google_calendar()[:10]
    for item in list:
        print(item['start'], item['summary'])
        start = item['event']['start'].get('dateTime')
        if start:
            time = item['date'].strftime('%m-%d %H:%M ')
        else:
            time = item['date'].strftime('%m-%d ')
        drawblack.text((x, y), time + item['summary'], font = font24, fill = 0)
        y += 30

def draw_current_time(x, y):
    nowtime = datetime.datetime.now()
    drawblack.text((x, y), nowtime.strftime('%H:%M'), font = font24, fill = 0)

def draw_calendar(initial_x, initial_y):
    delta_x = 60
    delta_y = 40

    days = [u'月', u'火', u'水', u'木', u'金', u'土', u'日']
    x = initial_x
    y = initial_y
    for day in days:
        drawblack.text((  x,  initial_y), day, font = font24, fill = 0)
        x += delta_x
    y += delta_y

    nowtime = datetime.datetime.now()

    x = initial_x
    pprint.pprint(calendar.monthcalendar(nowtime.year, nowtime.month))
    for week in calendar.monthcalendar(nowtime.year, nowtime.month):
        for day in week:
            if day > 0:
                drawblack.text((  x,  y), str(day).rjust(2), font = font24, fill = 0)
            x += delta_x
        x = initial_x
        y += delta_y

font48 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 48)
font24 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
Symb48 = ImageFont.truetype('/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf', 48)
Symb24 = ImageFont.truetype('/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf', 24)

try:
    epd = epd7in5_V2.EPD()
    logging.info("init")
    epd.init()

    timestamp("make image           ")
    HBlackimage = Image.new('1', (epd7in5_V2.EPD_WIDTH, epd7in5_V2.EPD_HEIGHT), 255)  # 298*126

    timestamp("Drawing              ")
    drawblack = ImageDraw.Draw(HBlackimage)

    draw_date(80, 10)
    draw_calendar(20, 70)
    drawblack.line((420, 0, 420, 600), fill = 0)
    draw_events_title(430, 5)
    draw_events(430, 45)
    draw_current_time(740, 450)

    timestamp("epd.display          ")
    epd.display(epd.getbuffer(HBlackimage))
    timestamp("epd.sleep            ")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()