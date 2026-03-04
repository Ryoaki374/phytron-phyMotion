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

from phytron_phymotion.message import AxisMessage, AbstractResponse, Response

PARAMETER_MICROSTEP = 45
PARAMETER_CURRENT = 41
PARAMETER_STOP_CURRENT = 40
PARAMETER_FREQUENCY = 14
PARAMETER_ENABLE_BOOST = 17
PARAMETER_BOOST_CURRENT = 42
PARAMETER_CURRENT_DELAY_TIME = 43
PARAMETER_START_STOP_FREQUENCY = 4

class ParameterMessage(AxisMessage):
    def init(self):
        self._axis_cmd = ''

    def set_parameter(self, id, value):
        self._is_valid_id(id)
        self._axis_cmd = 'P' + str(id).zfill(2) + '=' + str(value)

    def get_parameter(self, id):
        self._is_valid_id(id)
        self._axis_cmd = 'P' + str(id).zfill(2) + 'R'

    def _is_valid_id(self, id):
        if not isinstance(id, int):
            raise TypeError("number must be of instance integer")

        if id < 0 or id > 100:
            raise ValueError("number must be in range [0, 99]")

    def create_response(self, raw_response):
        return ParameterResponse(Response(raw_response))

class ParameterResponse(AbstractResponse):
    pass
