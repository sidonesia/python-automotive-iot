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
    handler_dict   = {}
    car_pid_buffer = {}
    serial_cmd     = None
    loop_go        = True

    def __init__(self, params):
        threading.Thread.__init__(self)

        self.handler_list  = params["handler_list"]
        self.handler_dict  = params["handler_dict"]
        self.serial_cmd    = params["serial_cmd"]
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
            for handler_item in self.handler_list:
                handler      = handler_item["pid_handler"]
                pid_value    = handler_item["pid_value"]
                handler_name = handler_item["handler_name"]
                obd_resp     = self.write({
                    "pid_value" : pid_value.encode() + " \r\n".encode()
                })
                time.sleep( config.G_EVENT_LOOP_WAIT )
                count_loop     = 0
                count_loop_max = 1 
                while count_loop < count_loop_max:
                    obd_resp = self.write({
                        "pid_value" : "\r\n".encode( )
                    })
                    time.sleep(config.G_EVENT_LOOP_WAIT)
                    count_loop += 1
                # end while
            # end for
        # end while
    # end def
# end class
