import time
import serial
import sys
import os


class obd_pid:

    loop_go      = True
    init_cmds    = []
    handler_list = []

    def __init__(self, params):
        car_model      = params["car_model"]
        self.init_cmds = config.G_CAR_INIT_CMDS[car_model]
    # end def
    
    def register_handler(self, params):
        handler   = params["handler"  ]
        pid_value = params["pid_value"]
    # end def

    def start(self, params):
        while self.loop_go:
            time.sleep(0.25)
        # end while
    # end def

    def stop(self, params):
        self.loop_go = False
    # end def
# end class
