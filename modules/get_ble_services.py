from bleak import BleakClient
from .uuid_to_name import uuid_to_name


async def get_ble_services(device_address):
    # Connect to the BLE device
    async with BleakClient(device_address) as client:
        # Check if connection is successful
        is_connected = await client.connect()

        # If connected, retrieve services information
        if is_connected:
            services_info = []
            services = await client.get_services()

            # Iterate through services and gather information
            for service in services:
                service_name = uuid_to_name(service.uuid)
                characteristics_info = []

                # Iterate through characteristics of the service
                for char in service.characteristics:
                    char_name = uuid_to_name(char.uuid)

                    # Gather characteristic information
                    characteristics_info.append(
                        {
                            "uuid": char.uuid,
                            "name": char_name,
                            "properties": char.properties,
                        }
                    )

                # Gather service information
                services_info.append(
                    {
                        "uuid": service.uuid,
                        "name": service_name,
                        "characteristics": characteristics_info,
                    }
                )

            # Return the gathered services information
            return services_info

        # If connection fails, print an error message and return None
        else:
            print(f"❌ Failed to connect to the device {device_address}.")
            return None
