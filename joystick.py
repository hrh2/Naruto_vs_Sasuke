import serial
import time


class ArduinoJoystick:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        try:
            self.arduino = serial.Serial(port, baudrate)
            time.sleep(2)  # Allow time for the connection to establish
            self.connected = True
        except serial.SerialException:
            print(f"Could not connect to Arduino on port {port}. Please check your connection.")
            self.connected = False

    def read_arduino_data(self):
        if not self.connected:
            return None, "Not connected to Arduino"

        try:
            serial_data = self.arduino.readline().decode().strip().split(",")
            joystick_x = int(serial_data[0])
            joystick_y = int(serial_data[1])
        except (ValueError, IndexError):
            joystick_x, joystick_y = 0, 0

        if 0 <= joystick_x <= 250 and 251 <= joystick_y <= 512:
            return 1, (joystick_x, joystick_y)
        elif 560 <= joystick_x and 402 <= joystick_y <= 512:
            return 2, (joystick_x, joystick_y)
        elif 251 <= joystick_x <= 512 and 560 <= joystick_y:
            return 3, (joystick_x, joystick_y)
        elif 251 <= joystick_x <= 512 and 0 <= joystick_y <= 250:
            return 4, (joystick_x, joystick_y)

        print(joystick_x, joystick_y)
        return 0, (joystick_x, joystick_y)  # Return 0 if none of the conditions are met


if __name__ == '__main__':
    joystick = ArduinoJoystick()
    result, position = joystick.read_arduino_data()
    print(f"Result: {result}, Position: {position}")
