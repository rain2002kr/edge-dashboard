import paho.mqtt.client as mqtt
import os
import json
from influxdb import InfluxDBClient
import time
import logging
import json
print("start")

with open('/cfg-data/env-config.json', 'r') as data:
    obj = json.load(data)

MQTT_BROKER_SERVER = obj['env']['MQTT_BROKER_SERVER']
MQTT_TOPIC = obj['env']['MQTT_TOPIC']
MQTT_USER = obj['env']['MQTT_USER']
MQTT_PASSWORD = obj['env']['MQTT_PASSWORD']
INFLUXDB_IP = obj['env']['INFLUXDB_IP']
INFLUXDB_DATABASE = obj['env']['INFLUXDB_DATABASE']

# The callback for when the client receives a CONNECT response from the server.
# after connecting subscribe to the southbound topic
def mqtt_on_connect(client, userdata, flags, rc):    
    logging.info("Connected with result code "+str(rc))
    mqtt_client.subscribe(MQTT_TOPIC)
    logging.info("subscribed to %s",MQTT_TOPIC)

# The callback for when a message is received from the server.
# the southbound sends the data as a json to the databus
# the incomming message is converted to a format that influxdb understands and send to influxdb
# the topic name is used as measurment name
def mqtt_on_message(client, userdata, msg):
    logging.info("%s     %s",msg.payload,msg.topic)
    payload = json.loads(msg.payload)
    logging.info(payload['Value'])
    json_body = [
        {
            "measurement" : msg.topic,
            "fields": {
                "value" : payload['Value']                
            }
        }
    ]
    logging.info(json_body)
    influx_client.write_points(json_body)

# on disconnect from the databus print the error code to log
def mqtt_on_disconnect(client, userdata, rc):
    logging.info("disconnected, but why?"+str(rc))
    if rc == 1:
        mqtt_protocol = mqtt.MQTTv311


# configure Logging
logging.basicConfig(level=logging.INFO)
logging.info("start of python")

# wait 5 seconds so the influxdb container is already up and running fine 
time.sleep(5)

# MQTT Client Setup
mqtt_protocol = mqtt.MQTTv31

# create a new mqtt_client
mqtt_client = mqtt.Client(clean_session=True,protocol = mqtt_protocol)
# set callback functions 
mqtt_client.on_connect = mqtt_on_connect
mqtt_client.on_message = mqtt_on_message
mqtt_client.on_disconnect = mqtt_on_disconnect

# set mqtt username and password
mqtt_client.username_pw_set(MQTT_USER,MQTT_PASSWORD)
# connect to the databus
mqtt_client.connect(MQTT_BROKER_SERVER, 1883, 60)

#create a new influx_client and connect to influxDB
influx_client = InfluxDBClient(INFLUXDB_IP,8086,"root","root",INFLUXDB_DATABASE)

#create a new database and use this database
influx_client.create_database(INFLUXDB_DATABASE)
influx_client.switch_database(INFLUXDB_DATABASE)

logging.info("influx connected")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_forever()