



import os
import fcntl
import time

I2C_SLAVE = 0x0703
LCD_I2C_ADDR = 0x27  

# Commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_FUNCTIONSET = 0x20
LCD_SETDDRAMADDR = 0x80

# Flags
LCD_ENTRYLEFT = 0x02
LCD_DISPLAYON = 0x04
LCD_2LINE = 0x08
LCD_5x8DOTS = 0x00
LCD_4BITMODE = 0x00

 
class Display:
    def __init__(self):
        self.file = os.open("/dev/i2c-1", os.O_RDWR)
        fcntl.ioctl(self.file, I2C_SLAVE, LCD_I2C_ADDR)
        self.backlight = 0x08  # backlight ON
        self._init_lcd()

    def _write_byte(self, data):
        os.write(self.file, bytes([data | self.backlight]))

    def _pulse_enable(self, data):
        self._write_byte(data | 0x04)  # Enable high
        time.sleep(0.0005)
        self._write_byte(data & ~0x04)  # Enable low
        time.sleep(0.0001)

    def _write4bits(self, data):
        self._write_byte(data)
        self._pulse_enable(data)

    def _send(self, data, mode=0):
        high = data & 0xF0
        low = (data << 4) & 0xF0
        self._write4bits(high | mode)
        self._write4bits(low | mode)

    def _command(self, cmd):
        self._send(cmd, mode=0x00)
        time.sleep(0.001)

    def _write_char(self, char):
        self._send(ord(char), mode=0x01)

    def _init_lcd(self):
        time.sleep(0.05)  # wait for LCD to power up
        self._write4bits(0x30)
        time.sleep(0.005)
        self._write4bits(0x30)
        time.sleep(0.005)
        self._write4bits(0x30)
        time.sleep(0.005)
        self._write4bits(0x20)  # set to 4-bit mode
        time.sleep(0.005)

        self._command(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self._command(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self._command(LCD_CLEARDISPLAY)
        self._command(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        time.sleep(0.002)

    def clear(self):
        self._init_lcd()
        self._command(LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def home(self):
        self._command(LCD_RETURNHOME)
        time.sleep(0.002)

    def set_cursor(self, col, row):
        row_offsets = [0x00, 0x40, 0x10, 0x50]  # Very important for 16x4!
        if row > 3:
            row = 3
        addr = col + row_offsets[row]
        self._command(LCD_SETDDRAMADDR | addr)

    def write(self, text):
        for char in text:
            self._write_char(char)
            

    def show_message(self, text, line=0, col=0):
        self.set_cursor(col, line)
        self.write(text.ljust(16))  # pad to clear line fully]
        
    def title(self):
        self.show_message("Pomodoro Timer", 0,3)

    def close(self):
        os.close(self.file)


if __name__ == "__main__":
    lcd = Display()

    lcd.show_message("HEEYYYY ", 1)
    lcd.show_message("How you  doin ", 2)
    lcd.show_message("Hello    there ", 0)
    lcd.clear()

    while(True):
        pass


