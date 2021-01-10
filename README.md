# desk-calendar

https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT
Install BCM2835 libraries
```
sudo apt install fonts-noto-cjk ttf-ancient-fonts-symbola libjpeg-dev
sudo pip3 install pipenv
sudo pipenv install
```

crontab -l
```
@reboot cd /home/pi/desk-calendar && sudo pipenv run python3 desk_calendar.py
0 * * * * cd /home/pi/desk-calendar && sudo pipenv run python3 desk_calendar.py
```
