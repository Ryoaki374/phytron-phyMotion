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

from .protocol import PhytronProtocol

from .message import AxisMessage

from .messages.clear import ClearMessage
from .messages.parameter import ParameterMessage
from .messages.isholding import IsHoldingMessage
from .messages.endphase import EndPhaseMessage
from .messages.arbitrary import ArbitraryMessage


class PhytronDriver(object):
    """Simple phyMotion driver without external framework dependencies."""

    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = PhytronProtocol()

        self._transport = transport
        self._protocol = protocol
        self._module, self._axis = 0, 0

    def set_axis(self, module, axis):
        self._module, self._axis = module, axis

    def send_message(self, message, set_axis=True):
        if isinstance(message, AxisMessage) and set_axis:
            message.set_axis(self._axis)
            message.set_module(self._module)

        return self._protocol.query(self._transport, message)

    def msg(self, msg):
        message = ArbitraryMessage()
        message.set_message(msg)
        return self.send_message(message, set_axis=False)

    def clear_bus(self):
        self._protocol.clear(self._transport)

    def clear(self):
        self.send_message(ClearMessage())

    def clear_axis(self):
        return self.send_message(AxisMessage('C'))

    def _signum(self, integer):
        if integer >= 0:
            return '+'
        return '-'

    def move_relative(self, rel):
        self.send_message(AxisMessage(self._signum(rel) + str(abs(rel))))

    def move_absolute(self, position):
        self.send_message(AxisMessage('A' + self._signum(position) + str(abs(position))))

    def get_absolute_counter(self):
        msg = ParameterMessage()
        msg.get_parameter(21)
        resp = self.send_message(msg)
        return resp.get() if resp is not None else None

    def stop(self):
        self.send_message(AxisMessage('S'))

    def stopped(self):
        return self.send_message(IsHoldingMessage())

    def has_stepping_errors(self):
        return self.send_message(AxisMessage('==M'))

    def set_parameter(self, id, value):
        msg = ParameterMessage()
        msg.set_parameter(id, value)
        self.send_message(msg)

    def get_parameter(self, id):
        msg = ParameterMessage()
        msg.get_parameter(id)
        return self.send_message(msg)

    def get_position(self):
        resp = self.get_parameter(21)
        return resp.get() if resp is not None else None

    def set_position(self, position):
        return self.move_absolute(position)

    def activate_endphase(self):
        msg = EndPhaseMessage()
        msg.activate()
        self.send_message(msg)

    def deactivate_endphase(self):
        msg = EndPhaseMessage()
        msg.deactivate()
        self.send_message(msg)
