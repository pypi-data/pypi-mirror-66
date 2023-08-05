# FPGA I2C Bridge API
A library for managing and remotely controlling devices connected to one or several bridges, which in turn are communicated with via a specialized I²C protocol. Intended for a Smart Home FPGA solution that was created as part of a Bachelor's thesis.

Includes a high-level API as well as a low-level debugging shell.

## Installation
```
pip install fpga-i2c-bridge
```

## Usage
### Interactive shell
On a device with I2C support, run:
```
python -m fpga_i2c_bridge
```

Use the `--addr` and `--bus` switches to adjust I2C bus and address values, respectively.

To run with simulated dummy devices only, run instead:
```
python -m fpga_i2c_bridge --dummy
```
Use `--dummy-appliances` and `--dummy-sensors` to supply a comma-seperated list of device types to simulate. For example:
```
python -m fpga_i2c_bridge --dummy --dummy-appliances 1,2,3,4 --dummy-sensors 1,3,5
``` 

### API Examples
#### Reading and manipulating device states
```python
from fpga_i2c_bridge import I2CBridge, I2CGenericBinary, I2CDimmer, I2CRGBDimmer, I2CShutter

# Appliance IDs
LAMP_ID = 1
DIMMER_ID = 2
RGB_ID = 3
SHUTTER_ID = 4

if __name__ == '__main__':
    # Create and initialize I2C Bridge
    i2c = I2CBridge(i2c_bus=1, i2c_addr=0x3E)
    
    # Store device objects
    lamp: I2CGenericBinary = i2c.appliances[LAMP_ID]
    dimmer: I2CDimmer = i2c.appliances[DIMMER_ID]
    rgb: I2CRGBDimmer = i2c.appliances[RGB_ID]
    shutter: I2CShutter = i2c.appliances[SHUTTER_ID]
    
    # -- Read device states --
    print(f"Lamp is currently {'on' if lamp.state is True else 'off'}")
    print(f"Dimmer brightness: {dimmer.state}")
    print(f"RGB lamp color: {rgb.state}")
    print(f"Shutter state: {shutter.state}")
    
    # -- Manipulate devices --
    # Turn on lamp
    lamp.turn_on()
    
    # Set dimmer to 50% brightness
    dimmer.set_brightness(0.5)
    
    # Set RGB lamp to orange-ish
    rgb.set_color((1.0, 0.7, 0.0))
    
    # Move shutter up fully
    shutter.move_up_full()
```

#### Using callback handlers
```python
from fpga_i2c_bridge import I2CBridge, I2CShutter, I2CShutterControlSensor

# Assuming a shutter is found under appliance ID 4
SHUTTER_ID = 4

# Assuming a shutter is found under sensor ID 0
SHUTTER_SENSOR_ID = 0

if __name__ == '__main__':
    # Create and initialize I2C Bridge
    i2c = I2CBridge(i2c_bus=1, i2c_addr=0x3E)

    # Store device objects
    shutter_appliance: I2CShutter = i2c.appliances[SHUTTER_ID]
    shutter_sensor: I2CShutterControlSensor = i2c.sensors[SHUTTER_SENSOR_ID]

    # Register handlers for the shutter sensor
    @shutter_sensor.register_full_down_handler()
    def on_full_down():
        print("Request to move down")
        shutter_appliance.move_down_full()

    @shutter_sensor.register_full_up_handler()
    def on_full_up():
        print("Request to move up")
        shutter_appliance.move_up()

    # Register handler for the shutter appliance
    @shutter_appliance.register_update_handler()
    def on_appliance_update():
        print(f"The shutter {shutter_appliance} updated its state to {shutter_appliance.state}")

    # Enable polling
    i2c.start_polling()

    # Loop and wait for input
    print("Press CTRL-C to quit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
```

## Protocol specification
This section describes the protocol used for communications between the device using this library (hereafter referred to as the "gateway") and a connected I2C device (the "bridge").

The bridge operates as an I2C slave on any address (by default, the library assumes this address to be `0x3E`, but this can be changed via the `--addr` command line switch, as outlined above.)

### Commands

Command messages sent to the I2C bridge consist of a command-dependent **opcode** byte as well as several **parameter** bytes. The amount of parameter data depends on the command used, and can range between 0 and 4 bytes in length.

Finally, 2 bytes of **CRC** data are appended at the end of the message, calculated from the opcode and parameter bytes using the polynomial x^16 + x^13 + x^11 + x^10 + x^9 + x^8 + x^4 + x^2 + 1 (encoded as `0x2F15` when omitting the MSB).

The following table gives a brief overview over the different commands, their opcodes and parameters:

| Command             | Opcode | Parameters              | Description                             |
| ------------------- |:------:| ----------------------- | --------------------------------------- |
| Get appliance state | `0x00` | Appliance ID            | Query an appliance's current state      |
| Get appliance type  | `0x01` | Appliance ID            | Query an appliances' type               |
| Get sensor type     | `0x02` | Sensor ID               | Query a sensor's type                   |
| Set appliance state | `0x10` | Appliance ID, new state | Set state of an appliance               |
| Get bridge status   | `0x20` | -                       | Queries bridge version and device count |
| Reset bridge        | `0x2F` | -                       | Reset bridge hardware                   |
| Poll events         | `0x30` | -                       | Poll for new input and update events    |
| Repeat last message | `0x40` | -                       | Request last message to be sent again   |

The bridge prepares responses to each command, which do not necessarily have to be read by the gateway. Responses are always 8 bytes long and contain the following:

| Byte | Meaning                                                    |
| ----:| ---------------------------------------------------------- |
|   1  | Status code: OK (`0xF0`), Error (`0xF1`), No data (`0xF2`) |
| 2..6 | Response data (padded with `0x00` to 5 bytes)              |
| 7..8 | CRC data                                                   |

Should a command result in an error, the response data includes the error codes and some relevant parameters. (See appendix.)

#### Get appliance state (`0x00`)

Requests the current state of an appliance.

- **Parameters:** Appliance ID (1 byte)
- **Expected response:** Appliance ID repeated (1 byte), Appliance state (3 bytes)
- **Error cases:**
    - If an unknown appliance ID is supplied, responds with error code `0x20` (Unknown device) followed by the erroneous appliance ID

##### Example

| Command                       | Response                                 |
| ----------------------------- | ---------------------------------------- |
| `00 01 2F 15`                 | `F0 01 00 00 01 00 4F 38`                |
| Get state of appliance `0x01` | OK, Appliance `0x01` state is `0x000001` |

##### Example for error on unknown appliance

| Command                       | Response                                 |
| ----------------------------- | ---------------------------------------- |
| `00 04 BC 54`                 | `F1 20 04 00 00 00 2C 57`                |
| Get state of appliance `0x04` | Error: Unknown appliance `0x04`          |


#### Get appliance type (`0x01`)

Requests the type of an appliance.

- **Parameters:** Appliance ID (1 byte)
- **Expected response:** Appliance ID repeated (1 byte), Appliance type identifier (1 bytes, see appendix) or `0x00` if the given appliance ID is not present
- **Error cases:**
    - If an unknown appliance ID is supplied, responds with error code `0x20` (Unknown device) followed by the erroneous appliance ID

##### Example

| Command                       | Response                                  |
| ----------------------------- | ----------------------------------------- |
| `01 01 D1 22`                 | `F0 01 02 00 00 00 75 8B`                 |
| Get type of appliance `0x01`  | OK, Appliance `0x01` is a Dimmer (`0x02`) |

##### Example for error on unknown appliance

| Command                      | Response                                 |
| ---------------------------- | ---------------------------------------- |
| `01 FF B1 29`                | `F1 20 FF 00 00 00 D4 71`                |
| Get type of appliance `0xFF` | Error: Unknown appliance `0xFF`          |


#### Get sensor type (`0x02`)

Requests the type of a sensor.

- **Parameters:** Sensor ID (1 byte)
- **Expected response:** Sensor ID repeated (1 byte), Sensor type identifier (1 bytes, see appendix)
- **Error cases:**
    - If an unknown sensor ID is supplied, responds with error code `0x20` (Unknown device) followed by the erroneous sensor ID

##### Example

| Command                   | Response                               |
| --------------------------| -------------------------------------- |
| `02 00 D3 7B`             | `F0 00 01 00 00 00 F7 ED`              |
| Get type of sensor `0x00` | OK, Sensor `0x00` is a Button (`0x01`) |

##### Example for error on unknown sensor

| Command                   | Response                     |
| ------------------------- | ---------------------------- |
| `02 FF 9C 65`             | `F1 20 FF 00 00 00 D4 71`    |
| Get type of sensor `0xFF` | Error: Unknown sensor `0xFF` |


#### Set appliance state (`0x10`)

Requests to set the state of an appliance.

- **Parameters:** Appliance ID (1 byte), new state (3 bytes)
- **Expected response:** Empty response
- **Error cases:**
    - If an unknown appliance ID is supplied, responds with error code `0x20` (Unknown device) followed by the erroneous appliance ID

##### Example

| Command                                  | Response                  |
| ---------------------------------------- | ------------------------- |
| `10 02 FF 77 00 C7 6C`                   | `F0 00 00 00 00 00 7D 3E` |
| Set appliance `0x02` to state `0xFF7700` | OK                        |

##### Example for error on unknown appliance

| Command                                  | Response                        |
| ---------------------------------------- | ------------------------------- |
| `10 49 12 34 56 4A 63`                   | `F1 20 49 00 00 00 A2 25`       |
| Set appliance `0x49` to state `0x123456` | Error: Unknown appliance `0x49` |


#### Get bridge status (`0x20`)

Retrieves the bridge version as well as the highest valid appliance and sensor IDs each. Depending on the configuration, not all device IDs are necessarily assigned.

- **Parameters:** None
- **Expected response:** Bridge version (2 bytes), highest appliance ID (1 byte), highest sensor ID (1 byte)
- **Error cases:** None

##### Example

| Command    | Response                                                                           |
| ---------- | ---------------------------------------------------------------------------------- |
| `20 71 E1` | `F0 DE AD 04 05 00 53 73`                                                          |
| Get status | OK, version is 0xDEAD, highest appliance ID is `0x04`, highest sensor ID is `0x05` |


#### Reset bridge (`0x2F`)

Requests the bridge hardware to reinitialize. What this means is up to the bridge implementation, but usually should put the hardware into a sane state. Reinitialization should also not take more than a couple of cycles.

- **Parameters:** None
- **Expected response:** Empty
- **Error cases:** None

##### Example

| Command      | Response                  |
| ------------ | ------------------------- |
| `2F EB 37`   | `F0 00 00 00 00 00 7D 3E` |
| Reset bridge | OK                        |


#### Poll events (`0x30`)

Receives a single input or update event from the bridge, if there are any. An update event describes an intrinsic, spontaneous change of an appliance's state without user input, while input events are fired by a sensor that has been triggered.

If there are no pending events, the bridge is expected to send a "No data" (`0xF2`) status response. The API keeps repeatedly sending this command until it receives such a response, to clear any event buffers the bridge might have.

- **Parameters:** None
- **Expected response:** Event data (5 bytes, see appendix) or "No data"
- **Error cases:** None


##### Example: Receiving an input event

| Command        | Response                                                              |
| -------------- | --------------------------------------------------------------------- |
| `30 DE 9B`     | `F0 00 01 00 00 01 D8 F8`                                             |
| Poll for event | OK, Input event (`0x00`) for sensor ID `0x01`, data: `0x000001`       |

##### Example: Receiving an update event

| Command        | Response                                                                 |
| -------------- | ------------------------------------------------------------------------ |
| `30 DE 9B`     | `F0 01 03 00 00 00 FF 58`                                                |
| Poll for event | OK, Update event (`0x01`) for appliance ID `0x03`, new state: `0x000000` |

##### Example: No new events

| Command        | Response                  |
| -------------- | ------------------------- |
| `30 DE 9B`     | `F2 00 00 00 00 00 5F 49` |
| Poll for event | No data                   |


#### Repeat last message (`0x40`)

Requests the last response to be sent again. This is used by the API in case it encounters a CRC checksum mismatch in any response. The bridge should always keep track of the last response it sent (that was not a CRC error response) and repeat it.

Sending this command intentionally before any other command results in undefined behavior.

- **Parameters:** none
- **Expected response:** Depends on the previous command
- **Error cases:** Depends on the previous command

##### Example: Repeating a previous response in case of a CRC error

| Command                                  | Response                  |
| ---------------------------------------- | ------------------------- |
| `10 00 00 00 01 7E 4A`                   | `F0 00 00 00 00 10 7D 3E` |
| Set appliance `0x00` to state `0x000001` | OK (corrupted)            |
| `40 E3 C2`                               | `F0 00 00 00 00 00 7D 3E` |
| Repeat last message                      | OK (valid)                |


### Appendix

#### Error response codes

| Code   | Error                      | Parameters                                        |
|:------:| -------------------------- | ------------------------------------------------- |
| `0x10` | Unknown command opcode     | Unrecognized opcode, repeated                     |
| `0x20` | No such device             | Unrecognized appliance or sensor ID, repeated     |
| `0x30` | CRC failure, please repeat | Calculated (nonzero) checksum of received message |
| `0xFF` | Unknown failure            | -                                                 |


#### Event data

##### Input events

An input event gets fired by a sensor that has been triggered, e.g. when a button has been pressed, or similar. The event contains the ID of the sensor as well as the data it is reporting.

| Byte | Content                       |
| ----:| ----------------------------- |
| 1    | `0x00`                        |
| 2    | ID of sensor that fired event |
| 3..5 | Sensor payload                |

##### Update events

An update event gets fired when an appliance has changed its state by itself, thus notifying the API about its new state. The event contains the ID of the appliance as well as its new state.

| Byte | Content                            |
| ----:| ---------------------------------- |
| 1    | `0x01`                             |
| 2    | ID of appliance that changed state |
| 3..5 | New state of appliance             |


#### Appliance type identifiers

| Code   | Appliance type |
|:------:| -------------- |
| `0x01` | Switch         |
| `0x02` | Dimmer         |
| `0x03` | RGB Dimmer     |
| `0x04` | Shutter        |


#### Sensor type identifiers

| Code   | Sensor type     |
|:------:| --------------- |
| `0x01` | Button          |
| `0x02` | Toggle          |
| `0x03` | Dimmer cycle    |
| `0x04` | RGB cycle       |
| `0x05` | Shutter control |