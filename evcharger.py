# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import config
import display
import power, time, serial
import mqtt
import QR
from getmac import get_mac_address

config.relay_pin.value = True
config.orange_LED.value = False
config.green_LED.value = True
config.red_LED.value = False
QR.generate_qr(f"{config.dashboard_url}/?deviceID={get_mac_address()}")

display.display_text("Welcome !!\nConnecting Sensor")
time.sleep(1)

master = power.power_track_init(serial)
while(master == None):
    display.display_text("Problem with \nSensor connection.\nCheck wiring..")
    print("trying to initalize power tracking")
    master= power.power_track_init(serial)
    time.sleep(1)

mqtt_client = mqtt.connect_mqtt()
mqtt_client.on_disconnect = mqtt.on_disconnect
mqtt.subscribe(mqtt_client)

mqtt_client.loop_start()

prev_connect_flag = False
config.prev_idle_time = time.time()

def idle_timeout_routine():
    mqtt.command = "stop"
    display.display_text(f"Charger Idle for\n{config.idle_time_in_sec} Seconds")
    config.relay_pin.value = True
    config.red_LED.value = False
    config.green_LED.value = True
    config.orange_LED.value = False
    time.sleep(2)
    display.draw_image("/home/surya/evcharger/qr.png")

while(1):
    connect_flag = mqtt.connection_flag

    if(connect_flag==True):
    
        if(mqtt.command=="start"):
            reading = power.get_power(master)
            if(reading["current_A"] < config.cutoff_current):
                config.orange_LED.value = True
                if((time.time()-config.prev_idle_time) > config.idle_time_in_sec):
                    idle_timeout_routine()
                    
            else:
                config.orange_LED.value = False
                config.prev_idle_time = time.time()

            display.display_info(reading["voltage"], reading["current_A"], reading["energy_Wh"]/1000)

            data = f'{{"deviceID": {config.deviceId}, "Power": {reading["energy_Wh"]/1000}}}'

            print(data)
            mqtt.publish(mqtt_client, data)
        
        elif(prev_connect_flag==False):
            display.draw_image("/home/surya/evcharger/qr.png")

    elif(connect_flag==False):
        display.display_text("Connecting to \nServer . . .")
    
    time.sleep(2)

    prev_connect_flag = connect_flag

mqtt_client.loop_stop()