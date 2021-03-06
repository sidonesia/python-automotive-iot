import os
import sys
import time 
import traceback
import json

sys.path.append("cfg_config"    )
sys.path.append("cfg_core"      )
sys.path.append("cfg_startup"   )
sys.path.append("cfg_model_pid" )

from cfg_config import config
from cfg_core   import helper

class evt_rpm:

    _pid      = None
    _pid_name = None

    def __init__(self, params):
        pass
    # end def

    def set_event_pid(self, params):
        self._pid = params["event_pid"]
    # end def

    def set_event_name(self, params):
        self._pid_name = params["event_name"]
    # end def

    def execute(self, params):
        response = helper.response_msg(
            "EVENT_EXECUTE_SUCCESS", "EXECUTE SUCCESS", {} , "0000"
        )
        try:
            result   = params["pid_result"]
            hex_code = params["pid_raw"]
            units    = params["pid_unit"]
            pid_resp = requests.post(
                config.G_AUTOVIA_CORE + config.G_PID_UPDATE_URL,
                data = {
                    "name"      : self._pid_name,
                    "pid"       : self._pid,
                    "value"     : result,
                    "hex_code"  : hex_code,
                    "unit"      : units
                }
            )
            #
            # we might write to database and do other things here 
            #   later, but for now just post to the core
            #   application that provides visuals
            #
        except:
            self.webapp.logger.debug(  traceback.format_exc()  )
            response.put( "status"      , "EVENT_EXECUTE_FAILED" )
            response.put( "desc"        , "EXECUTE FAILED" )
            response.put( "status_code" , "9999" )
        # end try
        return response
    # end def
# end class
