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

config.relay_pin.value = True
QR.generate_qr(f"{config.dashboard_url}/?deviceID={config.deviceId}")

master = power.power_track_init(serial)
while(master == None):
    print("trying to initalize power tracking")
    master= power.power_track_init(serial)
    time.sleep(1)

mqtt_client = mqtt.connect_mqtt()
mqtt_client.on_disconnect = mqtt.on_disconnect
mqtt.subscribe(mqtt_client)

mqtt_client.loop_start()

prev_connect_flag = False

while(1):
    connect_flag = mqtt.connection_flag

    if(connect_flag==True):
        
        if(mqtt.command=="start"):
            reading = power.get_power(master)
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