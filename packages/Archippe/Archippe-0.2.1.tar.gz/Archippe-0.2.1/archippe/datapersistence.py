from pelops.abstractmicroservice import AbstractMicroservice
from archippe.myinfluxdbclient import MyInfluxDBClient
from archippe.topic import Topic
from archippe.schema.schema import get_schema
import archippe


class DataPersistence(AbstractMicroservice):
    """
    The main entry point for the data persistence service. Creates the Topic-instances and starts/stops them.

    Yaml config:
    data-persistence:
        topics:  # list of topics that should be persisted
            - topic: /test/temperature
              type: float  # float, integer, string, boolean
            - topic: /test/humidity
              type: float  # float, integer, string, boolean
        topic-request-prefix: /dataservice/request  # prefix for each topic to request historic data
        topic-response-prefix: /dataservice/response  # prefix for each topic to publish historic data

    """
    _version = archippe.version  # version of software
    _influx_client = None  # instance of the influxdb client
    _topics = None  # list of instances of archippe.Topic

    def __init__(self, config, pubsub_client=None, logger=None, stdout_log_level=None, no_gui=None):
        """
        Constructor.

        :param config: config yaml structure
        :param pubsub_client: instance of an mymqttclient (optional)
        :param logger: instance of a logger (optional)
        :param no_gui: if False create and control a ui instance
        :param stdout_log_level: if set, a logging handler with target sys.stdout will be added
        """

        AbstractMicroservice.__init__(self, config, "data-persistence", pubsub_client=pubsub_client, logger=logger,
                                      logger_name=__name__, stdout_log_level=stdout_log_level, no_gui=no_gui)

        self._influx_client = MyInfluxDBClient(self._config["influx"], self._logger)

        prefix_request = self._config["topic-request-prefix"]
        prefix_response = self._config["topic-response-prefix"]

        self._topics = []
        for c in self._config["topics"]:
            topic_sub = c["topic"]

            if c["type"].lower() == "integer":
                conversion = int
            elif c["type"].lower() == "float":
                conversion = float
            elif c["type"].lower() == "boolean":
                conversion = bool
            elif c["type"].lower() == "string":
                conversion = str
            else:
                self._logger.error("Unkown type '{}'.".format(c["type"]))
                raise ValueError("Unkown type '{}'.".format(c["type"]))

            topic = Topic(topic_sub, prefix_request + topic_sub, prefix_response + topic_sub, conversion, self._pubsub_client,
                          self._logger, self._influx_client)
            self._topics.append(topic)

    def _start(self):
        for topic in self._topics:
            topic.start()

    def _stop(self):
        for topic in self._topics:
            topic.stop()

    @classmethod
    def _get_schema(cls):
        return get_schema()

    @classmethod
    def _get_description(cls):
        return "Archippe is a data persistence micro service for pelops. It uses influxdb to store incoming values " \
               "and publishes the history a series upon request."

    def runtime_information(self):
        return {}

    def config_information(self):
        return {}


def standalone():
    """Calls the static method DataPersistence.standalone()."""
    DataPersistence.standalone()


if __name__ == "__main__":
    DataPersistence.standalone()
