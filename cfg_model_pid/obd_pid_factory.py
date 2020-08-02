import time
import serial
import sys
import os

import obd_pid_rpm
import obd_pid_speed
import obd_pid_coolant_temp
import obd_pid_engine_code
import obd_pid_engine_load
import obd_pid_fuel_status
import obd_pid_intake_air_pressure
import obd_pid_intake_manifold_abs
import obd_pid_long_term_fuel
import obd_pid_oxygen_present
import obd_pid_short_term_fuel
import obd_pid_throttle_position
import obd_pid_timing_advanced

class obd_pid_factory:

    _rpm_length = 11

    _obd_model  = {}

    def __init__(self, params):
        self._load_pid_proc({})
    # end def

    def _load_pid_proc(self, params):
        self._obd_model["0101"] = obd_pid_engine_code.obd_pid_engine_code({})
        self._obd_model["0103"] = obd_pid_fuel_status.obd_pid_fuel_status({})
        self._obd_model["0104"] = obd_pid_engine_load.obd_pid_engine_load({})
        self._obd_model["0105"] = obd_pid_coolant_temp.obd_pid_coolant_temp({})
        self._obd_model["0106"] = obd_pid_short_term_fuel_bank_one.obd_pid_short_term_fuel_bank_one({})
        self._obd_model["0107"] = obd_pid_long_term_fuel.obd_pid_long_term_fuel({})
        self._obd_model["010B"] = obd_pid_intake_manifold_abs.obd_pid_intake_manifold_abs({})
        self._obd_model["010C"] = obd_pid_rpm.obd_pid_rpm({})
        self._obd_model["010D"] = obd_pid_speed.obd_pid_speed({})
        self._obd_model["010E"] = obd_pid_timing_advanced.obd_pid_timing_advanced({})
        self._obd_model["010F"] = obd_pid_intake_air_pressure.obd_pid_intake_air_pressure({})
        self._obd_model["0111"] = obd_pid_throttle_position.obd_pid_throttle_position({})
        self._obd_model["0113"] = obd_pid_oxygen_present.obd_pid_oxygen_present({})
        self._obd_model["0114"] = obd_pid_short_term_fuel.obd_pid_short_term_fuel({})
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
