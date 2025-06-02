# Qipu Light Curtain

A Python library for interfacing with Qipu Light Curtain devices using Modbus RTU protocol.

## Usage

### Basic Usage

```python
import asyncio
from qipu_light_curtain import IntelligentGrating, Parity

async def main():
    # Create a new instance using the build method
    grating = await IntelligentGrating.build(
        port="/dev/ttyUSB0",  # Serial port
        address=0x0F,         # Device address
        baudrate=19200,       # Baud rate
        parity='E',           # Parity (E for Even)
        timeout=1             # Timeout in seconds
    )

    try:
        # Read the lowest blocked beam
        lowest = await grating.read_lowest_blocked()
        print(f"Lowest blocked beam: {lowest}")

        # Read the highest blocked beam
        highest = await grating.read_highest_blocked()
        print(f"Highest blocked beam: {highest}")

        # Read the number of blocked beams
        quantity = await grating.read_blocked_quantity()
        print(f"Number of blocked beams: {quantity}")

        # Read the status of all light beams
        status = await grating.read_all_light_status()
        print(f"Light beam status: {status}")

        # Change device settings
        await grating.set_address(0x10)        # Change device address
        await grating.set_baud_rate(9600)      # Change baud rate
        await grating.set_parity(Parity.EVEN)  # Change parity

    finally:
        # Always close the connection when done
        await grating.close()

# Run the async main function
asyncio.run(main())
```

### Using with an Existing Client

```python
import asyncio
from pymodbus.client.serial import AsyncModbusSerialClient
from qipu_light_curtain import IntelligentGrating

async def main():
    # Create your own Modbus client
    client = AsyncModbusSerialClient(
        method='rtu',
        port="/dev/ttyUSB0",
        baudrate=19200,
        parity='E',
        stopbits=1,
        bytesize=8,
        timeout=1
    )

    # Create grating instance with existing client
    grating = IntelligentGrating(client=client, address=0x0F)

    try:
        # Connect the client
        await grating.connect()

        # Use the grating as normal
        status = await grating.read_all_light_status()
        print(f"Light beam status: {status}")

    finally:
        await grating.close()

asyncio.run(main())
```

## API Reference

### IntelligentGrating

#### Initialization

```python
# Using build method (recommended)
grating = await IntelligentGrating.build(
    port: str,
    address: int = 0x0F,
    baudrate: int = 19200,
    parity: str = 'E',
    timeout: int = 1
)

# Using existing client
grating = IntelligentGrating(
    client: AsyncModbusSerialClient,
    address: int = 0x0F
)
```

#### Methods

- `connect() -> bool`: Connect to the device
- `close() -> None`: Close the connection
- `set_address(new_address: int) -> bool`: Change device address
- `set_baud_rate(baud: int) -> bool`: Change baud rate
- `set_parity(mode: Parity) -> bool`: Change parity setting
- `reset_defaults() -> bool`: Reset device to default settings
- `read_lowest_blocked() -> Optional[int]`: Read lowest blocked beam
- `read_highest_blocked() -> Optional[int]`: Read highest blocked beam
- `read_blocked_quantity() -> Optional[int]`: Read number of blocked beams
- `read_all_light_status(count_light_points: int = 80) -> Optional[List[int]]`: Read status of all light beams

### Parity Enum

```python
class Parity(Enum):
    NONE = 0
    ODD = 1
    EVEN = 2
```

## License
