#!/usr/bin/python3.6
# coding: utf-8

import datetime
import start

lastStart = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d').date()

while True:
    today = datetime.datetime.today().date()
    if (today - lastStart).days > 2:
        start.start_parser()
        print(today, 'DONE')
        lastStart = today
