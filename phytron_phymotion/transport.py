import serial


class SerialTransport:
    """Minimal transport adapter backed by pyserial.

    Exposes the methods expected by `PhytronProtocol`:
    - write(data)
    - read_until(terminator)
    - read_bytes(n)
    """

    def __init__(self, device, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.5):
        self._serial = serial.Serial(
            port=device,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout,
        )

    def write(self, data):
        if isinstance(data, str):
            data = data.encode('latin1')
        self._serial.write(data)

    def read_until(self, terminator):
        if isinstance(terminator, str):
            terminator = terminator.encode('latin1')

        data = self._serial.read_until(terminator)
        if not data:
            raise TimeoutError('Read timed out')

        # Protocol currently expects iterable integer bytes.
        return list(data)

    def read_bytes(self, n):
        data = self._serial.read(n)
        if not data:
            raise TimeoutError('Read timed out')
        return data
