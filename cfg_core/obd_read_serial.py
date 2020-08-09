import time
import serial
import sys
import os
import threading
import traceback


sys.path.append("cfg_config"    )
sys.path.append("cfg_core"      )
sys.path.append("cfg_startup"   )
sys.path.append("cfg_model_pid" )

from cfg_config    import config
from cfg_core      import helper
from cfg_model_pid import obd_pid_factory

class obd_read_serial(threading.Thread):

    car_obd_cmds   = []
    handler_list   = []
    handler_dict   = {}
    car_pid_buffer = {}
    serial_cmd     = None
    obd_factory    = None
    loop_go        = True

    def __init__(self, params):
        threading.Thread.__init__(self)

        self.car_obd_cmds = params["init_cmds"]
        self.handler_list = params["handler_list"]
        self.handler_dict = params["handler_dict"]
        self.serial_cmd   = params["serial_cmd"]

        self.obd_factory  = obd_pid_factory.obd_pid_factory({})
    # end def

    def read(self, params):
        response = helper.response_msg(
            "SERIAL_SUCCESS", "SERIAL SUCCESS", {} , "0000"
        )
        if not self.serial_cmd.isOpen():
            response.put( "status"      , "SERIAL_FAILED" )
            response.put( "status_code" , "0001" )
            response.put( "desc"        , "CONNECTION FAILED" )
            return response
        # end if
        while self.loop_go:
            try:
                out = ''.encode()
                while self.serial_cmd.inWaiting() > 0:
                    out += self.serial_cmd.read(1)
                # end while
                obd_data = out.decode()
                if obd_data.find(config.G_DATA_HEADER) != -1:
                    pid_proc = self.obd_factory.get_pid_proc({
                        "obd_data" : obd_data 
                    })
                    if pid_proc != None:
                        obd_model = pid_proc["obd_model"]
                        obd_pid   = pid_proc["obd_pid"]
                        if obd_model != None:
                            pid_resp = obd_model._calculate({})
                            status_code = pid_resp.get("status_code")
                            if status_code == "0000":
                                pid_json = pid_resp.get("data")
                                pid_id   = pid_json["pid_handler"]
                                self.handler_dict[pid_id].execute({
                                    "pid_json" : pid_json
                                })
                            # end if
                        else:
                            print (
                                "PID: " + str(obd_pid) +\
                                        " NOT SUPPORTED PLEASE ADD HANDLER"
                            )
                        # end if
                    # end if
                # end if
                time.sleep( config.G_EVENT_LOOP_WAIT )
            except:
                print ( traceback.format_exc() )
                response.put( "status"      , "REALTIME_FAILED" )
                response.put( "desc" , "GENERAL ERROR" )
                response.put( "status_code" , "9999" )
            # end try
        # end while
        return response
    # end def

    def run(self):
        self.read({})
    # end def
# end class
