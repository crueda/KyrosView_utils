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

eventos = [{'id': 900, 'name': "EVENTS", 'file_name': "info.svg", 'description': "Eventos"},
{'id': 902, 'name': "ALARM", 'file_name': "warning.svg", 'description': "Alarma"},
{'id': 903, 'name': "PANIC", 'file_name': "siren.svg", 'description': "Pánico"},
{'id': 904, 'name': "AXA_PANIC", 'file_name': "siren.svg", 'description': "Pánico"},
{'id': 905, 'name': "THEFT", 'file_name': "siren.svg", 'description': "Robo"},
{'id': 906, 'name': "ACCIDENT", 'file_name': "accident.svg", 'description': "Accidente"},
{'id': 907, 'name': "UNAUTHORIZE", 'file_name': "prohibition.svg", 'description': "No autorizado"},
{'id': 908, 'name': "COERCION", 'file_name': "knife.svg", 'description': "Coerción"},
{'id': 909, 'name': "MANUAL", 'file_name': "hand.svg", 'description': "Alarma manual"},
{'id': 910, 'name': "LOW_BATTERY", 'file_name': "low_battery.svg", 'description': "Bateria baja"},
{'id': 911, 'name': "MAX_SPEED", 'file_name': "max_speed.svg", 'description': "Velocidad máxima excedida"},
{'id': 912, 'name': "VEHICLE_STARTED", 'file_name': "start.svg", 'description': "Arranque"},
{'id': 913, 'name': "VEHICLE_STOPPED", 'file_name': "stop.svg", 'description': "Parada"},
{'id': 914, 'name': "SERVICE_STARTED", 'file_name': "start.svg", 'description': "Inicio de servicio"},
{'id': 915, 'name': "SERVICE_STOPPED", 'file_name': "stop.svg", 'description': "Parada de servicio"},
{'id': 916, 'name': "PRIVATE_MODE_ACTIVATED", 'file_name': "shield_on.svg", 'description': "Modo privado activado"},
{'id': 917, 'name': "PRIVATE_MODE_DEACTIVATED", 'file_name': "shield_off.svg", 'description': "Modo privado desactivado"},
{'id': 918, 'name': "ALARM_STATE_ACTIVATED", 'file_name': "alarm_activate.svg", 'description': "Estado de alarma activado"},
{'id': 919, 'name': "ALARM_STATE_DEACTIVATED", 'file_name': "alarm_deactivate.svg", 'description': "Estado de alarma desactivado"},
{'id': 920, 'name': "CLAXON_ACTIVATED", 'file_name': "speaker_on.svg", 'description': "Claxón activado"},
{'id': 921, 'name': "CLAXON_DEACTIVATED", 'file_name': "speaker_off.svg", 'description': "Claxón desactivado"},
{'id': 922, 'name': "WARNER_ACTIVATED", 'file_name': "warning_on.svg", 'description': "Warning activado"},
{'id': 923, 'name': "WARNER_DEACTIVATED", 'file_name': "warning_off.svg", 'description': "Warning desactivado"},
{'id': 924, 'name': "POWERSWITCH_ACTIVATED", 'file_name': "electric_on.svg", 'description': "Alimentación activada"},
{'id': 925, 'name': "POWERSWITCH_DEACTIVATED", 'file_name': "electric_off.svg", 'description': "Alimentación desactivada"},
{'id': 926, 'name': "SPEAKER_ACTIVATED", 'file_name': "speaker_on.svg", 'description': "Altavoz activado"},
{'id': 927, 'name': "SPEAKER_DEACTIVATED", 'file_name': "speaker_off.svg", 'description': "Altavoz desactivado"},
{'id': 928, 'name': "ALARM_MODE_ACTIVATED", 'file_name': "warning_on.svg", 'description': "Modo de alarma activado"},
{'id': 929, 'name': "ALARM_MODE_DEACTIVATED", 'file_name': "warning_off.svg", 'description': "Modo de alarma desactivado"},
{'id': 930, 'name': "STOP_TIME_EXCEEDED", 'file_name': "stop_time.svg", 'description': "Tiempo de parada excedido"},
{'id': 931, 'name': "BRACELET_BREAK_ACTIVATED", 'file_name': "bracelet_on.svg", 'description': "Apertura de brazalete activado"},
{'id': 932, 'name': "BRACELET_BREAK_DEACTIVATED", 'file_name': "bracelet_off.svg", 'description': "Apertura de brazalete desactivado"},
{'id': 933, 'name': "BRACELET_HANDLING_ACTIVATED", 'file_name': "bracelet_on.svg", 'description': "Brazalete activado"},
{'id': 934, 'name': "BRACELET_HANDLING_DEACTIVATED", 'file_name': "bracelet_off.svg", 'description': "Brazalete desactivado"},
{'id': 935, 'name': "DEAD_MAN_ACTIVATED", 'file_name': "deadman_on.svg", 'description': "Hombre muerto activado"},
{'id': 936, 'name': "DEAD_MAN_DEACTIVATED", 'file_name': "deadman_off.svg", 'description': "Hombre muerto desactivado"},
{'id': 937, 'name': "AGGRESSOR_APPROACHING_ACTIVATED", 'file_name': "aggressor_on.svg", 'description': "Cercanía de agresor activado"},
{'id': 938, 'name': "AGGRESSOR_APPROACHING_DEACTIVATED", 'file_name': "aggressor_off.svg", 'description': "Cercanía de agresor desactivado"},
{'id': 939, 'name': "AGGRESSOR_AWAY_ACTIVATED", 'file_name': "aggressor_on.svg", 'description': "Separación de agresor activado"},
{'id': 940, 'name': "AGGRESSOR_AWAY_DEACTIVATED", 'file_name': "aggressor_off.svg", 'description': "Separación de agresor desactivado"},
{'id': 941, 'name': "PLUG", 'file_name': "plug.svg", 'description': "Enchufado"},
{'id': 942, 'name': "UNPLUG", 'file_name': "unplug.svg", 'description': "Desenchufado"},
{'id': 943, 'name': "POSITION_TEST", 'file_name': "pin.svg", 'description': "Test de posición"},
{'id': 944, 'name': "RALLYE_MAX_SPEED_EXCEEDED", 'file_name': "max_speed.svg", 'description': "Velocidad en rally excedida"},
{'id': 945, 'name': "NOT_AUTHORIZED_STOP", 'file_name': "stop.svg", 'description': "Parada no autorizada"},
{'id': 946, 'name': "NOT_AUTHORIZED_STOP_RALLY", 'file_name': "stop.svg", 'description': "Parada no autorizada en rally"},
{'id': 947, 'name': "WORKING_SCHEDULE_KO", 'file_name': "calendar.svg", 'description': "Horario de trabajo"},
{'id': 948, 'name': "OBLIGATORY_AREA_ACTIVATED", 'file_name': "obligatory_area.svg", 'description': "Zona obligatoria activada"},
{'id': 949, 'name': "OBLIGATORY_AREA_DEACTIVATED", 'file_name': "obligatory_area.svg", 'description': "Zona obligatoria desactivada"},
{'id': 950, 'name': "FORBIDDEN_AREA_ACTIVATED", 'file_name': "forbidden_area.svg", 'description': "Zona prohibida activada"},
{'id': 951, 'name': "FORBIDDEN_AREA_DEACTIVATED", 'file_name': "forbidden_area.svg", 'description': "Zona prohibida desactivada"},
{'id': 952, 'name': "GENERIC_AREA_ACTIVATED", 'file_name': "generic_area.svg", 'description': "Zona generica activada"},
{'id': 953, 'name': "GENERIC_AREA_DEACTIVATED", 'file_name': "generic_area.svg", 'description': "Zona generica desactivada"},
{'id': 954, 'name': "PROXIMITY_AREA_MAIN_ACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de proximidad activada"},
{'id': 955, 'name': "PROXIMITY_AREA_MAIN_DEACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de proximidad desactivada"},
{'id': 956, 'name': "DISTANCE_AREA_MAIN_ACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de distancia activada"},
{'id': 957, 'name': "DISTANCE_AREA_MAIN_DEACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de distancia desactivada"},
{'id': 958, 'name': "PROXIMITY_AREA_AFFECTED_ACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de proximidad afectada activada"},
{'id': 959, 'name': "PROXIMITY_AREA_AFFECTED_DEACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de proximidad afectada desactivada"},
{'id': 960, 'name': "DISTANCE_AREA_AFFECTED_ACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de distancia afectada activada"},
{'id': 961, 'name': "DISTANCE_AREA_AFFECTED_DEACTIVATED", 'file_name': "proximity_area.svg", 'description': "Zona de distancia afectada desactivada"},
{'id': 962, 'name': "BEACON_IN", 'file_name': "beacon_in.svg", 'description': "Entrada en baliza"},
{'id': 963, 'name': "BEACON_OUT", 'file_name': "beacon_out.svg", 'description': "Salida de baliza"},
{'id': 964, 'name': "BEACON_JUMPED", 'file_name': "beacon_jump.svg", 'description': "Salto de baliza"},
{'id': 965, 'name': "FRONT_SEAT_ACTIVATED", 'file_name': "seat_on.svg", 'description': "Cinturón delantero activado"},
{'id': 966, 'name': "FRONT_SEAT_DEACTIVATED", 'file_name': "seat_off.svg", 'description': "Cinturón delantero desactivado"},
{'id': 967, 'name': "BACK_SEAT_ACTIVATED", 'file_name': "seat_on.svg", 'description': "Cinturón trasero activado"},
{'id': 968, 'name': "BACK_SEAT_DEACTIVATED", 'file_name': "seat_off.svg", 'description': "Cinturón trasero desactivado"},
{'id': 969, 'name': "FLAG_DOWN", 'file_name': "flag_down.svg", 'description': "Bajada de bandera"},
{'id': 970, 'name': "FLAG_UP", 'file_name': "flag_up.svg", 'description': "Subida de bandera"},
{'id': 971, 'name': "TAXI_ZONE_ZERO", 'file_name': "taxi.svg", 'description': "Taxi zona 0"},
{'id': 972, 'name': "TAXI_ZONE_ONE", 'file_name': "taxi.svg", 'description': "Taxi zona 1"},
{'id': 973, 'name': "TAXI_ZONE_TWO", 'file_name': "taxi.svg", 'description': "Taxi zona 2"},
{'id': 974, 'name': "TAXI_ZONE_THREE", 'file_name': "taxi.svg", 'description': "Taxi zona 3"},
{'id': 975, 'name': "TAXI_DOOR_ACTIVATED", 'file_name': "door_on.svg", 'description': "Puerta de taxi activada"},
{'id': 976, 'name': "TAXI_DOOR_DEACTIVATED", 'file_name': "door_off.svg", 'description': "Puerta de taxi desactivada"},
{'id': 977, 'name': "FLAG_DOWN_TAXI_ZONE_ZERO", 'file_name': "flag_down.svg", 'description': "Bajada de bandera en zona 0"},
{'id': 978, 'name': "FLAG_DOWN_TAXI_ZONE_ONE", 'file_name': "flag_down.svg", 'description': "Bajada de bandera en zona 1"},
{'id': 979, 'name': "FLAG_DOWN_TAXI_ZONE_TWO", 'file_name': "flag_down.svg", 'description': "Bajada de bandera en zona 2"},
{'id': 980, 'name': "FLAG_DOWN_TAXI_ZONE_THREE", 'file_name': "flag_down.svg", 'description': "Bajada de bandera en zona 3"},
{'id': 981, 'name': "START_SPECIAL", 'file_name': "start.svg", 'description': "Arranque especial"},
{'id': 982, 'name': "PAUSE_SPECIAL", 'file_name': "pause_button.svg", 'description': "Pausa especial"},
{'id': 983, 'name': "STOP_SPECIAL", 'file_name': "stop.svg", 'description': "Parada especial"},
{'id': 984, 'name': "PAUSE_VEHICLE", 'file_name': "pause_button.svg", 'description': "Pausa"},
{'id': 985, 'name': "RESUME_VEHICLE", 'file_name': "play_button.svg", 'description': "Reanudar"},
{'id': 986, 'name': "INIT_LOAD", 'file_name': "load_on.svg", 'description': "Inico de carga"},
{'id': 987, 'name': "END_LOAD", 'file_name': "load_off.svg", 'description': "Fin de carga"},
{'id': 988, 'name': "INIT_UNLOAD", 'file_name': "load_on.svg", 'description': "Inicio de descarga"},
{'id': 989, 'name': "END_UNLOAD", 'file_name': "load_off.svg", 'description': "Fin de descarga"},
{'id': 990, 'name': "STOP_NEAR_POI", 'file_name': "stop_poi.svg", 'description': "Parada con cercanía a PDI"},
{'id': 991, 'name': "CHANGE_DRIVER", 'file_name': "taxi_driver.svg", 'description': "Cambio de conductor"},
{'id': 992, 'name': "RECORD_POI", 'file_name': "poi_add.svg", 'description': "Guardar PDI"},
{'id': 993, 'name': "DRIVING_HOURS_CONTROL", 'file_name': "watch.svg", 'description': "Control de horas de conducción"},
{'id': 994, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_SEMANAL_MENOR_24", 'file_name': "watch.svg", 'description': "Descanso semanal menor que 24h."},
{'id': 995, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_SEMANAL_REDUCIDO_NO_PERMITIDO", 'file_name': "watch.svg"},
{'id': 996, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_SEMANAL_NO_COMPESA_DESCANSO_REDUCIDO", 'file_name': "watch.svg", 'description': "Descanso semanal no compensa el reducido"},
{'id': 997, 'name': "DRIVING_HOURS_CONTROL_DESCANSO_DIARIO_REDUCIDO_INCORRECTO", 'file_name': "watch.svg", 'description': "Descanso reducido diario incorrecto"},
{'id': 998, 'name': "DRIVING_HOURS_CONTROL_NO_HAY_DESCANSO_SEMANAL_O_DIARIO_EN_24", 'file_name': "watch.svg", 'description': "Sin descanso semanal o diario en 24h."},
{'id': 999, 'name': "DRIVING_HOURS_CONTROL_MAS_DE_10_HORAS_EN_EL_DIA", 'file_name': "watch.svg", 'description': "Conducción de más de 10h. en 1 día"},
{'id': 1000, 'name': "DRIVING_HOURS_CONTROL_EXCESO_CONDUCCION_DIA_2_DIAS_MAS_DE_9_HORAS", 'file_name': "watch.svg", 'description': "Conducción con más de 2 días de 9h."},
{'id': 1001, 'name': "INDRIVING_HOURS_CONTROL_EXCESO_CONDUCCION_SEMANA_ACTUAL", 'file_name': "watch.svg", 'description': "Exceso de conducción semanal"},
{'id': 1002, 'name': "DRIVING_HOURS_CONTROL_EXCESO_CONDUCCION_BISEMANAL", 'file_name': "watch.svg", 'description': "Exceso de conducción bisemanal"},
{'id': 1003, 'name': "DRIVING_HOURS_CONTROL_EXCESO_DE_CONDUCCION_INITERRUMPIDA", 'file_name': "watch.svg", 'description': "Exceso de conducción ininterrupida"},
{'id': 1004, 'name': "DRIVING_HOURS_CONTROL_DESCANSOS_CONDUCCION_INSUFICIENTES", 'file_name': "watch.svg", 'description': "Descansos de conducción insuficiente"},
{'id': 1005, 'name': "INTERVENTION", 'file_name': "intervention.svg", 'description': "Intervención"},
{'id': 1006, 'name': "GATHERING", 'file_name': "gathering.svg", 'description': "Agrupación"},
{'id': 1008, 'name': "INDOOR_PANIC", 'file_name': "siren.svg", 'description': "Pánico indoor"},
{'id': 1009, 'name': "TRACKING_INDOOR", 'file_name': "pin_home.svg", 'description': "Tracking indoor"},
{'id': 1010, 'name': "DBUSCA_PHOTO", 'file_name': "camera.svg", 'description': "Foto dbusca"},
{'id': 1011, 'name': "TAMPERING", 'file_name': "tampering.svg", 'description': "Manipulación"},
{'id': 1015, 'name': "TEMP0", 'file_name': "thermometer.svg", 'description': "Temperatura"},
{'id': 1016, 'name': "TEMP1", 'file_name': "thermometer.svg", 'description': "Temperatura"},
{'id': 1017, 'name': "TEMP2", 'file_name': "thermometer.svg", 'description': "Temperatura"},
{'id': 1018, 'name': "TEMP3", 'file_name': "thermometer.svg", 'description': "Temperatura"},
{'id': 1019, 'name': "HARSH_ACCELERATION", 'file_name': "harsh_acceleration.svg", 'description': "Aceleración brusca"},
{'id': 1020, 'name': "HARSH_BRAKING", 'file_name': "harsh_braking.svg", 'description': "Frenazo brusco"},
{'id': 1021, 'name': "PROXIMITY", 'file_name': "gathering.svg", 'description': "Proximidad"},
{'id': 1022, 'name': "OYSTA_PERSONAL_EVENT", 'file_name': "info.svg", 'description': "Evento personal Oysta"},
{'id': 1023, 'name': "OYSTA_CANNED_EVENT", 'file_name': "info.svg", 'description': "Evento Oysta"},
{'id': 1024, 'name': "OYSTA_WAYPOINT_EVENT", 'file_name': "info.svg", 'description': "Evento de waypoint Oysta"},
{'id': 1025, 'name': "OYSTA_NFC_EVENT", 'file_name': "info.svg", 'description': "NFC Oysta"},
{'id': 1026, 'name': "MAX_TIME_INACTIVITY", 'file_name': "snail.svg", 'description': "Inactividad excedida"},
{'id': 1027, 'name': "BATTERY_CHARGING", 'file_name': "battery.svg", 'description': "Carga de bateria"},
{'id': 1028, 'name': "AMBER_ALERT", 'file_name': "warning.svg", 'description': "Alerta ambar"},
{'id': 1029, 'name': "POWER_ON", 'file_name': "power_on.svg", 'description': "Encendido"},
{'id': 1030, 'name': "POWER_OFF", 'file_name': "power_off.svg", 'description': "Apagado"},
{'id': 1031, 'name': "CHECKIN", 'file_name': "checked.svg", 'description': "Chequeo"},
{'id': 1032, 'name': "EHEALTH", 'file_name': "health.svg", 'description': "e-health"},
{'id': 1033, 'name': "EMPTY_BATTERY", 'file_name': "battery_empty.svg", 'description': "Bataría agotada"},
{'id': 1034, 'name': "RECOVER_BATTERY", 'file_name': "battery_full.svg", 'description': "Bateria recuperada"},
{'id': 1035, 'name': "HARSH_CORNERING", 'file_name': "harsh_cornering.svg", 'description': "Curva brusca"},
{'id': 1036, 'name': "RPM", 'file_name': "rpm.svg", 'description': "RPM"},
{'id': 1037, 'name': "TEMP", 'file_name': "thermometer.svg", 'description': "Temperatura"},
{'id': 1038, 'name': "SENSOR_RANGE", 'file_name': "thermometer.svg", 'description': "Rango de sensor"},
{'id': 1039, 'name': "BATTERY_CHARGING_OFF", 'file_name': "battery_empty.svg", 'description': "Carga de batería apagada"},
{'id': 1040, 'name': "OVERSPEED_AREA_ACTIVATED", 'file_name': "max_speed.svg", 'description': "Zona de velocidad excesiva activada"},
{'id': 1041, 'name': "BATTERY_LEVEL", 'file_name': "battery_level.svg", 'description': "Nivel de batería"},
{'id': 1042, 'name': "EVENT_OF_VEHICLE_OR_PERSONAL_DEVICE", 'file_name': "info.svg", 'description': "Manual"},    
{'id': 1043, 'name': "DRIVER_IDENTIFICATION_ON", 'file_name': "identification_on.svg", 'description': "Identificación del conductor activada"},
{'id': 1044, 'name': "DRIVER_IDENTIFICATION_OFF", 'file_name': "identification_off.svg", 'description': "Identificación del conductor desactivada"},
{'id': 1045, 'name': "BEACON_NFC_READ", 'file_name': "beacon_in.svg", 'description': "Lectura de baliza NFC"},
{'id': 1046, 'name': "BEACON_NFC_JUMPED", 'file_name': "beacon_jump.svg", 'description': "Salto de baliza NFC"},
{'id': 1047, 'name': "SCAN_EVENT", 'file_name': "scanner.svg", 'description': "Evento de escaner"},
{'id': 1048, 'name': "RESTART", 'file_name': "power_reinit.svg", 'description': "Reinicio"},
{'id': 1049, 'name': "BT_EVENT", 'file_name': "bluetooth.svg", 'description': "Evento BT"},
{'id': 1050, 'name': "STOP_IN_AREA", 'file_name': "stop.svg", 'description': "Parada en zona"},
{'id': 1051, 'name': "SIDE_DOOR_OPENING", 'file_name': "door_on.svg", 'description': "Apertura de puerta lateral"},
{'id': 1052, 'name': "SIDE_DOOR_CLOSING", 'file_name': "door_off.svg", 'description': "Cierre de puerta lateral"},
{'id': 1053, 'name': "BACK_DOOR_OPENING", 'file_name': "door_on.svg", 'description': "Apertura de puerta trasera"},
{'id': 1054, 'name': "BACK_DOOR_CLOSING", 'file_name': "door_off.svg", 'description': "Cierre de puerta trasera"},
{'id': 1055, 'name': "JAMMER", 'file_name': "jammer.svg", 'description': "Inhibidor GPS"}]  

########################################################################

def new_icon(type, subtype, name, description, fileName, svg):
	con = MongoClient(DB_MONGO_IP, int(DB_MONGO_PORT))
	db = con[DB_MONGO_NAME]
	icon_collection = db['ICON']
	icon = {
    "version" : 1,
    "type" : type,
    "subtype" : subtype,
    "name" : name,
    "description" : description,
    "file_name" : fileName,
    "svg" : svg
	}
	icon_collection.save(icon)

def leer_svg(fichero):
    enc = "latin-1"
    f = open(fichero, "r")
    content = f.read() # raw encoded content
    u_content = content.decode(enc) # decodes from enc to unicode
    utf8_content = u_content.encode("utf8")
    return utf8_content

def get_event(fileName):
    for element in eventos:
        #print element['file_name']
        if (element['file_name']==fileName):
            return element
    #print "NO encontrado: "+fileName
    return None

########################################################################

########################################################################

print "Start process"
#print eventos[10]['id']

for file_name in listdir("./events"):
    svg = leer_svg("./events/"+file_name)
    evento = get_event(file_name)
    #print evento
    if (evento!=None):
        new_icon(1, evento['id'], evento['name'], evento['description'], file_name, svg)

print "Done!"