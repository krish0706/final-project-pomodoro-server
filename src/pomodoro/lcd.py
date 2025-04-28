/******************************************************************************
 * Name        : Bhakti Ramani
 * Subject     : ECEN 5713 - Advanced Embedded Systems Development (AESD)
 * Institution : University of Colorado Boulder
 * File        : lcd_basic.py
 * Description : 
 *   This file contains updated drivers and integration for the Pomodoro 
 *   hardware project:
 *     - New LCD driver using fcntl library (replacing rpi.lcd for Buildroot compatibility)
 *     - Updated buzzer driver with tunes for different system states
 *     - Integration of LCD and Buzzer drivers into Buildroot and server logic
 *
 * Steps :
 *	This code uses 16x4 LCD with i2c driver module. Simply connect i2c pins to Rpi
 * 	and run this code with Display class
 * 	If this code doesn't work, try checking lcd display address and change LCD_I2C_ADDR
 *	using i2cdetect -y
 *
 * Notes : This code was written for working on Buildroot and Raspberry Pi 4B
 * 	   
 *
 *****************************************************************************/



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


/***********************************************************
 * Function Name : lcd_init
 * Description   : Initializes the LCD display using fcntl IOCTL calls.
 ***********************************************************/
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

    def show_message(self, text, line=0):
        self.set_cursor(0, line)
        self.write(text.ljust(16))  # pad to clear line fully

    def close(self):
        os.close(self.file)

