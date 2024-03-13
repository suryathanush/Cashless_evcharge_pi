import digitalio
import board

deviceId = 123456

dashboard_url = "3.211.231.196:3000"

#relay pin
relay_pin = digitalio.DigitalInOut(board.D4)
relay_pin.direction = digitalio.Direction.OUTPUT

#Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

red_LED = digitalio.DigitalInOut(board.D17)
green_LED = digitalio.DigitalInOut(board.D27)
orange_LED = digitalio.DigitalInOut(board.D22)

#set direction for pins
cs_pin.direction = digitalio.Direction.OUTPUT
dc_pin.direction = digitalio.Direction.OUTPUT
reset_pin.direction = digitalio.Direction.OUTPUT

red_LED.direction = digitalio.Direction.OUTPUT
green_LED.direction = digitalio.Direction.OUTPUT
orange_LED.direction = digitalio.Direction.OUTPUT

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

#screen rotation
Rotation = 180

font_path = '/home/surya/evcharger/fotns/OpenSans-Bold.ttf'
font_path_2 = '/home/surya/evcharger/fotns/OpenSans-ExtraBold.ttf'
font_size = 12
mqtt_broker = "3.211.231.196"
mqtt_port = 1883

# Create the topic string.
subscribe_topic = "Control"
publish_topic = "Update"

cred_file_path = '/home/surya/evcharger/creds.txt'

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 10

# time for idle turn on
idle_time_in_sec = 300

cutoff_current = 0.5 # in Ampere

prev_idle_time = 0