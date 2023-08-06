import os
from konduit import PythonConfig, ServingConfig, InferenceConfiguration
from konduit.utils import default_python_path
from konduit import PythonStep
from konduit.server import Server
import sys
import numpy as np
import time
from utils import to_base_64
from konduit.client import Client
from PIL import Image
from utils import to_base_64

python_code = """
import numpy as np 
output = np.array(int("123"))
"""

python_config = PythonConfig(
    python_code=python_code,
    python_inputs={"int_string": "STR"},
    python_outputs={"output": "NDARRAY"}
)

onnx_step = PythonStep().step(python_config)

server = Server(
    steps=onnx_step,
    serving_config=ServingConfig(http_port=255)
)

server.start()
time.sleep(30)
client = Client(
    input_type='JSON',
    return_output_type='JSON',
    endpoint_output_type="JSON",
    port=255
)
a = client.predict(
    {"int_string": "123"}
)
print(a)

server.stop()