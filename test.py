#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import datetime
x = datetime.datetime.now()
 
dicdias = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miercoles','THURSDAY':'Jueves', \
'FRIDAY':'Viernes','SATURDAY':'saturday','SUNDAY':'Domingo'}
anho = x.year
mes =  x.month
dia= x.day
hora = x.hour

fecha = datetime.date(anho, mes, dia)
print (dicdias[fecha.strftime('%A').upper()])
print hora