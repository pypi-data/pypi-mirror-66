
import abc
import asyncio
import logging
import os
import re

from typing import Optional

from qtoggleserver.lib import polled


W1_DEVICES_PATH = '/sys/bus/w1/devices'
SLAVE_FILE_NAME = 'w1_slave'


logger = logging.getLogger(__name__)


class OneWireException(Exception):
    pass


class OneWirePeripheralNotFound(OneWireException):
    def __init__(self, address: str) -> None:
        super().__init__(f'Peripheral @{address} not found')


class OneWirePeripheralAddressRequired(OneWireException):
    def __init__(self) -> None:
        super().__init__('Peripheral address required')


class OneWireTimeout(OneWireException):
    def __init__(self, message: str = 'timeout') -> None:
        super().__init__(message)


class OneWirePeripheral(polled.PolledPeripheral):
    logger = logger

    TIMEOUT = 5  # Seconds

    def __init__(self, address: str, name: str) -> None:
        super().__init__(address, name)

        self._filename: Optional[str] = None
        self._data: Optional[str] = None

    def get_filename(self) -> str:
        if self._filename is None:
            self._filename = self._find_filename()

        return self._filename

    def _find_filename(self) -> str:
        address_parts = re.split('[^a-zA-Z0-9]', self.get_address())
        pat = address_parts[0] + '-0*' + ''.join(address_parts[1:])
        for name in os.listdir(W1_DEVICES_PATH):
            if re.match(pat, name, re.IGNORECASE):
                return os.path.join(W1_DEVICES_PATH, name, SLAVE_FILE_NAME)

        raise OneWirePeripheralNotFound(self.get_address())

    def read(self) -> Optional[str]:
        data = self._data
        self._data = None

        return data

    def read_sync(self) -> Optional[str]:
        filename = self.get_filename()
        self.debug('opening file %s', filename)
        with open(filename, 'rt') as f:
            data = f.read()
            self.debug('read data: %s', data.replace('\n', '\\n'))

        return data

    async def poll(self) -> None:
        try:
            future = self.run_threaded(self.read_sync)
            self._data = await asyncio.wait_for(future, timeout=self.TIMEOUT)

        except asyncio.TimeoutError as e:
            raise OneWireTimeout('Timeout waiting for one-wire data from peripheral') from e

    async def handle_disable(self) -> None:
        await super().handle_disable()
        self._filename = None
        self._data = None


class OneWirePort(polled.PolledPort, metaclass=abc.ABCMeta):
    PERIPHERAL_CLASS = OneWirePeripheral

    def __init__(self, address: str = None, peripheral_name: str = None) -> None:
        autodetected = False
        if address is None:
            address = self.autodetect_address()
            autodetected = True

        super().__init__(address, peripheral_name)

        if autodetected:
            self.debug('autodetected device address %s', address)

    @staticmethod
    def autodetect_address() -> str:
        # TODO make this method look only through specific device types (e.g. temperature sensors)

        names = os.listdir(W1_DEVICES_PATH)
        names = [n for n in names if re.match('^[0-9]{2}-', n)]
        if len(names) == 0:
            raise OneWirePeripheralNotFound('auto')

        if len(names) > 1:
            raise OneWirePeripheralAddressRequired()

        address = re.sub('[^a-f0-9]', '', names[0], re.IGNORECASE)
        address = ':'.join(address[2 * i: 2 * i + 2] for i in range(len(address) // 2))

        return address
