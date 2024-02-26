# <img src="assets/blade-icon.gif" width="76" height="76"> BLADE: Bluetooth Link Access and Data Exchange


## Overview

BLADE represents an advanced system crafted to establish a seamless bridge between HTTP requests and Bluetooth communications, enabling streamlined interaction with Bluetooth devices via a local server. This server adeptly manages device connections, facilitating operations such as service discovery, data exchange, and file transfers with both classic Bluetooth and BLE devices through HTTP requests.

## Key Features

##### Streamlined Device Management

- Offers a unified interface for managing classic Bluetooth and BLE devices, eliminating the need for separate tools or protocols.

##### Effortless Service Discovery

- Provides accessible service discovery via simple HTTP requests, enabling users to explore device capabilities effortlessly.

##### Robust Data Exchange

- Utilizes reliable mechanisms for sending commands and receiving data, enabling real-time interactions and telemetry monitoring.

##### File Transfer Capabilities

- Supports effortless data exchange with compatible devices via FTP or OBEX, thereby enhancing device functionality and versatility.

##### Expanded Accessibility

- Enables integration with various applications and systems, fostering innovation across domains.

##### Examples of New Use Cases

1. **Remote Device Configuration**: Make it easy to mass deployments and centralized management.
2. **Real-time Monitoring and Control**: Enables tasks like environmental monitoring and IoT device control.
3. **Automated Data Acquisition**: Integrates seamlessly into data logging systems, analytics platforms, or industrial automation workflows.
4. **Cross-platform Integration**: Ensures compatibility and interoperability in cross-platform applications.

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

| Operating System | Compatibility |
| ---------------- | ------------- |
| Windows          | ✅            |
| Linux            | ❌            |
| macOS            | ❌            |

### Python Version Compatibility

| Version | Compatibility |
| ------- | ------------- |
| 3       |   =>3.11.8    |

## Example Usage

Upon executing the BLADE server script, the terminal output might look like this:

```console
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
```

A sample GET request to `http://localhost:8080/04-D9-F5-BE-E8-A9/services` would yield:

```console
$ curl http://localhost:8080/04-D9-F5-BE-E8-A9/services
```

```json
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
```

## API Reference

### Available Endpoints

The availability of endpoints depends on the capabilities of each connected device. For instance, file transfers are feasible with devices that support serial communication (such as RFCOMM) and have FTP or OBEX protocol support.

| Endpoint             | Description                                                   |
| -------------------- | ------------------------------------------------------------- |
| `/services`          | Retrieves service information for a specified device.         |
| `/connect`           | Initiates a connection to a specified device.                 |
| `/disconnect`        | Terminates the connection with a device.                      |
| `/transfer`          | Initiates a file transfer to a device (requires FTP or OBEX support).|
| `/notifications`     | Subscribes to notifications from a BLE device.                |
| `/write`             | Writes data to a characteristic of a BLE device.              |
| `/read`              | Reads data from a characteristic of a BLE device.             |

- `/services`: Lists all available services provided by a device. The services available are specific to the device's capabilities.
- `/connect`: Establishes a connection to a specified Bluetooth device. This is the first step before interacting with the device.
- `/disconnect`: Safely disconnects from a connected Bluetooth device. This is recommended after completing all interactions.
- `/transfer`: Available for devices that support file transfer capabilities. This endpoint is specifically for transferring files using the FTP or OBEX protocol, which is generally supported by devices capable of serial communication.
- `/notifications`: This endpoint is specific to BLE devices that support notifications. It allows a client to subscribe to updates for specific characteristics provided by the device.
- `/write`: Sends data to a specific characteristic of a BLE device. This is often used to change settings or control device behavior.
- `/read`: Retrieves the current value of a specific characteristic from a BLE device. Useful for getting the state or reading sensor data.

### Example Usage:

Connecting to and communicating with Bluetooth devices is essential for various functionalities. Let's elaborate on how to achieve this using the provided endpoints and request formats.

#### Connecting to a Bluetooth Device

To connect to a Bluetooth device, we use the `/connect` endpoint. Here's how you would initiate a connection:

- **Request Format**:
  - Endpoint: `http://localhost:8080/<device_mac>/connect`
  - Method: POST
  - Example:
    ```bash
    $ curl -X POST http://localhost:8080/<device_mac>/connect
    ```

#### Communicating with Bluetooth Devices

After establishing a connection, we can perform various actions such as service discovery, data exchange, or controlling device behavior.

##### Service Discovery

To retrieve information about the services provided by a Bluetooth device, we use the `/services` endpoint.

- **Request Format**:
  - Endpoint: `http://localhost:8080/<device_mac>/services`
  - Method: GET
  - Example:
    ```bash
    $ curl http://localhost:8080/<device_mac>/services
    ```

##### Writing to a Characteristic

To send data to a specific characteristic of a Bluetooth Low Energy (BLE) device, we use the `/write` endpoint.

- **Request Format**:
  - Endpoint: `http://localhost:8080/<device_mac>/write`
  - Method: POST
  - Body: JSON object containing the service UUID, characteristic UUID, and the data to write.
  - Example:
    ```bash
    $ curl -X POST http://localhost:8080/<device_mac>/write -d '{"service_uuid": "<service_uuid>", "characteristic_uuid": "<characteristic_uuid>", "data": "New Value"}'
    ```

##### Reading from a Characteristic

To retrieve the current value of a specific characteristic from a BLE device, we use the `/read` endpoint.

- **Request Format**:
  - Endpoint: `http://localhost:8080/<device_mac>/read/<service_uuid>/<characteristic_uuid>`
  - Method: GET
  - Example:
    ```bash
    $ curl http://localhost:8080/<device_mac>/read/<service_uuid>/<characteristic_uuid>
    ```

##### Subscribing to Notifications

For BLE devices that support notifications, we can subscribe to updates for specific characteristics using the `/notifications` endpoint.

- **Request Format**:
  - Endpoint: `http://localhost:8080/<device_mac>/notifications`
  - Method: POST
  - Body: JSON object containing the service UUID, characteristic UUID, and a flag indicating subscription status (true for subscribe, false for unsubscribe).
  - Example:
    ```bash
    $ curl -X POST http://localhost:8080/<device_mac>/notifications -d '{"service_uuid": "<service_uuid>", "characteristic_uuid": "<characteristic_uuid>", "subscribe": true}'
    ```

#### Disconnecting from a Bluetooth Device

Once interactions with a Bluetooth device are complete, it's essential to disconnect from it to release resources.

- **Request Format**:
  - Endpoint: `http://localhost:8080/<device_mac>/disconnect`
  - Method: POST
  - Example:
    ```bash
    $ curl -X POST http://localhost:8080/<device_mac>/disconnect
    ```

### Response Formatting

Responses are JSON formatted, providing clear and structured data about the request outcomes, including service discovery results, confirmation of actions taken, and data received from devices.

## Contribution Guidelines

Contributions to BLADE are welcome! Whether it's adding support for additional operating systems, enhancing existing features, or fixing bugs, please feel free to fork the repository, make your changes, and submit a pull request.

## License

BLADE is released under a specified open-source license. Please refer to the LICENSE file in the repository for detailed terms and conditions.
