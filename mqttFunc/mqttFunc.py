
import random
from enum import Enum
from paho.mqtt import client as mqtt_client

class Topic(Enum):
    ALERT_ON = 1
    ALERT_OFF = 2

broker = 'broker.emqx.io'
port = 1883
username = 'group7robot'
password = 'thisisntsecureohwell'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f'python-mqtt-{random.randint(0, 100)}')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def getClient():
    client = connect_mqtt()
    client.loop_start()
    return client;

def subscribe(on_message, topic : Topic):
    if not callable(on_message):
        raise Exception("Subscriber must have a callback for on_message")
    client = connect_mqtt()
    client.on_message = on_message
    client.subscribe(str(topic))
    client.loop_start()
    return client

def publish(client: mqtt_client, msg : str, topic: Topic):
    result = client.publish(str(topic), msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send '{msg}' to topic '{topic}'")
    else:
        print(f"Failed to send message to topic '{topic}'")\

#USAGE EXAMPLE
#def on_message(client, userdata, msg):
#    print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
#subscriber = subscribe(on_message, Topic.ALERT_ON)


#HOME BAKED VERSION

#Begin testing mqtt here

#def on_message(client, userdata, message):
#    print("message received " ,str(message.payload.decode("utf-8")))
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)


#client = mqtt.Client("my_client")
#broker_address = "broker.hivemq.com"
#client.on_message=on_message
#client.connect(broker_address)
#client.loop_start()
#client.subscribe("RobotTest")
#client.publish("RobotTest", "Working")
#time.sleep(4)
#client.loop_stop()