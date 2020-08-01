import obd_interface

obd = obd_interface.obd_interface({
    "car_model":"CAMRY_2000"
})
obd_resp = obd.register_handler({
    "handler"      : None,
    "pid_value"    : "0C",
    "handler_name" : "RPM"
})

obd.start({})
