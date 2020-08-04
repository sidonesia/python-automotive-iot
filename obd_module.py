import obd_interface

obd = obd_interface.obd_interface({
    "car_model":"CAMRY_2000"
})
obd_resp = obd.register_handler({
    "handler"      : None,
    "pid_value"    : "010C",
    "handler_name" : "RPM"
})
obd_resp = obd.register_handler({
    "handler"      : None,
    "pid_value"    : "010D",
    "handler_name" : "SPEED"
})
obd_resp = obd.register_handler({
    "handler"      : None,
    "pid_value"    : "0104",
    "handler_name" : "ENGINE_LOAD"
})

obd.start({"blocking" : True})
