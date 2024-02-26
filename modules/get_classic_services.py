import bluetooth
from .uuid_to_service_name import uuid_to_service_name  # Adjust as necessary


async def get_classic_services(device_mac):
    # Find classic Bluetooth services associated with the device MAC address
    services = bluetooth.find_service(address=device_mac)
    services_info = []

    # Iterate through each found service
    for svc in services:
        # Process each service class UUID
        service_classes_converted = [
            uuid_to_service_name(uuid) for uuid in svc.get("service-classes", [])
        ]

        # Process each profile, assuming it might be a tuple
        profiles_converted = [
            {
                "profile_id": (
                    uuid_to_service_name(profile[0])
                    if isinstance(profile, tuple)
                    else uuid_to_service_name(profile)
                ),
                "profile_size": (
                    len(profile[0])
                    if isinstance(profile, tuple) and isinstance(profile[0], bytes)
                    else 0
                ),
            }
            for profile in svc.get("profiles", [])
        ]

        # Construct service information dictionary
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

    return services_info
