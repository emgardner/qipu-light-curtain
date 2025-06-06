import asyncio
from qipu_light_curtain import IntelligentGrating, Parity

async def main():
    # Create a new instance using the build method
    grating = await IntelligentGrating.build(
        port="/dev/ttyUSB1",  # Serial port
        #address=0x0F,         # Device address
        #address=0x40,         # Device address
        address=0x41,         # Device address
        #baudrate=19200,       # Baud rate
        baudrate=115200,       # Baud rate
        #parity='E',           # Parity (E for Even)
        parity='N',           # Parity (E for Even)
        timeout=1             # Timeout in seconds
    )

    try:
        #await grating.reset_defaults()
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
        #status = await grating.read_all_light_status()
        #print(f"Light beam status: {status}")
        # Change device settings
        #await grating.set_address(0x41)        # Change device address
        #await grating.set_baud_rate(115200)      # Change baud rate
        #await grating.set_parity(Parity.NONE)  # Change parity
        while True:
            #await grating.read_all_light_status()
            lowest = await grating.read_lowest_blocked()
            highest = await grating.read_highest_blocked()
            quantity = await grating.read_blocked_quantity()
            print(f"{lowest} {highest} {quantity}")
            #await asyncio.sleep(.1)

    finally:
        # Always close the connection when done
        grating.close()

# Run the async main function
asyncio.run(main())


"""
0x40 = Module On Scale 
0x41 = Module On Front Panel
"""

