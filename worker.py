import faust
import json
import ast
from typing import Optional, Type
import time

app = faust.App(
    'faust_poc',
    broker='faust-broker',
    value_serializer='raw',
)        