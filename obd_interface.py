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
    writer_threads  = {}
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
        """
            We initialise the connection here with the 
                init string commands
        """
        is_open  = self.serial_cmd.isOpen()
        for init in range( config.G_EVENT_INIT_RETRY ):
            # initially write the standard commands
            for serial_cmd in self.init_cmds:
                self.serial_cmd.write( serial_cmd )
                time.sleep( config.G_EVENT_INIT_TO )
            # end for
            self.serial_cmd.write( config.G_INIT_DATA )
            time.sleep( config.G_EVENT_INIT_CMD_TO )
        # end for
        out = "".encode()
        while self.serial_cmd.inWaiting() > 0:
            out += self.serial_cmd.read(1)
        # end while
        print ( out )
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
        for handler_pid in self.handler_list:
            handler      = handler_pid["pid_handler"]
            pid_value    = handler_pid["pid_value"]
            handler_name = handler_pid["handler_name"]
            full_pid     = pid_value + " \r\n"
            full_pid     = full_pid.encode()
            conn_obd_write_serial = obd_write_serial.obd_write_serial({
                "write_pid"     : full_pid,
                "serial_cmd"    : self.serial_cmd
            })
            self.writer_threads[pid_value] = conn_obd_write_serial
            self.writer_threads[pid_value].start()
        # end for
        self.conn_obd_read_serial = obd_read_serial.obd_read_serial({
            "init_cmds"         : self.init_cmds,
            "handler_list"      : self.handler_list,
            "handler_dict"      : self.handler_dict,
            "serial_cmd"        : self.serial_cmd
        })
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
