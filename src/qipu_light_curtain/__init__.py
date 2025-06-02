from pymodbus.client.serial import AsyncModbusSerialClient
from pymodbus.pdu import ModbusResponse
from typing import Optional, List
from enum import Enum

class Parity(Enum):
    NONE = 0
    ODD = 1
    EVEN = 2

class IntelligentGrating:
    def __init__(self, client: AsyncModbusSerialClient, address: int = 0x0F) -> None:
        self.client: AsyncModbusSerialClient = client
        self.address: int = address

    @classmethod
    async def build(cls, port: str, address: int = 0x0F, baudrate: int = 19200, 
                   parity: str = 'E', timeout: int = 1) -> 'IntelligentGrating':
        client: AsyncModbusSerialClient = AsyncModbusSerialClient(
            method='rtu',
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=1,
            bytesize=8,
            timeout=timeout
        )
        instance: IntelligentGrating = cls(client=client, address=address)
        await instance.connect()
        return instance

    async def connect(self) -> bool:
        return await self.client.connect()

    async def close(self) -> None:
        await self.client.close()


    async def set_address(self, new_address: int) -> bool:
        return await self._write_register(0xFFF1, new_address)

    async def set_baud_rate(self, baud: int) -> bool:
        value: int = baud // 100
        return await self._write_register(0xFFF2, value)

    async def set_parity(self, mode: Parity) -> bool:
        return await self._write_register(0xFFF3, mode.value)

    async def reset_defaults(self) -> bool:
        # Broadcast address 0x00
        return await self.client.write_register(address=0xFFF4, value=0x1111, unit=0x00)

    async def _write_register(self, reg: int, value: int, unit: Optional[int] = None) -> bool:
        unit = unit or self.address
        return await self.client.write_register(address=reg, value=value, unit=unit)

    async def _read_registers(self, start: int, count: int) -> ModbusResponse:
        return await self.client.read_holding_registers(start, count, unit=self.address)

    async def read_lowest_blocked(self) -> Optional[int]:
        rr: ModbusResponse = await self._read_registers(0x0040, 1)
        return rr.registers[0] if not rr.isError() else None

    async def read_highest_blocked(self) -> Optional[int]:
        rr: ModbusResponse = await self._read_registers(0x0041, 1)
        return rr.registers[0] if not rr.isError() else None

    async def read_blocked_quantity(self) -> Optional[int]:
        rr: ModbusResponse = await self._read_registers(0x0042, 1)
        return rr.registers[0] if not rr.isError() else None

    async def read_all_light_status(self, count_light_points: int = 80) -> Optional[List[int]]:
        reg_count: int = (count_light_points + 15) // 16
        rr: ModbusResponse = await self._read_registers(0x0000, reg_count)
        if rr.isError():
            return None
        status_bits: List[int] = []
        for reg in rr.registers:
            for i in range(16):
                status_bits.append((reg >> i) & 1)
        return status_bits[:count_light_points]

