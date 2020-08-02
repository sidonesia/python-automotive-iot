import time
import serial
import sys
import os


class obd_pid:

    _current_obd_data = ""
    _current_pid_data = ""

    _rpm_length   = 11
    _speed_length = 8 

    def __init__(self, params):
        pass
    # end def
    
# end class
