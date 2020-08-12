import os
import sys
import time 
import traceback
import json
import requests

sys.path.append("cfg_config"    )
sys.path.append("cfg_core"      )
sys.path.append("cfg_startup"   )
sys.path.append("cfg_model_pid" )

from cfg_config import config
from cfg_core   import helper

class pid_proc:

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
            pid_handler = params["pid_handler"]
            pid_result  = params["pid_result" ]
            pid_unit    = params["pid_unit"   ]
            pid_raw     = params["pid_raw"    ]

            app_post    = requests.post(
                config.G_AUTOVIA_CORE + config.G_PID_UPDATE_URL,
                data    = {
                    "pid"       : self._pid,
                    "name"      : self._pid_name,
                    "value"     : pid_result,
                    "hex_code"  : pid_raw,
                    "unit"      : pid_unit
                }
            )
            response.put( "data" , {
                "pid"     : self._pid,
                "name"    : self._pid_name,
                "handler" : pid_handler,
                "result"  : pid_result,
                "raw"     : pid_raw,
                "unit"    : pid_unit
            })
        except:
            trace_back_msg = traceback.format_exc() 
            print(  trace_back_msg  )
            response.put( "status"      , "EVENT_EXECUTE_FAILED" )
            response.put( "desc"        , "EXECUTE FAILED" )
            response.put( "status_code" , "9999" )
            response.put( "data"        , { "error_message" : trace_back_msg })
        # end try
        return response
    # end def
# end class
