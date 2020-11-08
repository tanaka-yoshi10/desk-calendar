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

def current_time() :
    nowtime = datetime.datetime.now()
    return nowtime.strftime('%T')

def timestamp(mess):
        nowtime = datetime.datetime.now()
        print("{}: {}".format(mess,nowtime.strftime('%T.%f')))

def ntp_status():
    out = check_output(["ntpq", "-c", "sysinfo"])

    for line in out.splitlines():
        if "system peer: " in line.decode():
            peer = re.sub('^system peer: *', '', line.decode())

        if "stratum:" in line.decode():
            st = re.sub("^stratum: *", "", line.decode())

    return (int(st), peer)

def draw_calendar():
    initial_x = 20
    initial_y = 70
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
    print(nowtime)
    print(nowtime.year)

    x = initial_x
    pprint.pprint(calendar.monthcalendar(nowtime.year, nowtime.month))
    for week in calendar.monthcalendar(nowtime.year, nowtime.month):
        print(week)
        for day in week:
            print(day)
            if day > 0:
                drawblack.text((  x,  y), str(day), font = font24, fill = 0)
            x += delta_x
        x = initial_x
        y += delta_y

font48 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 48)
font24 = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
Symb48 = ImageFont.truetype('/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf', 48)

try:
    logging.info("epd7in5_V2 Demo")

    # (ntp_stratum, ntp_sys_peer) = ntp_status()

    epd = epd7in5_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    # epd.Clear()

    timestamp("make image           ")
    # Drawing on the Horizontal image
    HBlackimage = Image.new('1', (epd7in5_V2.EPD_WIDTH, epd7in5_V2.EPD_HEIGHT), 255)  # 298*126

    # Horizontal
    timestamp("Drawing              ")
    drawblack = ImageDraw.Draw(HBlackimage)

    drawblack.text((  0,  0), u'ただ今の時刻', font = font48, fill = 0)
    draw_calendar()
    drawblack.text((288, 14), u'⏰' ,font = Symb48, fill = 0)

    list = google_calendar_2.google_calendar()[:10]
    y = 30
    for item in list:
        print(item['start'], item['summary'])
        start = item['event']['start'].get('dateTime')
        if start:
            time = item['date'].strftime('%m-%d %H:%M ')
        else:
            time = item['date'].strftime('%m-%d ')
        drawblack.text((  400,  y), time + item['summary'], font = font24, fill = 0)
        y += 30

    drawblack.text((  700, 0), current_time(), font = font24, fill = 0)
    # drawblack.text((  0,102), 'NTP stratum:{:2d}'.format(ntp_stratum), font = font24, fill = 0)
    # drawblack.text(( 48,127),     'peer:{:s}'.format(ntp_sys_peer),    font = font24, fill = 0)

    timestamp("epd.display          ")
    epd.display(epd.getbuffer(HBlackimage))
    timestamp("epd.sleep            ")
    epd.sleep()

    #font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    #font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Drawing on the Horizontal image
    # logging.info("1.Drawing on the Horizontal image...")
    # Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    # draw = ImageDraw.Draw(Himage)
    # draw.text((10, 0), 'hello world', font = font24, fill = 0)
    # draw.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
    # draw.text((150, 0), u'微雪电子', font = font24, fill = 0)    
    # draw.line((20, 50, 70, 100), fill = 0)
    # draw.line((70, 50, 20, 100), fill = 0)
    # draw.rectangle((20, 50, 70, 100), outline = 0)
    # draw.line((165, 50, 165, 100), fill = 0)
    # draw.line((140, 75, 190, 75), fill = 0)
    # draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    # draw.rectangle((80, 50, 130, 100), fill = 0)
    # draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)

    # Drawing on the Vertical image
    # logging.info("2.Drawing on the Vertical image...")
    # Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # draw = ImageDraw.Draw(Limage)
    # draw.text((2, 0), 'hello world', font = font18, fill = 0)
    # draw.text((2, 20), '7.5inch epd', font = font18, fill = 0)
    # draw.text((20, 50), u'微雪电子', font = font18, fill = 0)
    # draw.line((10, 90, 60, 140), fill = 0)
    # draw.line((60, 90, 10, 140), fill = 0)
    # draw.rectangle((10, 90, 60, 140), outline = 0)
    # draw.line((95, 90, 95, 140), fill = 0)
    # draw.line((70, 115, 120, 115), fill = 0)
    # draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
    # draw.rectangle((10, 150, 60, 200), fill = 0)
    # draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
    # epd.display(epd.getbuffer(Limage))
    # time.sleep(2)

    # logging.info("3.read bmp file")
    #Himage = Image.open(os.path.join(picdir, '7in5_V2.bmp'))
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)

    # logging.info("4.read bmp file on window")
    # Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    #bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    # Himage2.paste(bmp, (50,10))
    # epd.display(epd.getbuffer(Himage2))
    # time.sleep(2)

    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()

    # logging.info("Goto Sleep...")
    # epd.sleep()
    # epd.Dev_exit()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
