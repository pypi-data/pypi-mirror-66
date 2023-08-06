import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config
from archippe.datapersistence import DataPersistence
from archippe.myinfluxdbclient import MyInfluxDBClient
from pelops.logging.mylogger import create_logger
from pelops.pubsub.mymqttclient import MyMQTTClient


class TestDataPersistence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
                                 "/tests_unit/config.yaml")
        cls.logger = create_logger(cls.config["logger"], "TestValidateConfig")
        cls.logger.info("start")
        cls.mqtt_client = MyMQTTClient(cls.config["pubsub"], cls.logger)
        cls.mqtt_client.connect()
        cls.influxdb = MyInfluxDBClient(cls.config["data-persistence"]["influx"], cls.logger)

    @classmethod
    def tearDownClass(cls):
        cls.influxdb.client.close()
        cls.mqtt_client.disconnect()
        cls.logger.info("end")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        self.logger.info("test_main")

        dp = DataPersistence(self.config, pubsub_client=self.mqtt_client, no_gui=True)

        prefix_request = self.config["data-persistence"]["topic-request-prefix"]
        prefix_response = self.config["data-persistence"]["topic-response-prefix"]

        for entry in self.config["data-persistence"]["topics"]:
            self.assertNotIn(entry["topic"], self.mqtt_client._topic_handler.keys())
            self.assertNotIn(prefix_response + entry["topic"], self.mqtt_client._topic_handler.keys())
            self.assertNotIn(prefix_request + entry["topic"], self.mqtt_client._topic_handler.keys())

        dp.start()

        for entry in self.config["data-persistence"]["topics"]:
            self.assertIn(entry["topic"], self.mqtt_client._topic_handler.keys())
            self.assertNotIn(prefix_response + entry["topic"], self.mqtt_client._topic_handler.keys())
            self.assertIn(prefix_request + entry["topic"], self.mqtt_client._topic_handler.keys())

        dp.stop()

        for entry in self.config["data-persistence"]["topics"]:
            self.assertNotIn(entry["topic"], self.mqtt_client._topic_handler.keys())
            self.assertNotIn(prefix_response + entry["topic"], self.mqtt_client._topic_handler.keys())
            self.assertNotIn(prefix_request + entry["topic"], self.mqtt_client._topic_handler.keys())


if __name__ == '__main__':
    unittest.main()
