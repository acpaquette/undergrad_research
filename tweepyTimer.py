#!/usr/bin/env python
import tweepyTest
import datetime

count = 0

while(True):
    time = datetime.datetime.now()
    tweepyTest.__init__(time, count)
