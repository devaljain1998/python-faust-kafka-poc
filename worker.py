import faust
import json
import ast
from typing import Optional, Type
import time
import socket
import ccloud_lib
import random
import ssl
import certifi

ssl_context = ssl.create_default_context(
    purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where())

config_file = './kafka.config'

# New conf from CC-cloud
conf = ccloud_lib.read_ccloud_config(config_file)

# DEBUG
print(conf)

app = faust.App(
    'kafka_streaming',
    broker='pkc-41p56.asia-south1.gcp.confluent.cloud:9092',
    broker_credentials=faust.SASLCredentials(
        username=conf['sasl.username'],
        password=conf['sasl.password'],
        ssl_context=ssl_context
    ),
    value_serializer='raw',
    topic_replication_factor=3
)        