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

from e21_util.transport import Serial
from e21_util.log import get_sputter_logger
from e21_util.ports import Ports
from .protocol import PhytronProtocol
from .driver import PhytronDriver

class PhytronFactory:

    def get_logger(self):
        logger = logging.getLogger('phytron_phymotion')
        logger.addHandler(logging.NullHandler())
        return logger

    def create_driver(self, device=None, logger=None):
        if logger is None:
            logger = self.get_logger()

        if device is None:
            device = os.environ.get('PHYTRON_DEVICE', '/dev/ttyUSB0')

        protocol = PhytronProtocol(logger=logger)
        transport = SerialTransport(device, 115200, 8, 'N', 1, 0.5)
        return PhytronDriver(transport, protocol)
