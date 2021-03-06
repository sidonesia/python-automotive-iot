import time
import serial
import sys
import os
import traceback

sys.path.append("../"           )
sys.path.append("cfg_config"    )
sys.path.append("cfg_core"      )
sys.path.append("cfg_startup"   )
sys.path.append("cfg_model_pid" )

from cfg_config import config
from cfg_core   import helper

import obd_pid


class obd_pid_coolant_temp(obd_pid.obd_pid):


    def __init__(self, params):
        obd_pid.obd_pid.__init__(self, params)
    # end def

    def _set_obd_data(self, params):
        self._current_obd_data = params["obd_data"]
        self._current_pid_data = params["obd_pid" ]
    # end def

    def _get_pid(self, params):
        return _current_pid_data
    # end def

    # A - 40
    def _calculate(self, params):
        response = helper.response_msg(
            "CALCULATE_SUCCESS", "CALCULATE SUCCESS", {} , "0000"
        )
        try:
            hex_value  = self._current_obd_data.replace(
                    "\r","").replace(">","").lstrip().rstrip()
            length_hex = len( hex_value )
            if self._coolant_temp != length_hex:
                response.put( "status"      , "CALCULATE_FAILED" )
                response.put( "status_code" , "0001" )
                response.put( "desc"        , "LENGTH INCORRECT" )
                return response
            # end if
            obd2_hex     = hex_value.split(" ")
            A            = obd2_hex[2]
            int_a        = int("0x" + A , 16 )
            coolant_temp = int_a - 40
            print ( 
                "[" + str(length_hex) + "] " + hex_value +\
                        " [" + str(coolant_temp) + "] COOLANT TEMP"
            )
            response.put( "data" , { 
                "pid_handler": self._current_pid_data, 
                "pid_result" : coolant_temp,
                "pid_raw"    : hex_value,
                "pid_unit"   : "o.C"
            })
        except:
            print ( traceback.format_exc() )
            response.put( "status"      , "CALCULATE_FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "desc"        , "GENERAL ERROR" )
        # end try
        return response
    # end def
# end class
