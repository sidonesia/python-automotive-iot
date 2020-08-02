import time
import serial
import sys
import os

import obd_pid_rpm
import obd_pid_speed

class obd_pid_factory:

    _rpm_length = 11

    _obd_model  = {}

    def __init__(self, params):
        self._load_pid_proc({})
    # end def

    def _load_pid_proc(self, params):
        self._obd_model["010C"] = obd_pid_rpm.obd_pid_rpm({})
        self._obd_model["010D"] = obd_pid_speed.obd_pid_speed({})
    # end def

    def get_pid_proc(self, params):
        obd_data        = params["obd_data"]
        hex_value       = obd_data.replace("\r","").replace(">","").lstrip().rstrip()
        obd_array       = hex_value.split(" ")
        if len( obd_array ) < 2:
            return None
        # end if
        pid_header      = obd_array[1]
        pid             = "01" + pid_header
        pid             = pid.upper()
        if not pid in self._obd_model:
            return None
        # end if
        obd_model_proc  = self._obd_model[pid]
        obd_model_proc._set_obd_data({
            "obd_data"  : obd_data,
            "obd_pid"   : pid
        })
        return {
            "obd_model" : obd_model_proc,
            "obd_pid"   : pid
        }
    # end def
# end class
