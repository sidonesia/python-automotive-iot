import time
import serial
import sys
import os

import obd_pid_rpm

class obd_pid_factory:

    _rpm_length = 11

    _obd_model  = {}

    def __init__(self, params):
        self._load_pid_proc({})
    # end def

    def _load_pid_proc(self, params):
        self._obd_model["010C"] = obd_pid_rpm.obd_pid_rpm()
    # end def

    def get_pid_proc(self, params):
        obd_data        = params["obd_data"]
        obd_array       = self._current_obd_data.split(" ")
        pid_header      = obd_array[1]
        pid             = "01" + pid_header
        pid             = pid.upper()
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
