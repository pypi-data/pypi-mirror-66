This software subscribes to mqtt-topics that contain raw sensor data and
publishes e.g. average values for configurable time spans.

Available algorithms are: \* ``Average`` - Vanilla average/mean
implementation. \* ``WeightedAverage`` - The weighted average of all
valid data points within the time window. The weight is the inverse time
difference to the time\_to time stamp. \* ``Count`` - Count how many
valid data points are within the give time window. \* ``Maximum`` - The
maximum value of all valid data points within the time window. \*
``Minimum`` - The minimum value of all valid data points within the time
window.

Alcathous [1]_ is the brother of Copreus. Both are sons of Pelops.
[`wiki <https://en.wikipedia.org/wiki/Alcathous,_son_of_Pelops>`__]

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Alcathous`` is part of the collection of mqtt based microservices
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

    sudo pip3 install pelops alcathous

To update to the latest version add ``--upgrade`` as prefix to the
``pip3`` line above.

Install via gitlab (might need additional packages):

::

    git clone git@gitlab.com:pelops/alcathous.git
    cd alcathous
    sudo python3 setup.py install

This will install the following shell scripts: \* ``alcathous``

The script cli arguments are: \* '-c'/'--config' - config file
(mandatory) \* '--version' - show the version number and exit

YAML-Config
-----------

A yaml [2]_ file must contain three root blocks: \* mqtt - mqtt-address,
mqtt-port, and path to credentials file credentials-file (a file
consisting of two entries: mqtt-user, mqtt-password) \* logger - which
log level and which file to be used \* data-preparation \* general -
parameters for the manager \* methods - mapping of algorithms,
parameters and topic-pub suffix \* datapoints - which topics should be
used and which methods should be applied

::

    mqtt:
        mqtt-address: localhost
        mqtt-port: 1883
        credentials-file: ~/credentials.yaml
        log-level: INFO

    logger:
        log-level: DEBUG
        log-file: alcathous.log

    data-preparation:  # alcathous root node
        no_data_behavior: last_valid  # mute, last_valid, empty_message
        update_cycle: 30  # new values published each ... seconds
        number_worker: 2  # how many worker threads should be spawned to process task queue

        methods:
            - name: avg_5min  # unique name for method
              topic-pub-suffix: avg_5min
              algorithm: avg  # avg - average, wavg - weighted average, count, min, max
              time_window: 5  # use the values from the last ... minutes

            - name: wavg_5min  # unique name for method
              topic-pub-suffix: wavg_5min
              algorithm: wavg  # avg - average, wavg - weighted average, count, min, max
              time_window: 5  # use the values from the last ... minutes

            - name: count_2min  # unique name for method
              topic-pub-suffix: count_2min
              algorithm: count  # avg - average, wavg - weighted average, count, min, max
              time_window: 2  # use the values from the last ... minutes

            - name: min_3min  # unique name for method
              topic-pub-suffix: min_3min
              algorithm: min  # avg - average, wavg - weighted average, count, min, max
              time_window: 3  # use the values from the last ... minutes

            - name: max_3min  # unique name for method
              topic-pub-suffix: max_3min
              algorithm: max  # avg - average, wavg - weighted average, count, min, max
              time_window: 3  # use the values from the last ... minutes

        datapoints:
            - topic-sub: /test/0/raw
              topic-pub-prefix: /test/0/aggregated/
              zero_is_valid: False  # 0 is valid or rejected
              methods: wavg_5min, avg_5min, count_2min, min_3min, max_3min

            - topic-sub: /test/1/raw
              topic-pub-prefix: /test/1/aggregated/
              zero_is_valid: False  # 0 is valid or rejected
              methods: wavg_5min, avg_5min

systemd
-------

-  add systemd example.

For Developers
==============

Getting Started
---------------

The project consists of three main modules: \* ``datapointmanager`` -
loads the config and create all ``Datapoint`` instances. Hosts the main
loop. \* ``datapoint`` - ``Datapoint`` is one of the datapoints in the
config. it holds all data received for the given topic, has its own set
of method instances. \* ``algorithms`` - The configureable algorithms
are then used as data preparation methods in ``DataPoint``. Currently,
two algorithms are implemented: Average and WeightedAverage. The first
one treats all values in a time window equivalent, the later one weights
them with the time span between ``time_from`` and ``time_value``.

``DataPointManager`` has two lists: references to the ``process``
functions from all instantiated methods and a references to the
``purge`` functions from all instantiated ``DataPoint``\ s. The first
list is ordered by an execution cost estimation (highest value first).
Both lists are applied to worker threads (``general.number_worker``) -
please adapt the number of the workers to your needs.

Todos
-----

-  Add better validity check for incoming values
-  ...

Misc
----

The code is written for ``python3`` (and tested with python 3.5 on an
Raspberry Pi Zero with Raspbian Stretch).

`Merge requests <https://gitlab.com/pelops/alcathous/merge_requests>`__
/ `bug reports <https://gitlab.com/pelops/alcathous/issues>`__ are
always welcome.

.. [1]
   The icon used for this project is in fact not Alcathous. Moreover, it
   is Odysseus and resembles perfectly my failed journey to find a
   fitting symbol.

.. [2]
   Currently, pyyaml is yaml 1.1 compliant. In pyyaml On/Off and Yes/No
   are automatically converted to True/False. This is an unwanted
   behavior and deprecated in yaml 1.2. In copreus this autoconversion
   is removed. Thus, On/Off and Yes/No are read from the yaml file as
   strings (see module baseclasses.myconfigtools).

