def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(' = ')
            credentials[key] = value
    return credentials

file_path = '/home/surya/evcharger/creds.txt'
credentials = read_credentials(file_path)

username = credentials.get('username')
clientId = credentials.get('clientId')
password = credentials.get('password')

# Example: print the values
print(f"Username: {username}")
print(f"Client ID: {clientId}")
print(f"Password: {password}")

import paho.mqtt.publish as publish
import psutil
import string

# The ThingSpeak Channel ID.
# Replace <YOUR-CHANNEL-ID> with your channel ID.
channel_ID = "2410152"

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt3.thingspeak.com"

t_transport = "websockets"
t_port = 80

# Create the topic string.
topic = "channels/" + channel_ID + "/publish"

while (True):

    # get the system performance data over 20 seconds.
    cpu_percent = psutil.cpu_percent(interval=20)
    ram_percent = psutil.virtual_memory().percent

    # build the payload string.
    payload = "field1=" + str(cpu_percent) + "&field2=" + str(ram_percent)

    # attempt to publish this data to the topic.
    try:
        print ("Writing Payload = ", payload," to host: ", mqtt_host, " clientID= ", clientId, " User ", username, " PWD ", password)
        publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=clientId, auth={'username':username,'password':password})
    except (keyboardInterrupt):
        break
    except Exception as e:
        print (e) 