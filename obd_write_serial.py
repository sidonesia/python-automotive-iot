import time
import serial
import sys
import os
import threading
import traceback


sys.path.append("cfg_config"    )
sys.path.append("cfg_core"      )
sys.path.append("cfg_startup"   )
sys.path.append("obd_model_pid" )

from cfg_config import config
from cfg_core   import helper

class obd_write_serial(threading.Thread):

    car_obd_cmds   = []
    handler_list   = []
    car_pid_buffer = {}
    serial_cmd     = None
    loop_go        = True

    def __init__(self, params):
        threading.Thread.__init__(self)

        self.write_pid = params["write_pid"]
    # end def

    def write(self, params):
        response = helper.response_msg(
            "SERIAL_SUCCESS", "SERIAL SUCCESS", {} , "0000"
        )
        if not self.serial_cmd.isOpen():
            response.put( "status"      , "SERIAL_FAILED" )
            response.put( "status_code" , "0001" )
            response.put( "desc"        , "CONNECTION FAILED" )
            return response
        # end if
        pid_value = params["pid_value"]
        try:
            self.serial_cmd.write( pid_value )
            time.sleep( config.G_EVENT_LOOP_WAIT )
        except:
            print ( traceback.format_exc() )
            response.put( "status"      , "REALTIME_FAILED" )
            response.put( "desc"        , "GENERAL ERROR" )
            response.put( "status_code" , "9999" )
        # end try
        return response
    # end def

    def run(self):
        is_open  = self.serial_cmd.isOpen()
        while self.loop_go:
            # initially write the standard commands
            obd_resp = self.write({
                "pid_value" : self.write_pid
            })
            time.sleep( config.G_EVENT_INIT_CMD_TO )
            count_loop     = 0
            count_loop_max = 10
            while count_loop < count_loop_max:
                obd_resp = self.write({
                    "pid_value" : "\r\n".encode( )
                })
                time.sleep(config.G_EVENT_LOOP_WAIT)
                count_loop += 1
            # end while
        # end while
    # end def
# end class
