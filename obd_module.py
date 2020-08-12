import os
import sys
import time
import traceback
import json
import requests

sys.path.append("cfg_config"       )
sys.path.append("cfg_core"         )
sys.path.append("cfg_startup"      )
sys.path.append("cfg_model_pid"    )
sys.path.append("modules"          )
sys.path.append("modules/pid_proc" )

from cfg_config import config
from cfg_core   import helper
from pid_proc   import pid_proc

import obd_interface

obd = obd_interface.obd_interface({
    "car_model":"CAMRY_2000"
})
obd_resp = obd.register_handler({
    "handler"      : pid_proc.pid_proc(),
    "pid_value"    : "010C",
    "handler_name" : "RPM"
})
obd_resp = obd.register_handler({
    "handler"      : pid_proc.pid_proc(),
    "pid_value"    : "010D",
    "handler_name" : "SPEED"
})
obd_resp = obd.register_handler({
    "handler"      : pid_proc.pid_proc(),
    "pid_value"    : "0104",
    "handler_name" : "ENGINE_LOAD"
})
obd.start({"blocking" : True})
