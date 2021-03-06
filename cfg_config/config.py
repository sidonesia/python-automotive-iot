import serial

##################### CAR SPECIFIC DETAILS #####################


# ADD YOUR SPECIFIC STRINGS FOR YOUR CAR HERE 
G_CAMRY_INIT=[
    "ATZ \r\n".encode(),
    "ATIB 96 \r\n".encode(),
    "ATIIA 13 \r\n".encode(),
    "ATSH8113F1 \r\n".encode(),
    "ATSH8113F1 \r\n".encode(),
    "ATSP A4 \r\n".encode(),
    "ATSW00 \r\n".encode()
]

# SELECT WHICH CAR YOU WANT TO USE FOR INITIALIZATION
G_CAR_INIT_CMDS = {
    "CAMRY_2000" : G_CAMRY_INIT
}



#################### APPLICATION SPECIFIC DETAILS ####################

G_EVENT_LOOP_WAIT    = 0.25
G_EVENT_INIT_TO      = 1
G_EVENT_INIT_CMD_TO  = 3
G_EVENT_INIT_RETRY   = 2
G_GENERAL_ERROR      = "9999"
G_AUTOVIA_CORE       = "http://0.0.0.0:5000"
G_PID_UPDATE_URL     = "/v1/api/obd/realtime/pid-update"

#################### SERIAL CONNECTIVITY ####################

G_SERIAL_COMM        = "/dev/rfcomm0"
G_SERIAL_PORT        = 38400
G_PARITY             = serial.PARITY_ODD
G_STOPBITS           = serial.STOPBITS_TWO
G_BYTESIZE           = serial.SEVENBITS
G_DATA_HEADER        = "41"
G_SERIAL_TIMEOUT     = 5
G_INIT_DATA          = "010C \r\n".encode()
