import time
import serial
import sys
import os

sys.path.append("cfg_config"    )
sys.path.append("cfg_core"      )
sys.path.append("cfg_startup"   )
sys.path.append("obd_model_pid" )

from cfg_config import config
from cfg_core   import helper

import obd_write_serial
import obd_read_serial

class obd_interface:

    loop_go         = True
    init_cmds       = []
    handler_list    = []
    handler_dict    = {}
    conn_obd_serial = None

    """
        Here we get the initialisation commands given a specific 
            car that we put in there. You can add your own initialisation
            commands for your car in the configuration
    """
    def __init__(self, params):
        car_model            = params["car_model"]
        self.init_cmds       = config.G_CAR_INIT_CMDS[car_model]
        self.serial_cmd   = serial.Serial(
            port     = config.G_SERIAL_COMM,
            baudrate = config.G_SERIAL_PORT,
            parity   = config.G_PARITY,
            stopbits = config.G_STOPBITS,
            bytesize = config.G_BYTESIZE,
            timeout  = 5
        )
    # end def

    """
        Here we register the event handlers that are triggered 
            when data is found on the serial connecter given new data 
            for a specific PID is available
    """
    def register_handler(self, params):
        response = helper.response_msg(
            "REGISTER_SUCCESS", "REGISTER SUCCESS", {} , "0000"
        )        
        try:
            handler        = params["handler"     ]
            pid_value      = params["pid_value"   ]
            handler_name   = params["handler_name"]

            if handler_name in self.handler_dict:
                response.put( "status"      , "REGISTER_FAILED" )
                response.put( "status_desc" , "DUPLICATE FOUND" )
                response.put( "status_code" , "0001" )
                return response
            # end if
            handler_obj = {
                "pid_handler"   : handler,
                "pid_value"     : pid_value,
                "handler_name"  : handler_name
            }
            self.handler_list.append( handler_obj )
            self.handler_dict[pid_value] = handler_obj
        except:
            response.put( "status"      , "REGISTER_FAILED" )
            response.put( "status_desc" , "GENERAL ERROR" )
            response.put( "status_code" , "9999" )
        # end try
        return response
    # end def

    """
        Main event loop, will annotate later
    """
    def start(self, params):
        self.conn_obd_write_serial = obd_write_serial.obd_write_serial({
            "init_cmds"    : self.init_cmds,
            "handler_list" : self.handler_list,
            "handler_dict" : self.self.handler_dict,
            "serial_cmd"   : self.serial_cmd
        })
        self.conn_obd_read_serial = obd_read_serial.obd_read_serial({
            "init_cmds"    : self.init_cmds,
            "handler_list" : self.handler_list,
            "handler_dict" : self.self.handler_dict,
            "serial_cmd"   : self.serial_cmd
        })
        self.conn_obd_write_serial.start()
        self.conn_obd_read_serial.start()
        blocking = params["blocking"]
        if not blocking:
            self.loop_go = False
        # end if
        while self.loop_go:
            time.sleep(config.G_EVENT_LOOP_WAIT)
        # end while
    # end def

    def stop(self, params):
        self.loop_go = False
    # end def
# end class
