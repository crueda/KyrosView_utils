#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# autor: Carlos Rueda
# date: 2016-11-25
# version: 1.1

##################################################################################
# version 1.0 release notes: extract data from MySQL and generate json
# Initial version
##################################################################################

import logging, logging.handlers
import os
import json
import sys
import datetime
import calendar
import time
import json
from os import listdir


#### VARIABLES #########################################################


########################################################################

########################################################################

print "Start process"

for file_name in listdir("./events"):
	if (file_name.find('.svg')!=-1):
		comando = "/Applications/Inkscape.app/Contents/Resources/bin/inkscape --export-png /Users/Carlos/Workspace/KyrosView/KyrosView_utils/events/png/" + file_name[0: file_name.find('.svg')] + ".png -w 50 -h 50 /Users/Carlos/Workspace/KyrosView/KyrosView_utils/events/" + file_name
		print comando
		os.system(comando)

print "Done!"
