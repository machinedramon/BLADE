"""
BLADE: Bluetooth Link Access and Data Exchange

This script implements an HTTP server using Flask to expose Bluetooth services of devices.
It provides endpoints to retrieve information about Bluetooth services for both Classic and BLE devices.

Author: Diego Augusto Ferreira
Contact:
    GitHub: @machinedramon
    Email: machinedramonengineer@gmail.com

Modules:
    - uuid_to_name: Module to convert UUIDs to human-readable service names.
    - check_os: Module to check the operating system and discover paired Bluetooth devices.

"""

import asyncio
from datetime import datetime
from flask import Flask, Response, jsonify
import bluetooth
from bleak import BleakClient
from modules.uuid_to_name import uuid_to_name
from modules.check_os import check_os

# Flask Configuration
app = Flask(__name__)
filtered_devices = {}


@app.route("/<device_mac>/services")
async def device_services(device_mac):
    """
    Retrieves the services for a specified device.

    Args:
        device_mac (str): MAC address of the device.

    Returns:
        JSON: Information about the services available on the device.
    """
    print(f"🔍 Searching for services for the device: {device_mac}")
    device_mac = device_mac.upper().replace("-", ":")
    if device_mac in filtered_devices:
        device_type = filtered_devices[device_mac]["type"]
        if device_type == "Classic":
            services = bluetooth.find_service(address=device_mac)
            services_info = []
            for svc in services:
                service_classes_converted = [
                    uuid_to_name(uuid) for uuid in svc.get("service-classes", [])
                ]
                profiles_converted = [
                    {
                        "profile_id": (
                            uuid_to_name(profile[0])
                            if isinstance(profile, tuple)
                            else uuid_to_name(profile)
                        ),
                        "profile_size": (
                            len(profile[0])
                            if isinstance(profile, tuple)
                            and isinstance(profile[0], bytes)
                            else 0
                        ),
                    }
                    for profile in svc.get("profiles", [])
                ]

                service_info = {
                    "name": (
                        svc.get("name").decode("utf-8")
                        if isinstance(svc.get("name"), bytes)
                        else svc.get("name")
                    ),
                    "description": (
                        svc.get("description", "").decode("utf-8")
                        if isinstance(svc.get("description", ""), bytes)
                        else svc.get("description", "")
                    ),
                    "provider": (
                        svc.get("provider").decode("utf-8")
                        if isinstance(svc.get("provider"), bytes)
                        else svc.get("provider")
                    ),
                    "protocol": (
                        svc.get("protocol").decode("utf-8")
                        if isinstance(svc.get("protocol"), bytes)
                        else svc.get("protocol")
                    ),
                    "port": svc.get("port"),
                    "service_classes": service_classes_converted,
                    "profiles": profiles_converted,
                    "profile_count": len(profiles_converted),
                }
                services_info.append(service_info)

            response_data = {
                "request_type": "GET",
                "request_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "total_services_found": len(services),
                "services": services_info,
            }
            return jsonify(response_data)
        elif device_type == "BLE":
            services_info = await fetch_ble_services(device_mac)
            if services_info is not None:
                response_data = {
                    "request_type": "GET",
                    "request_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "services": services_info,
                }
                return jsonify(response_data)
            else:
                return Response(
                    "Failed to retrieve services from the BLE device.", status=500
                )
    else:
        return Response("Device not found.", status=404)


async def fetch_ble_services(device_address):
    """
    Fetches BLE services for the specified device.

    Args:
        device_address (str): MAC address of the BLE device.

    Returns:
        list: List of dictionaries containing information about the services.
    """
    try:
        async with BleakClient(device_address) as client:
            await client.connect()
            services = await client.get_services()
            services_info = [
                {"uuid": service.uuid, "name": uuid_to_name(service.uuid)}
                for service in services
            ]
            return services_info
    except Exception as e:
        print(f"Error searching for BLE services: {e}")
        return None


async def main_async():
    """
    Main asynchronous function to start the HTTP Bluetooth server.
    """
    print("📡 HTTP Bluetooth Server starting...")
    port = 8080
    # Directly updates the filtered_devices dictionary with the discovered devices
    discovered_devices = await check_os()
    filtered_devices.update(discovered_devices)
    for mac, info in filtered_devices.items():
        print(f"📱 Device: {info['friendlyName']}, Type: {info['type']}")

    for mac, info in filtered_devices.items():
        route = f"http://localhost:{port}/{mac.replace(':', '-')}/services"
        print(f"🔗 Exposed device: {info['friendlyName']} - {route}")

    # Starting the Flask server asynchronously
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, app.run, "127.0.0.1", port, False)
    print("📡 HTTP Bluetooth Server started.")


if __name__ == "__main__":
    asyncio.run(main_async())


# Example json response from /services for better visualization
"""
Example Response:
{
    "request_time": "2024-02-26T01:56:24Z",
    "request_type": "GET",
    "services": [
        {
            "description": "",
            "name": null,
            "port": 31,
            "profile_count": 0,
            "profiles": [],
            "protocol": "L2CAP",
            "provider": null,
            "service_classes": ["Unknown Service (b'1801')"]
        },
        {
            "description": "OBEX Object Push",
            "name": "OBEX Object Push",
            "port": 12,
            "profile_count": 1,
            "profiles": [{"profile_id": "OBEX Object Push", "profile_size": 4}],
            "protocol": "RFCOMM",
            "provider": null,
            "service_classes": ["Unknown Service (b'1105')"]
        },
        ...
    ],
    "total_services_found": 14
}
"""
