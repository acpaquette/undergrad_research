#!/usr/bin/env python
import tweepyTest
import datetime
import os

while(True):
    time = datetime.datetime.now()
    tweepyTest.__init__(time)

    #works when put into terminal, but not when running live
    os.system('cat output_machine1_time* <(tail +2 output_machine2_time*) <(tail +2 output_machine3_time*) > bigfile.csv')
    #os.system('rm output_machine1_time*')
    #os.system('rm output_machine2_time*')
    #os.system('rm output_machine3_time*')
