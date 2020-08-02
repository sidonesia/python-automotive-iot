import time
import serial
import sys
import os


class obd_pid:

    _current_obd_data = ""
    _current_pid_data = ""

    _rpm_length     = 11 # (RPM)
    _fuel_sys_stat  = 11 # (fuel system status)
    _speed_length   = 8  # (car speed)
    _engine_code    = 8  # (engine lamp)
    _engine_load    = 8  # (calculated engine load)
    _coolant_temp   = 8  # (Engine coolant temperature)
    _st_fuel_bank1  = 8  # (short term fuel -- Bank 1)
    _lt_fuel_bank1  = 8  # (long term fuel trim bank 1)
    _intake_manif   = 8  # (Intake manifold absolute pressure)
    _timing_adv     = 8  # (timing advance)
    _intake_air_p   = 8  # (intake air pressure)
    _throttle_pos   = 8  # (Throttle position)
    _oxygen_sensor  = 8  # (Oxygen sensors present)
    _oxygen_vol_stf = 8  # (Oxygen sensor 1 ) A vltge, B short term fuel trim

    def __init__(self, params):
        pass
    # end def
    
# end class
