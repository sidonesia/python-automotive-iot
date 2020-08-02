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

        self.car_obd_cmds = params["init_cmds"]
        self.serial_cmd   = params["serial_cmd"]
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
            response.put( "desc" , "GENERAL ERROR" )
            response.put( "status_code" , "9999" )
        # end try
        return response
    # end def

    def run(self):
        is_open  = self.serial_cmd.isOpen()
        # initially write the standard commands
        for serial_cmd in self.car_obd_cmds:
            self.serial_cmd.write( serial_cmd )
            time.sleep( 1 )
        # end for
        obd_resp = self.write({
            "pid_value" : "010C".encode() + " \r\n".encode( )
        })
        time.sleep( 3 )
        for serial_cmd in self.car_obd_cmds:
            self.serial_cmd.write( serial_cmd )
            time.sleep( 1 )
        # end for
        obd_resp = self.write({
            "pid_value" : "010C".encode() + " \r\n".encode( )
        })
        time.sleep( 3 )
        while self.loop_go:
            obd_resp = self.write({
                "pid_value" : "\r\n".encode( )
            })
            time.sleep(config.G_EVENT_LOOP_WAIT)
        # end while
    # end def
# end class
