# BLADE: Bluetooth Link Access and Data Exchange

## Overview

BLADE is an advanced framework designed to establish a bridge between HTTP requests and Bluetooth communications, allowing for seamless interaction with Bluetooth devices via a local server. This server manages device connections, facilitating operations such as service discovery, data exchange, and file transfers with both classic Bluetooth and BLE devices through HTTP requests.

## Key Features

- Unified Device Management for both classic Bluetooth and BLE devices.
- Comprehensive Service Discovery for connected devices.
- Robust Data Exchange mechanisms for sending commands and receiving data.
- File Transfer capabilities via OBEX for supported devices.
- Simplified interactions through an HTTP-based interface.

## Technical Specifications

### System Interaction Flow

1. **HTTP Request Reception**: The server receives an HTTP request targeting a specific Bluetooth device's MAC address or a service endpoint.
2. **Request Parsing**: It parses the request to extract relevant parameters, such as the device identifier (MAC address) and requested action (e.g., service discovery, data exchange).
3. **Bluetooth Communication**: Based on the parsed request, the server initiates a Bluetooth connection to the targeted device, performing operations like service discovery or data transmission.
4. **Response Generation**: After completing the Bluetooth operation, the server constructs an HTTP response encapsulating the outcome, which may include a list of services, data received from the device, or confirmation of a successful operation.
5. **HTTP Response Delivery**: The generated response is sent back to the requester, providing detailed outcomes or data obtained from the Bluetooth device.

### External Libraries

- Flask: For the HTTP server framework.
- bleak: For BLE device communications.
- PyBluez: For classic Bluetooth device interactions.

### System Compatibility

\| Operating System \| Compatibility \|
\|------------------\|---------------\|
\| Windows          \| ✅             \|
\| Linux            \| ❌             \|
\| macOS            \| ❌             \|

### Python Version Compatibility

\| Version \| Compatibility \|
\|---------\|---------------\|
\| 3.11.8  \| ✅             \|

## Example Usage

Upon executing the BLADE server script, the terminal output might look like this:

\```console
📡 HTTP Bluetooth Server starting...
🔍 Searching for paired devices on Windows...
✅ Paired devices found.
✅ Device discovery complete.
📱 Device: Mormaii Life, Type: BLE
📱 Device: ROG Phone 5s, Type: Classic
🔗 Exposed device: Mormaii Life - http://localhost:8080/CC-52-83-36-B5-1B/services
🔗 Exposed device: ROG Phone 5s - http://localhost:8080/04-D9-F5-BE-E8-A9/services
📡 HTTP Bluetooth Server started.

Serving Flask app 'index'
Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
Running on http://127.0.0.1:8080
Press CTRL+C to quit
\```

A sample GET request to `http://localhost:8080/04-D9-F5-BE-E8-A9/services` would yield:

\```console
$ curl http://localhost:8080/04-D9-F5-BE-E8-A9/services
\```

\```json
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
    ...
  ],
  "total_services_found": 14
}
\```

## API Reference

### Available Endpoints

| Endpoint    | Description                                             |
| ----------- | ------------------------------------------------------- |
| /services   | Retrieves service information for a specified device.   |
| /connect    | (Example) Initiates a connection to a specified device. |
| /disconnect | (Example) Terminates the connection with a device.      |
| /transfer   | (Example) Initiates a file transfer to a device.        |

### Example Request Formats

- **Service Discovery Request**:
    \```console
    $ curl http://localhost:8080/<device_mac>/services
    \```
- **Connect to Device**:
    \```console
    $ curl -X POST http://localhost:8080/connect -d '{"device_mac": "<device_mac>"}'
    \```
- **Send Data to a Service**:
    \```console
    $ curl -X POST http://localhost:8080/<device_mac>/<service_uuid>/send -d '{"data": "Hello World"}'
    \```

### Response Formatting

Responses are JSON formatted, providing clear and structured data about the request outcomes, including service discovery results, confirmation of actions taken, and data received from devices.

## Contribution Guidelines

Contributions to BLADE are welcome! Whether it's adding support for additional operating systems, enhancing existing features, or fixing bugs, please feel free to fork the repository, make your changes, and submit a pull request.

## License

BLADE is released under a specified open-source license. Please refer to the LICENSE file in the repository for detailed terms and conditions.
