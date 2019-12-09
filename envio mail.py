#!/usr/bin/env python 1
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import sys
import smtplib
import mimetypes

global supero
supero = False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Conectado - Codigo de resultado: "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/proyectos/voltaje")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    lista = msg.topic.split("/")

    global supero

    if str(lista[2]) == "voltaje" and float(msg.payload) > 26:
       supero = False

    if supero == False and str(lista[2]) == "voltaje" and float(msg.payload) < 26:

        supero = True

        from email.mime.text import MIMEText     
        emisor = "sensorweb.itver@gmail.com"
        receptor = "sensorweb.itver@gmail.com"
        
        print("Enviando Email...")
     
        # Configuracion del mensaje
        mensaje = MIMEText("El Voltaje es: " + str(msg.payload)+" Fallo en el suministro Electrico")
        mensaje['From']=emisor
        mensaje['To']=receptor
        mensaje['Subject']= "ALERTA"
     
        try:
            # Nos conectamos al servidor SMTP de Gmail
            serverSMTP = smtplib.SMTP('smtp.gmail.com',587)
            serverSMTP.ehlo()
            serverSMTP.starttls()
            serverSMTP.ehlo()
            serverSMTP.login(emisor,"wifiesp8266")
            print("Conectado con exito al servidor SMTP...")
        except:
            print("Error al intentar conectarse al servidor SMTP...")
     
        try:
            # Enviamos el mensaje
            serverSMTP.sendmail(emisor,receptor,mensaje.as_string())
            # Cerramos la conexion
            serverSMTP.close()
            print("Email enviado con exito...")
        except:
            print("Error al intentar enviar el email...")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("tailor.cloudmqtt.com", 14232, 60)
except:
    print("No se pudo conectar con el MQTT Broker...")
    print("Cerrando...")
    sys.exit()
    
client.username_pw_set("proyectos", "123456789")

try:
    client.loop_forever()
except KeyboardInterrupt:  #precionar Crtl + C para salir
    print("Cerrando...")
