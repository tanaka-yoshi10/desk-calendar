#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import calendar
import datetime
import pprint
import jpholiday
from subprocess import check_output

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'epd')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd7in5_V2
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
    delta_y = 40

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

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

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
    line_x = 345

    draw_date(55, 10)
    draw_calendar(20, 70)
    drawblack.line((line_x, 0, line_x, 600), fill = 0)
    draw_events_title(line_x + 25, 5)
    draw_events(line_x + 25, 45, 13)
    draw_current_time(730, 0)

    cropped = HBlackimage.crop((0, 0, epd7in5_V2.EPD_WIDTH - 10, epd7in5_V2.EPD_HEIGHT))
    img = add_margin(cropped, 0, 10, 0, 0, 255)
    timestamp("epd.display          ")
    epd.display(epd.getbuffer(img))
    # epd.display(epd.getbuffer(HBlackimage))
    timestamp("epd.sleep            ")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
