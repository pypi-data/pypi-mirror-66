Archippe is a data persistence micro service for pelops. It uses
influxdb to store incoming values and publishes the history a series
upon request.

For example, ``archippe`` should store all values from topic
``\room\temperature``. For this purpose a series with the same name is
used in influxdb. To retrieve data a message must be sent to
``\dataservice\request\room\temperature``. The message can either be a
single float or a simple json structure. In the first case, the float
value defines the time span in seconds (from=now()-floatvalue,
to=now()). The json structure consists of two timestamps and group-by in
seconds (optional):
``{"from": "2009-11-10T22:00:00Z",  "to": "2009-11-10T23:00:00Z", "group-by": 60}``
(timestamp are inclusive: ``where t<=to and t>=from``; time format is
``%Y-%m-%dT%H:%M:%S.%fZ``, ``group-by`` must be integer). The result
from the query will be published to
``\dataservice\response\room\temperature``. It contains a list of a
values and their timestamp that are available for the given period:
``[{"time": 10, "value": 0.1}, {"time": 11, "value": 0.2},  ...]``.

Request json-message:

::

    {
        "from": "2009-11-10T22:00:00Z", 
        "to": "2009-11-10T23:00:00Z", 
        "group-by": 60  # optional (equal to 0)
    }

Response json-message:

::

    {
        "first": "2009-11-10T22:00:01Z",
        "last": "2009-11-10T22:59:23Z",
        "len": 49,  # entries in data list
        "topic": "/test/example",                 
        "version": 2,  # version of the response format
        "group-by": 0,
        "data": [
            {"time": "2009-11-10T22:00:01Z", "value": 17.98},
            {"time": "2009-11-10T22:01:50Z", "value": 13.98},
            {"time": "2009-11-10T22:03:00Z", "value": 11.98},
            ...
            {"time": "2009-11-10T22:59:23Z", "value": 20.0}
        ]
    }

In `pelops <https://gitlab.com/pelops/pelops>`__ exists a
``HistoryAgent``-class that implements a client side interaction with
this dataservice. A usage example can be found in
`nikippe <https://gitlab.com/pelops/nikippe>`__ - the charts
``CircularChart`` and ``SequentialChart`` rely on ``HistoryAgent`` to
keep track of old data.

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Archippe`` is part of the collection of mqtt based microservices
`pelops <https://gitlab.com/pelops>`__. An overview on the microservice
architecture and examples can be found at
(http://gitlab.com/pelops/pelops).

For Users
=========

Installation Core-Functionality
-------------------------------

Prerequisites for the core functionality are:

::

    sudo apt install python3 python3-pip

Install via pip:

::

    sudo pip3 install archippe

To update to the latest version add ``--upgrade`` as prefix to the
``pip3`` line above.

Install via gitlab (might need additional packages):

::

    git clone git@gitlab.com:pelops/archippe.git
    cd archippe
    sudo python3 setup.py install

This will install the following shell scripts: \* ``archippe``

The script cli arguments are: \* '-c'/'--config' - config file
(mandatory) \* '--version' - show the version number and exit

influxdb
--------

Installation
~~~~~~~~~~~~

Install influx database and client. For example in ubuntu to install
them use:

::

    sudo apt install influxdb influxdb-client

and start the influx client with ``ìnflux``.

Configuration
~~~~~~~~~~~~~

We need to create a database (``archippe``), an admin user, and a
non-admin user with write access to this database.

Within the influx client:

::

    create database archippe
    use archippe
    create user admin with password 'supersecret' with all privileges
    create user pelops with password 'secret'
    grant all on archippe to pelops
    exit

YAML-Config
-----------

A yaml [1]_ file must contain four root blocks:

-  mqtt - mqtt-address, mqtt-port, and path to credentials file
   credentials-file (a file consisting of the entry ``mqtt`` with two
   sub-entries ``mqtt-user``, ``mqtt-password``)  [2]_
-  logger - which log level and which file to be used
-  influx - influx-address, influx-port, and path to credentials file
   credentials-file (a file consisting of the entry ``influx`` with two
   sub-entries ``influx-user``, ``influx-password``)  [3]_
-  data-persistence

   -  topics - list of topics that should be persisted and their types
   -  prefix - prefix for each topic to request historic data
   -  response - prefix for each topic to publish historic data

::

    mqtt:
        mqtt-address: localhost
        mqtt-port: 1883
        credentials-file: ~/credentials.yaml
        log-level: INFO

    logger:
        log-level: DEBUG
        log-file: archippe.log

    data-persistence:
        influx:
            influx-address: homebase.w.strix.at
            influx-port: 8086
            credentials-file: ~/credentials.yaml
            database: archippe  # influx database
            log-level: INFO
        topics:  # list of topics that should be persisted
            - topic: /test/temperature
              type: float  # float, integer, string, boolean
            - topic: /test/humidity
              type: float  # float, integer, string, boolean
        topic-request-prefix: /dataservice/request  # prefix for each topic to request historic data
        topic-response-prefix: /dataservice/response  # prefix for each topic to publish historic data

systemd
-------

-  add systemd example.

For Developers
==============

Getting Started
---------------

This service consists of two classes ``DataPersistence`` and ``Topic``.
For each topic that should be peristet an instance of ``Topic`` is
created in ``DataPersistence``.

Changes in the yaml structure must be mirrored in
``archippe/schema.py``. It is a json-schema that verifies the provided
yaml.

MyInfluxDBClient
----------------

Wrapper for influxdb.InfluxDBClient. Takes care initializing and writing
of single datapoints to the db.

Next to the raw connectivity, this client provides two methods: \*
``write_point``: Write a single measurement value to the database
(wrapper for influxdb.write\_points method). \* ``write_points``: Write
a list of entries (timestamp, value) into the measurement of the
database.

Todos
-----

-  none currently planed

Misc
----

The code is written for ``python3`` (and tested with python 3.5 on an
Raspberry Pi Zero with Raspbian Stretch).

`Merge requests <https://gitlab.com/pelops/archippe/merge_requests>`__ /
`bug reports <https://gitlab.com/pelops/archippe/issues>`__ are always
welcome.

.. [1]
   Currently, pyyaml is yaml 1.1 compliant. In pyyaml On/Off and Yes/No
   are automatically converted to True/False. This is an unwanted
   behavior and deprecated in yaml 1.2. In copreus this autoconversion
   is removed. Thus, On/Off and Yes/No are read from the yaml file as
   strings (see module baseclasses.myconfigtools).

.. [2]
   Mqtt and influx credentials can be stored in one file.

.. [3]
   Mqtt and influx credentials can be stored in one file.

