import platform
from .get_paired_devices_windows import get_paired_devices_windows


async def check_os():
    discovered_devices = {}  # Dictionary to store discovered devices

    # Determine the operating system
    os_type = platform.system().lower()

    # If the OS is Windows, attempt to get paired devices
    if os_type == "windows":
        paired_devices = await get_paired_devices_windows()

        # Process paired devices
        for device in paired_devices:
            mac = device["mac"]
            name = device["name"]
            device_type = device["type"]

            # Store device information in the dictionary
            discovered_devices[mac] = {
                "friendlyName": name.strip(),
                "type": device_type,
            }

    # If the OS is Linux, print a message indicating device discovery is not implemented
    elif os_type == "linux":
        print("Device discovery on Linux is not yet implemented.")

    # If the OS is macOS, print a message indicating device discovery is not implemented
    elif os_type == "darwin":
        print("Device discovery on macOS is not yet implemented.")

    # For unsupported operating systems, print a message
    else:
        print(f"Operating system {os_type} is not supported for device discovery.")

    # Print a message indicating device discovery is complete
    print("✅ Device discovery complete.")

    # Return the dictionary of discovered devices
    return discovered_devices
