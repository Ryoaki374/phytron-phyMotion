# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

def compute_chksum(data):
    chksum = 0
    for el in data:
        chksum = ord(el) ^ chksum
          
    return hex(chksum)[2:].upper().zfill(2)

class Message(object):
    SEPARATOR = chr(0x3A) # 0x3a_h = str(':')
    STX = chr(0x02)
    ETX = chr(0x03)
    
    def __init__(self):
        self.addr = '0'
        self.cmd = ''
        self.chksum = 'XX'
    
    def set_cmd(self, cmd):
        self.cmd = str(cmd)
        
    def get_cmd(self):
        return self.cmd
    
    def set_checksum(self, chksum):
        self.chksum = chksum
        
    def get_checksum(self):
        return self.chksum
    
    def compute_checksum(self):
        return compute_chksum(list("".join([self.addr, self.cmd, self.SEPARATOR])))
        
    def set_address(self, addr):
        if isinstance(addr, int):
            if addr in range(0, 16):
                addr = hex(addr)[2:]
            else:
                raise ValueError("address must be either 0...15 or '@'")

        if not isinstance(addr, str):
            raise ValueError("address must either be an integer or a string")
                
        if addr.upper() in "1234567890ABCEDF@" and len(addr) == 1:
            self.addr = addr.upper()
        else:
            raise ValueError("address must be either 0...9, A...F or '@'")
    
    def get_address(self):
        return self.addr
    
    def get_raw(self):
        return "".join([self.STX, self.addr, self.cmd, self.SEPARATOR, self.chksum, self.ETX])
    
    def __str__(self):
        return self.get_raw()

    def __repr__(self):
        return self.__str__()
    
class Response(object):
    
    ACK = chr(0x06)
    NAK = chr(0x15)
    
    def __init__(self, response_array):
        if len(response_array) > 5:
            self.stx = response_array[0]
            self.status = response_array[1]
            self.etx = response_array[-1]
            self.chksum = "".join(response_array[-3:-1])

            if response_array[2] == Message.SEPARATOR:
                self.response = ''
            elif response_array[-4] == Message.SEPARATOR:
                self.response = "".join(response_array[2:-4])
            else:
                raise ValueError("Invalid response given (Separator ':' not found)")
        else:
            raise ValueError("Invalid response given (Response too short: "+str(len(response_array))+")")

    def get_response(self):
        return self.response
    
    def get_raw(self):
        return "".join([self.stx, self.status, self.response, Message.SEPARATOR, self.chksum, self.etx])
    
    def compute_checksum(self):
        return compute_chksum(list("".join([self.status, self.response, Message.SEPARATOR])))
    
    def is_successful(self):
        return self.status == self.ACK
    
    def get_checksum(self):
        return self.chksum
    
    def is_valid(self):
        if self.stx is not Message.STX or self.etx is not Message.ETX:
            return False
        if not self.compute_checksum() == self.chksum:
            return False
        
        return True
    
    def __str__(self):
        return self.get_raw()
    
class AbstractMessage(object):
    def __init__(self):
        self.msg = Message()
        self.init()
        
    def init(self):
        pass
        
    def get_message(self):
        self._prepare_message()
        return self.msg

    def _prepare_message(self):
        pass

    def create_response(self, response):
        raise NotImplementedError()
    
    def __str__(self):
        return "".join([self.__class__.__name__, ':', str(self.msg)])

class AxisMessage(AbstractMessage):
    def __init__(self, cmd = ''):
        self._module = 0
        self._axis = 0
        self._axis_cmd = cmd
        super(AxisMessage, self).__init__()

    def set_module(self, module):
        if not isinstance(module, int):
            raise TypeError("module must be of instance integer")

        if not module >= 0:
            raise ValueError("module must not be negative")

        self._module = module

    def set_axis(self, axis):
        if not isinstance(axis, int):
            raise TypeError("axis must be of instance integer")

        if not axis >= 0:
            raise ValueError("axis must not be negative")

        self._axis = axis

    def get_axis(self):
        return self._axis

    def get_module(self):
        return self._module

    def _prepare_message(self):
        self.msg.set_cmd("".join(['M', str(self._module), '.', str(self._axis), self._axis_cmd]))

    def create_response(self, response):
        return Response(response)
    
class AbstractResponse(object):
    def __init__(self, response):
        if isinstance(response, (str, list)):
            response = Response(response)
        
        if not isinstance(response, Response):

            raise TypeError("No Response given")
            
        self.resp = response

    def get(self):
        return self.resp.get_response()

    def get_response(self):
        return self.resp
    
    def is_valid(self):
        return self.resp.is_valid()
    
    def is_successful(self):
        return self.resp.is_successful()

    def get_bool(self):
        return self.get() == 'E'

    def __bool__(self):
        return self.get_bool()

    __nonzero__ = __bool__

    def __str__(self):
        return "".join([self.__class__.__name__, ':', str(self.resp)])

