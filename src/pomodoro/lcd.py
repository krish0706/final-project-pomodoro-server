# #!/usr/bin/python3

# from rpi_lcd import LCD
# import time

# class Display:
#     def __init__(self):
#         self.lcd = LCD()

#     def home(self):
#         self.lcd.clear()
#         self.lcd.text("Pomodoro Timer", 1)

#     def show_message(self, line1="", line2=""):
#         self.lcd.clear()
#         if line1:
#             self.lcd.text(line1, 1)
#         if line2:
#             self.lcd.text(line2, 2)

#     def clear(self):
#         self.lcd.clear()

#     def cleanup(self):
#         self.lcd.clear()


















import fcntl
import time
import os


I2C_SLAVE = 0x0703

class I2CDevice:
    def __init__(self, address, bus=1):
        self.address = address
        self.bus = bus
        self.file = os.open(f"/dev/i2c-{bus}", os.O_RDWR)
        fcntl.ioctl(self.file, I2C_SLAVE, address)

    def write_byte(self, byte):
        os.write(self.file, bytes([byte]))

    def close(self):
        os.close(self.file)
        
        
class LCD:
    # Commands
    LCD_CLEAR = 0x01
    LCD_RETURN_HOME = 0x02
    LCD_ENTRY_MODE = 0x06
    LCD_DISPLAY_ON = 0x0C
    LCD_FUNCTION_SET = 0x28  # 4-bit, 2-line, 5x8 font

    # Control bits
    ENABLE = 0b00000100
    RW = 0b00000010
    RS = 0b00000001

    def __init__(self, address=0x27, bus=1):
        self.device = I2CDevice(address, bus)
        self.backlight = 0x08  # Assume backlight on
        self._init_lcd()

    def _pulse_enable(self, data):
        self.device.write_byte(data | self.ENABLE | self.backlight)
        time.sleep(0.0005)
        self.device.write_byte((data & ~self.ENABLE) | self.backlight)
        time.sleep(0.0001)

    def _send_nibble(self, nibble, mode=0):
        data = (nibble & 0xF0) | mode
        self.device.write_byte(data | self.backlight)
        self._pulse_enable(data)

    def _send_byte(self, byte, mode=0):
        self._send_nibble(byte & 0xF0, mode)
        self._send_nibble((byte << 4) & 0xF0, mode)

    def _init_lcd(self):
        time.sleep(0.02)  # Wait for LCD to power up
        self._send_nibble(0x30)
        time.sleep(0.005)
        self._send_nibble(0x30)
        time.sleep(0.001)
        self._send_nibble(0x30)
        time.sleep(0.001)
        self._send_nibble(0x20)  # 4-bit mode
        time.sleep(0.001)

        self._send_byte(self.LCD_FUNCTION_SET)
        self._send_byte(self.LCD_DISPLAY_ON)
        self._send_byte(self.LCD_CLEAR)
        self._send_byte(self.LCD_ENTRY_MODE)
        time.sleep(0.002)

    def clear(self):
        self._send_byte(self.LCD_CLEAR)
        time.sleep(0.002)

    def write(self, text):
        for char in text:
            self._send_byte(ord(char), self.RS)

    def set_cursor(self, row, col):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        addr = 0x80 | (col + row_offsets[row])
        self._send_byte(addr)

    def close(self):
        self.device.close()

lcd = LCD()

lcd.clear()
lcd.set_cursor(0, 0)
lcd.write("Hello, World!")

lcd.set_cursor(1, 0)
lcd.write("Bhakti Ramani!")

# When done
lcd.close()





