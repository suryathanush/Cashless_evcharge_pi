from paho.mqtt import client as mqtt_client
import time, json
import config
import display

command = "stop"
connection_flag = False

def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(' = ')
            credentials[key] = value
    return credentials

credentials = read_credentials(config.cred_file_path)

username = credentials.get('username')
clientId = str(config.deviceId)
password = credentials.get('password')

def on_connect(client, userdata, flags, rc):
    global connection_flag
    if rc == 0:
        print("Connected to MQTT Broker!")
        connection_flag = True
    else:
        print("Failed to connect, return code %d\n", rc)
        connection_flag = False


def connect_mqtt():
    # Set Connecting Client ID
    client = mqtt_client.Client(clientId)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(config.mqtt_broker, config.mqtt_port)
    return client


def on_disconnect(client, userdata, rc):
    global connection_flag
    connection_flag = False
    print("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, config.FIRST_RECONNECT_DELAY
    while reconnect_count < config.MAX_RECONNECT_COUNT:
        print("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print("Reconnected successfully!")
            
        except Exception as err:
            print("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= config.RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, config.MAX_RECONNECT_DELAY)
        reconnect_count += 1
    print("Reconnect failed after %s attempts. Exiting...", reconnect_count)
    return False

def publish(client, message):
     msg_count = 1
     while True:
        time.sleep(1)
        result = client.publish(config.publish_topic, message)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{config.publish_topic}`")
            return True
        else:
            print(f"Failed to send message to topic {config.publish_topic}")
            return False
         
def subscribe(client: mqtt_client):
    global command
    def on_message(client, userdata, msg):
        global command
        data = json.loads(msg.payload.decode())
        print(data)
        #print(type(data))
        if(data["deviceID"]==config.deviceId):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            
            if(data["Command"]=="start"):
                print("command start recieved")
                command = "start"
                config.prev_idle_time = time.time()
                config.relay_pin.value = False
                config.red_LED.value = True
                config.green_LED.value = False
                config.orange_LED.value = False
            elif(data["Command"]=="stop"):
                print("command stop recieved")
                command = "stop"
                display.draw_image("/home/surya/evcharger/qr.png")
                config.relay_pin.value = True
                config.red_LED.value = False
                config.green_LED.value = True
                config.orange_LED.value = False
            else:
                print(f'command corrupted : received -> {data["Command"]}')

    client.subscribe(config.subscribe_topic)
    client.on_message = on_message