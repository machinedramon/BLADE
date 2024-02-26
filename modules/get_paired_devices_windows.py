import re
import asyncio
from subprocess import Popen, PIPE
import json


async def get_paired_devices_windows():
    print("🔍 Searching for paired devices on Windows...")

    # Define the PowerShell command to get information about Bluetooth device drivers, formatting the output
    cmd = "Get-WmiObject -Class Win32_PnPSignedDriver | Where-Object {$_.DeviceName -like '*Bluetooth*'} | Select-Object DeviceID, FriendlyName, DeviceName | Format-List"

    # Execute the PowerShell command, capturing both standard output and standard error
    process = Popen(["powershell", "-Command", cmd], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    # Decode the PowerShell command output from bytes to string
    output = stdout.decode("utf-8", errors="ignore")

    # List to store unique devices
    devices = []

    # Process each line of the output
    lines = output.split("\n")
    for i in range(len(lines)):
        # Try to find DeviceID, FriendlyName, and DeviceName using adapted regular expressions
        if "DeviceID" in lines[i]:
            device_id_line = lines[i]
            friendly_name_line = lines[i + 1] if i + 1 < len(lines) else ""
            device_name_line = lines[i + 2] if i + 2 < len(lines) else ""

            device_id_match = re.search(r"DeviceID\s*:\s*(.*)", device_id_line)
            friendly_name_match = re.search(
                r"FriendlyName\s*:\s*(.*)", friendly_name_line
            )
            device_name_match = re.search(r"DeviceName\s*:\s*(.*)", device_name_line)

            if device_id_match and friendly_name_match and device_name_match:
                device_id = device_id_match.group(1).strip()
                friendly_name = friendly_name_match.group(1).strip()
                device_name = device_name_match.group(1).strip()

                # Determine the device type based on DeviceName
                if "Bluetooth Device" in device_name:
                    device_type = "Classic"
                else:
                    device_type = "BLE"

                # Check if the device is Bluetooth or Bluetooth LE and extract the MAC address
                mac_match = re.search(r"_([0-9A-F]{12})", device_id, re.IGNORECASE)
                if mac_match:
                    mac = ":".join(
                        a + b
                        for a, b in zip(
                            mac_match.group(1)[::2], mac_match.group(1)[1::2]
                        )
                    )

                    # Construct the device object and add it to the list of devices
                    device = {"name": friendly_name, "type": device_type, "mac": mac}
                    devices.append(device)

    # Remove duplicates, prioritizing devices with type "Bluetooth Device"
    unique_devices = {}
    mac_count = {}
    for device in devices:
        if device["mac"] not in mac_count:
            mac_count[device["mac"]] = 1
        else:
            mac_count[device["mac"]] += 1

    for device in devices:
        key = (device["mac"], device["name"])
        if mac_count[device["mac"]] > 1 and device["name"] == "":
            continue
        unique_devices[key] = device

    # Format the output as a list of dictionaries in the desired format
    formatted_output = [
        f"{{\"name\": \"{device['name']}\", \"type\": \"{device['type']}\", \"mac\": \"{device['mac']}\"}}"
        for device in unique_devices.values()
    ]

    # Print the formatted output to console
    print("✅ Paired devices found.")
    json_output = json.loads("[" + ", ".join(formatted_output) + "]")
    return json_output


if __name__ == "__main__":
    asyncio.run(get_paired_devices_windows())
