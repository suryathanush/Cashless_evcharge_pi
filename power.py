import time
import json
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

def power_track_init(serial):
    try:
        # Connect to the slave
        serial = serial.Serial(
                               port='/dev/ttyUSB0',
                               baudrate=9600,
                               bytesize=8,
                               parity='N',
                               stopbits=1,
                               xonxoff=0
                              )

        master = modbus_rtu.RtuMaster(serial)
        master.set_timeout(2.0)
        master.set_verbose(True)
        return master
    except Exception as e:
        print(e)

def get_power(master):
    dict_payload = dict()
    data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

    dict_payload["voltage"]= data[0] / 10.0
    dict_payload["current_A"] = (data[1] + (data[2] << 16)) / 1000.0 # [A]
    dict_payload["power_W"] = (data[3] + (data[4] << 16)) / 10.0 # [W]
    dict_payload["energy_Wh"] = data[5] + (data[6] << 16) # [Wh]
    dict_payload["frequency_Hz"] = data[7] / 10.0 # [Hz]
    dict_payload["power_factor"] = data[8] / 100.0
    dict_payload["alarm"] = data[9] # 0 = no alarm
    #str_payload = json.dumps(dict_payload, indent=2)

    return dict_payload

        
def end_power_track(master):
    master.close()