#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# autor: Carlos Rueda
# date: 2016-11-25
# version: 1.1

##################################################################################
# version 1.0 release notes: extract data from MySQL and generate json
# Initial version
# Requisites: library python-mysqldb. To install: "apt-get install python-mysqldb"
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
from pymongo import MongoClient


#### VARIABLES #########################################################
#DB_MONGO_IP = "127.0.0.1"
DB_MONGO_IP = "192.168.28.248"
DB_MONGO_PORT = 27017
DB_MONGO_NAME = "kyros"

########################################################################

eventos = [{'id': 900, 'name': "EVENTS", 'icon': "info.svg", 'description': "Eventos"},
{'id': 902, 'name': "ALARM", 'icon': "warning.svg", 'description': "Alarma"},
{'id': 903, 'name': "PANIC", 'icon': "siren.svg", 'description': "Pánico"},
{'id': 904, 'name': "AXA_PANIC", 'icon': "siren.svg", 'description': "Pánico"},
{'id': 905, 'name': "THEFT", 'icon': "siren.svg", 'description': "Robo"},
{'id': 906, 'name': "ACCIDENT", 'icon': "accident.svg", 'description': "Accidente"},
{'id': 907, 'name': "UNAUTHORIZE", 'icon': "prohibition.svg", 'description': "No autorizado"},
{'id': 908, 'name': "COERCION", 'icon': "knife.svg", 'description': "Coerción"},
{'id': 909, 'name': "MANUAL", 'icon': "hand.svg", 'description': "Alarma manual"},
{'id': 910, 'name': "LOW_BATTERY", 'icon': "low_battery.svg", 'description': "Bateria baja"},
{'id': 911, 'name': "MAX_SPEED", 'icon': "max_speed.svg", 'description': "Velocidad máxima excedida"},
{'id': 912, 'name': "VEHICLE_STARTED", 'icon': "start.svg", 'description': "Arranque"},
{'id': 913, 'name': "VEHICLE_STOPPED", 'icon': "stop.svg", 'description': "Parada"},
{'id': 914, 'name': "SERVICE_STARTED", 'icon': "start.svg", 'description': "Inicio de servicio"},
{'id': 915, 'name': "SERVICE_STOPPED", 'icon': "stop.svg", 'description': "Parada de servicio"},
{'id': 916, 'name': "PRIVATE_MODE_ACTIVATED", 'icon': "shield_on.svg", 'description': "Modo privado activado"},
{'id': 917, 'name': "PRIVATE_MODE_DEACTIVATED", 'icon': "shield_off.svg", 'description': "Modo privado desactivado"},
{'id': 918, 'name': "ALARM_STATE_ACTIVATED", 'icon': "alarm_activate.svg", 'description': "Estado de alarma activado"},
{'id': 919, 'name': "ALARM_STATE_DEACTIVATED", 'icon': "alarm_deactivate.svg", 'description': "Estado de alarma desactivado"},
{'id': 920, 'name': "CLAXON_ACTIVATED", 'icon': "speaker_on.svg", 'description': "Claxón activado"},
{'id': 921, 'name': "CLAXON_DEACTIVATED", 'icon': "speaker_off.svg", 'description': "Claxón desactivado"},
{'id': 922, 'name': "WARNER_ACTIVATED", 'icon': "warning_on.svg", 'description': "Warning activado"},
{'id': 923, 'name': "WARNER_DEACTIVATED", 'icon': "warning_off.svg", 'description': "Warning desactivado"},
{'id': 924, 'name': "POWERSWITCH_ACTIVATED", 'icon': "electric_on.svg", 'description': "Alimentación activada"},
{'id': 925, 'name': "POWERSWITCH_DEACTIVATED", 'icon': "electric_off.svg", 'description': "Alimentación desactivada"},
{'id': 926, 'name': "SPEAKER_ACTIVATED", 'icon': "speaker_on.svg", 'description': "Altavoz activado"},
{'id': 927, 'name': "SPEAKER_DEACTIVATED", 'icon': "speaker_off.svg", 'description': "Altavoz desactivado"},
{'id': 928, 'name': "ALARM_MODE_ACTIVATED", 'icon': "warning_on.svg", 'description': "Modo de alarma activado"},
{'id': 929, 'name': "ALARM_MODE_DEACTIVATED", 'icon': "warning_off.svg", 'description': "Modo de alarma desactivado"},
{'id': 930, 'name': "STOP_TIME_EXCEEDED", 'icon': "stop_time.svg", 'description': "Tiempo de parada excedido"},
{'id': 931, 'name': "BRACELET_BREAK_ACTIVATED", 'icon': "bracelet_on.svg", 'description': "Apertura de brazalete activado"},
{'id': 932, 'name': "BRACELET_BREAK_DEACTIVATED", 'icon': "bracelet_off.svg", 'description': "Apertura de brazalete desactivado"},
{'id': 933, 'name': "BRACELET_HANDLING_ACTIVATED", 'icon': "bracelet_on.svg", 'description': "Brazalete activado"},
{'id': 934, 'name': "BRACELET_HANDLING_DEACTIVATED", 'icon': "bracelet_off.svg", 'description': "Brazalete desactivado"},
{'id': 935, 'name': "DEAD_MAN_ACTIVATED", 'icon': "deadman_on.svg", 'description': "Hombre muerto activado"},
{'id': 936, 'name': "DEAD_MAN_DEACTIVATED", 'icon': "deadman_off.svg", 'description': "Hombre muerto desactivado"},
{'id': 937, 'name': "AGGRESSOR_APPROACHING_ACTIVATED", 'icon': "aggressor_on.svg", 'description': "Cercanía de agresor activado"},
{'id': 938, 'name': "AGGRESSOR_APPROACHING_DEACTIVATED", 'icon': "aggressor_off.svg", 'description': "Cercanía de agresor desactivado"},
{'id': 939, 'name': "AGGRESSOR_AWAY_ACTIVATED", 'icon': "aggressor_on.svg", 'description': "Separación de agresor activado"},
{'id': 940, 'name': "AGGRESSOR_AWAY_DEACTIVATED", 'icon': "aggressor_off.svg", 'description': "Separación de agresor desactivado"},
{'id': 941, 'name': "PLUG", 'icon': "plug.svg", 'description': "Enchufado"},
{'id': 942, 'name': "UNPLUG", 'icon': "unplug.svg", 'description': "Desenchufado"},
{'id': 943, 'name': "POSITION_TEST", 'icon': "pin.svg", 'description': "Test de posición"},
{'id': 944, 'name': "RALLYE_MAX_SPEED_EXCEEDED", 'icon': "max_speed.svg", 'description': "Velocidad en rally excedida"},
{'id': 945, 'name': "NOT_AUTHORIZED_STOP", 'icon': "stop.svg", 'description': "Parada no autorizada"},
{'id': 946, 'name': "NOT_AUTHORIZED_STOP_RALLY", 'icon': "stop.svg", 'description': "Parada no autorizada en rally"},
{'id': 947, 'name': "WORKING_SCHEDULE_KO", 'icon': "calendar.svg", 'description': "Horario de trabajo"},
{'id': 948, 'name': "OBLIGATORY_AREA_ACTIVATED", 'icon': "obligatory_area.svg", 'description': "Zona obligatoria activada"},
{'id': 949, 'name': "OBLIGATORY_AREA_DEACTIVATED", 'icon': "obligatory_area.svg", 'description': "Zona obligatoria desactivada"},
{'id': 950, 'name': "FORBIDDEN_AREA_ACTIVATED", 'icon': "forbidden_area.svg", 'description': "Zona prohibida activada"},
{'id': 951, 'name': "FORBIDDEN_AREA_DEACTIVATED", 'icon': "forbidden_area.svg", 'description': "Zona prohibida desactivada"},
{'id': 952, 'name': "GENERIC_AREA_ACTIVATED", 'icon': "generic_area.svg", 'description': "Zona generica activada"},
{'id': 953, 'name': "GENERIC_AREA_DEACTIVATED", 'icon': "generic_area.svg", 'description': "Zona generica desactivada"},
{'id': 954, 'name': "PROXIMITY_AREA_MAIN_ACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de proximidad activada"},
{'id': 955, 'name': "PROXIMITY_AREA_MAIN_DEACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de proximidad desactivada"},
{'id': 956, 'name': "DISTANCE_AREA_MAIN_ACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de distancia activada"},
{'id': 957, 'name': "DISTANCE_AREA_MAIN_DEACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de distancia desactivada"},
{'id': 958, 'name': "PROXIMITY_AREA_AFFECTED_ACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de proximidad afectada activada"},
{'id': 959, 'name': "PROXIMITY_AREA_AFFECTED_DEACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de proximidad afectada desactivada"},
{'id': 960, 'name': "DISTANCE_AREA_AFFECTED_ACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de distancia afectada activada"},
{'id': 961, 'name': "DISTANCE_AREA_AFFECTED_DEACTIVATED", 'icon': "proximity_area.svg", 'description': "Zona de distancia afectada desactivada"},
{'id': 962, 'name': "BEACON_IN", 'icon': "beacon_in.svg", 'description': "Entrada en baliza"},
{'id': 963, 'name': "BEACON_OUT", 'icon': "beacon_out.svg", 'description': "Salida de baliza"},
{'id': 964, 'name': "BEACON_JUMPED", 'icon': "beacon_jump.svg", 'description': "Salto de baliza"},
{'id': 965, 'name': "FRONT_SEAT_ACTIVATED", 'icon': "seat_on.svg", 'description': "Cinturón delantero activado"},
{'id': 966, 'name': "FRONT_SEAT_DEACTIVATED", 'icon': "seat_off.svg", 'description': "Cinturón delantero desactivado"},
{'id': 967, 'name': "BACK_SEAT_ACTIVATED", 'icon': "seat_on.svg", 'description': "Cinturón trasero activado"},
{'id': 968, 'name': "BACK_SEAT_DEACTIVATED", 'icon': "seat_off.svg", 'description': "Cinturón trasero desactivado"},
{'id': 969, 'name': "FLAG_DOWN", 'icon': "flag_down.svg", 'description': "Bajada de bandera"},
{'id': 970, 'name': "FLAG_UP", 'icon': "flag_up.svg", 'description': "Subida de bandera"},
{'id': 971, 'name': "TAXI_ZONE_ZERO", 'icon': "taxi.svg", 'description': "Taxi zona 0"},
{'id': 972, 'name': "TAXI_ZONE_ONE", 'icon': "taxi.svg", 'description': "Taxi zona 1"},
{'id': 973, 'name': "TAXI_ZONE_TWO", 'icon': "taxi.svg", 'description': "Taxi zona 2"},
{'id': 974, 'name': "TAXI_ZONE_THREE", 'icon': "taxi.svg", 'description': "Taxi zona 3"},
{'id': 975, 'name': "TAXI_DOOR_ACTIVATED", 'icon': "door_on.svg", 'description': "Puerta de taxi activada"},
{'id': 976, 'name': "TAXI_DOOR_DEACTIVATED", 'icon': "door_off.svg", 'description': "Puerta de taxi desactivada"},
{'id': 977, 'name': "FLAG_DOWN_TAXI_ZONE_ZERO", 'icon': "flag_down.svg", 'description': "Bajada de bandera en zona 0"},
{'id': 978, 'name': "FLAG_DOWN_TAXI_ZONE_ONE", 'icon': "flag_down.svg", 'description': "Bajada de bandera en zona 1"},
{'id': 979, 'name': "FLAG_DOWN_TAXI_ZONE_TWO", 'icon': "flag_down.svg", 'description': "Bajada de bandera en zona 2"},
{'id': 980, 'name': "FLAG_DOWN_TAXI_ZONE_THREE", 'icon': "flag_down.svg", 'description': "Bajada de bandera en zona 3"},
{'id': 981, 'name': "START_SPECIAL", 'icon': "start.svg", 'description': "Arranque especial"},
{'id': 982, 'name': "PAUSE_SPECIAL", 'icon': "pause_button.svg", 'description': "Pausa especial"},
{'id': 983, 'name': "STOP_SPECIAL", 'icon': "stop.svg", 'description': "Parada especial"},
{'id': 984, 'name': "PAUSE_VEHICLE", 'icon': "pause_button.svg", 'description': "Pausa"},
{'id': 985, 'name': "RESUME_VEHICLE", 'icon': "play_button.svg", 'description': "Reanudar"},
{'id': 986, 'name': "INIT_LOAD", 'icon': "load_on.svg", 'description': "Inico de carga"},
{'id': 987, 'name': "END_LOAD", 'icon': "load_off.svg", 'description': "Fin de carga"},
{'id': 988, 'name': "INIT_UNLOAD", 'icon': "load_on.svg", 'description': "Inicio de descarga"},
{'id': 989, 'name': "END_UNLOAD", 'icon': "load_off.svg", 'description': "Fin de descarga"},
{'id': 990, 'name': "STOP_NEAR_POI", 'icon': "stop_poi.svg", 'description': "Parada con cercanía a PDI"},
{'id': 991, 'name': "CHANGE_DRIVER", 'icon': "taxi_driver.svg", 'description': "Cambio de conductor"},
{'id': 992, 'name': "RECORD_POI", 'icon': "poi_add.svg", 'description': "Guardar PDI"},
{'id': 993, 'name': "DRIVING_HOURS_CONTROL", 'icon': "watch.svg", 'description': "Control de horas de conducción"},
{'id': 994, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_SEMANAL_MENOR_24", 'icon': "watch.svg", 'description': "Descanso semanal menor que 24h."},
{'id': 995, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_SEMANAL_REDUCIDO_NO_PERMITIDO", 'icon': "watch.svg"},
{'id': 996, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_SEMANAL_NO_COMPESA_DESCANSO_REDUCIDO", 'icon': "watch.svg", 'description': "Descanso semanal no compensa el reducido"},
{'id': 997, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_DIARIO_REDUCIDO_INCORRECTO", 'icon': "watch.svg", 'description': "Descanso reducido diario incorrecto"},
{'id': 998, 'name': "DRIVING_HOURS_CONTROL_NO_HAY_DESCANSO_SEMANAL_O_DIARIO_EN_24", 'icon': "watch.svg", 'description': "Sin descanso semanal o diario en 24h."},
{'id': 999, 'name': "DRIVING_HOURS_CONTROL_MAS_DE_10_HORAS_EN_EL_DIA", 'icon': "watch.svg", 'description': "Conducción de más de 10h. en 1 día"},
{'id': 1000, 'name': "DRIVING_HOURS_CONTROL_EXCESO_CONDUCCION_DIA_2_DIAS_MAS_DE_9_HORAS", 'icon': "watch.svg", 'description': "Conducción con más de 2 días de 9h."},
{'id': 1001, 'name': "INDRIVING_HOURS_CONTROL_EXCESO_CONDUCCION_SEMANA_ACTUAL", 'icon': "watch.svg", 'description': "Exceso de conducción semanal"},
{'id': 1002, 'name': "DRIVING_HOURS_CONTROL_EXCESO_CONDUCCION_BISEMANAL", 'icon': "watch.svg", 'description': "Exceso de conducción bisemanal"},
{'id': 1003, 'name': "DRIVING_HOURS_CONTROL_EXCESO_DE_CONDUCCION_INITERRUMPIDA", 'icon': "watch.svg", 'description': "Exceso de conducción ininterrupida"},
{'id': 1004, 'name': "DRIVING_HOURS_CONTROL_DESCANSOS_CONDUCCION_INSUFICIENTES", 'icon': "watch.svg", 'description': "Descansos de conducción insuficiente"},
{'id': 1005, 'name': "INTERVENTION", 'icon': "intervention.svg", 'description': "Intervención"},
{'id': 1006, 'name': "GATHERING", 'icon': "gathering.svg", 'description': "Agrupación"},
{'id': 1008, 'name': "INDOOR_PANIC", 'icon': "siren.svg", 'description': "Pánico indoor"},
{'id': 1009, 'name': "TRACKING_INDOOR", 'icon': "pin_home.svg", 'description': "Tracking indoor"},
{'id': 1010, 'name': "DBUSCA_PHOTO", 'icon': "camera.svg", 'description': "Foto dbusca"},
{'id': 1011, 'name': "TAMPERING", 'icon': "tampering.svg", 'description': "Manipulación"},
{'id': 1015, 'name': "TEMP0", 'icon': "thermometer.svg", 'description': "Temperatura"},
{'id': 1016, 'name': "TEMP1", 'icon': "thermometer.svg", 'description': "Temperatura"},
{'id': 1017, 'name': "TEMP2", 'icon': "thermometer.svg", 'description': "Temperatura"},
{'id': 1018, 'name': "TEMP3", 'icon': "thermometer.svg", 'description': "Temperatura"},
{'id': 1019, 'name': "HARSH_ACCELERATION", 'icon': "harsh_acceleration.svg", 'description': "Aceleración brusca"},
{'id': 1020, 'name': "HARSH_BRAKING", 'icon': "harsh_braking.svg", 'description': "Frenazo brusco"},
{'id': 1021, 'name': "PROXIMITY", 'icon': "gathering.svg", 'description': "Proximidad"},
{'id': 1022, 'name': "OYSTA_PERSONAL_EVENT", 'icon': "info.svg", 'description': "Evento personal Oysta"},
{'id': 1023, 'name': "OYSTA_CANNED_EVENT", 'icon': "info.svg", 'description': "Evento Oysta"},
{'id': 1024, 'name': "OYSTA_WAYPOINT_EVENT", 'icon': "info.svg", 'description': "Evento de waypoint Oysta"},
{'id': 1025, 'name': "OYSTA_NFC_EVENT", 'icon': "info.svg", 'description': "NFC Oysta"},
{'id': 1026, 'name': "MAX_TIME_INACTIVITY", 'icon': "snail.svg", 'description': "Inactividad excedida"},
{'id': 1027, 'name': "BATTERY_CHARGING", 'icon': "battery.svg", 'description': "Carga de bateria"},
{'id': 1028, 'name': "AMBER_ALERT", 'icon': "warning.svg", 'description': "Alerta ambar"},
{'id': 1029, 'name': "POWER_ON", 'icon': "power_on.svg", 'description': "Encendido"},
{'id': 1030, 'name': "POWER_OFF", 'icon': "power_off.svg", 'description': "Apagado"},
{'id': 1031, 'name': "CHECKIN", 'icon': "checked.svg", 'description': "Chequeo"},
{'id': 1032, 'name': "EHEALTH", 'icon': "health.svg", 'description': "e-health"},
{'id': 1033, 'name': "EMPTY_BATTERY", 'icon': "battery_empty.svg", 'description': "Bataría agotada"},
{'id': 1034, 'name': "RECOVER_BATTERY", 'icon': "battery_full.svg", 'description': "Bateria recuperada"},
{'id': 1035, 'name': "HARSH_CORNERING", 'icon': "harsh_cornering.svg", 'description': "Curva brusca"},
{'id': 1036, 'name': "RPM", 'icon': "rpm.svg", 'description': "RPM"},
{'id': 1037, 'name': "TEMP", 'icon': "thermometer.svg", 'description': "Temperatura"},
{'id': 1038, 'name': "SENSOR_RANGE", 'icon': "thermometer.svg", 'description': "Rango de sensor"},
{'id': 1039, 'name': "BATTERY_CHARGING_OFF", 'icon': "battery_empty.svg", 'description': "Carga de batería apagada"},
{'id': 1040, 'name': "OVERSPEED_AREA_ACTIVATED", 'icon': "max_speed.svg", 'description': "Zona de velocidad excesiva activada"},
{'id': 1041, 'name': "BATTERY_LEVEL", 'icon': "battery_level.svg", 'description': "Nivel de batería"},
{'id': 1042, 'name': "EVENT_OF_VEHICLE_OR_PERSONAL_DEVICE", 'icon': "info.svg", 'description': "Manual"},    
{'id': 1043, 'name': "DRIVER_IDENTIFICATION_ON", 'icon': "identification_on.svg", 'description': "Identificación del conductor activada"},
{'id': 1044, 'name': "DRIVER_IDENTIFICATION_OFF", 'icon': "identification_off.svg", 'description': "Identificación del conductor desactivada"},
{'id': 1045, 'name': "BEACON_NFC_READ", 'icon': "beacon_in.svg", 'description': "Lectura de baliza NFC"},
{'id': 1046, 'name': "BEACON_NFC_JUMPED", 'icon': "beacon_jump.svg", 'description': "Salto de baliza NFC"},
{'id': 1047, 'name': "SCAN_EVENT", 'icon': "scanner.svg", 'description': "Evento de escaner"},
{'id': 1048, 'name': "RESTART", 'icon': "power_reinit.svg", 'description': "Reinicio"},
{'id': 1049, 'name': "BT_EVENT", 'icon': "bluetooth.svg", 'description': "Evento BT"},
{'id': 1050, 'name': "STOP_IN_AREA", 'icon': "stop.svg", 'description': "Parada en zona"},
{'id': 1051, 'name': "SIDE_DOOR_OPENING", 'icon': "door_on.svg", 'description': "Apertura de puerta lateral"},
{'id': 1052, 'name': "SIDE_DOOR_CLOSING", 'icon': "door_off.svg", 'description': "Cierre de puerta lateral"},
{'id': 1053, 'name': "BACK_DOOR_OPENING", 'icon': "door_on.svg", 'description': "Apertura de puerta trasera"},
{'id': 1054, 'name': "BACK_DOOR_CLOSING", 'icon': "door_off.svg", 'description': "Cierre de puerta trasera"},
{'id': 1055, 'name': "JAMMER", 'icon': "jammer.svg", 'description': "Inhibidor GPS"}]  

########################################################################

def new_icon(type, subtype, fileName, svg):
	con = MongoClient(DB_MONGO_IP, int(DB_MONGO_PORT))
	db = con[DB_MONGO_NAME]
	icon_collection = db['ICON']
	icon = {
    "type" : type,
    "subtype" : subtype,
    "file_name" : fileName,
    "svg" : svg
	}
	icon_collection.save(icon)

def leer_svg(fichero):
    #str = open(fichero, 'r').read()
    #return str
    enc = "latin-1"
    f = open(fichero, "r")
    content = f.read() # raw encoded content
    u_content = content.decode(enc) # decodes from enc to unicode
    utf8_content = u_content.encode("utf8")
    return utf8_content

########################################################################

########################################################################

print eventos[10]['id']
'''
for file_name in listdir("./events"):
    svg = leer_svg("./events/"+file_name)
    new_icon(1, 0, file_name, svg)
'''
