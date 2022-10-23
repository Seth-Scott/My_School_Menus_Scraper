import time
import paho.mqtt.client as mqtt
import os

mqtt_broker = os.environ.get("mqttbroker")
mqtt_port = int(os.environ.get("mqttport"))

mqtt_user = os.environ.get("mqttuser")
mqtt_passwd = os.environ.get("mqttpasswd")


# function called when publish is successful
def on_publish(client, userdata, mid):
    print("sent a message")


# client name
mqttClient = mqtt.Client("schoolmeal")

# client username and password
mqttClient.username_pw_set(username=mqtt_user, password=mqtt_passwd)

# function called when publish is successful
# mqttClient.on_publish = on_publish

# address and port of MTQQ broker
mqttClient.connect(mqtt_broker, mqtt_port)

mqttClient.loop_start()

while True:
    # message to be published to the MTTQ broker
    message = "sample lunch data 2"

    # topic, payload encoded in utf-8,
    info = mqttClient.publish(
        topic='school/food/lunch',
        payload=message.encode('utf-8'),
        # TODO qos likely not needed below, delete?
        qos=0,
    )

    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)

    # TODO re-configure configuration.YAML file in HA to be visible as a thing (entity?) in the proper way.
    # TODO figure out how to read the string from the custom MQTT aloud in Google Home
    # TODO if (current day) not in (scraped data json) - do not broadcast the stuff