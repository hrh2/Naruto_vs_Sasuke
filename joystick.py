import serial
import time


class ArduinoJoystick:
    def __init__(self, port='COM8', baudrate=9600):
        try:
            self.arduino = serial.Serial(port, baudrate)
            time.sleep(2)  # Allow time for the connection to establish
            self.connected = True
        except serial.SerialException:
            print(f"Could not connect to Arduino on port {port}. Please check your connection.")
            self.connected = False

    def read_arduino_data(self):
        global joystick_x, joystick_y
        if not self.connected:
            return None, "Not connected to Arduino"

        try:
            # Attempt to read a line of serial data
            serial_data = self.arduino.readline().decode().strip().split(",")

            # Check if we received both X and Y data
            if len(serial_data) >= 2:
                joystick_x = int(serial_data[0])
                joystick_y = int(serial_data[1])

                if 0 <= joystick_x <= 250 and 251 <= joystick_y <= 512:
                    return 1#, (joystick_x, joystick_y)
                elif 560 <= joystick_x and 402 <= joystick_y <= 512:
                    return 2#, (joystick_x, joystick_y)
                elif 251 <= joystick_x <= 512 and 560 <= joystick_y:
                    return 3#, (joystick_x, joystick_y)
                elif 251 <= joystick_x <= 512 and 0 <= joystick_y <= 250:
                    return 4#, (joystick_x, joystick_y)
                else:
                    return 0#, (joystick_x, joystick_y)  # Default return
            else:
                # print("Incomplete data received:", serial_data)
                return 0#, None  # Incomplete data received

        except ValueError:
            print("Error: Received non-numeric data")
            return 0#, None  # Handle non-numeric data gracefully

        except Exception as e:
            print(f"Error reading data: {e}")
            return 0#, None