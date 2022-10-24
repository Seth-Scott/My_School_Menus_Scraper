import time
import paho.mqtt.client as mqtt
import os


class MqttClient:
    def __init__(self):
        self.mqtt_broker = os.environ.get("mqttbroker")
        self.mqtt_port = int(os.environ.get("mqttport"))

        self.mqtt_user = os.environ.get("mqttuser")
        self.mqtt_passwd = os.environ.get("mqttpasswd")

        # client name
        self.mqttClient = mqtt.Client("schoolmeal")

        # client username and password
        self.mqttClient.username_pw_set(username=self.mqtt_user, password=self.mqtt_passwd)

        # address and port of MQTT broker
        self.mqttClient.connect(self.mqtt_broker, self.mqtt_port)

        self.mqttClient.loop_start()

    # function called when publish is successful
    def on_publish(self, client, userdata, mid):
        print("MQTT client posted a message to broker")

    def post_message(self, mqtt_message, mqtt_update_interval, topic):
        # message to be published to the MQTT broker
        message = mqtt_message

        # topic, payload encoded in utf-8,
        info = self.mqttClient.publish(
            topic=topic,
            payload=message.encode('utf-8'),
            # TODO qos likely not needed below, delete?
            qos=0,
        )
        # function called when publish is successful
        self.mqttClient.on_publish = self.on_publish

        # Because published() is not synchronous,
        # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
        info.wait_for_publish()
        print(info.is_published())
        time.sleep(mqtt_update_interval)

        # TODO re-configure configuration.YAML file in HA to be visible as a thing (entity?) in the proper way.
        # TODO figure out how to read the string from the custom MQTT aloud in Google Home
        # TODO if (current day) not in (scraped data json) - do not broadcast the stuff






