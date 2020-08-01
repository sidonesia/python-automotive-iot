import os
import sys
import copy
import json
import base64
import copy

class response_msg:

    mapping_data = {
        "status" : "message_action",
        "desc"   : "message_desc",
        "data"   : "message_data",
        "status_code"   : "status_code"
    }

    def __init__(self, status, desc, data, status_code):
        self.response = {
            "status"         : status  ,
            "desc"           : desc    ,
            "data"           : data    ,
            "status_code"    : status_code  ,
        }
    # end def

    def put(self, key, value):
        if not (key in self.response):
            raise ValueError('SETTING_NON_EXISTING_FIELD', key, value)
        # end if
        self.response[key] = value
        self.response[self.mapping_data[key]] = value
    #end def

    def get(self, key):
        if not (key in self.response):
            raise ValueError('SETTING_NON_EXISTING_FIELD', key, value)
        # end if
        return self.response[key]
    # end def

    def json(self):
        return self.response
    # end def

    def stringify(self, app=None):
        record_prev = copy.deepcopy( self.response )
        if app != None:
            app.logger.debug( record_prev["message_data"] )
        # end if
        return json.dumps( record_prev )
    # end def

    def http_stringify(self, app=None):
        record_prev = self.stringify(app)
        response    = make_response(
            record_prev, 
            200
        )
        response.mimetype = "application/json"
        return response
    # end def
# end class
