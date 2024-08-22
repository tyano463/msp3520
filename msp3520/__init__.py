#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import spidev
import time
from dlog import dlog
import definitions as D

class Singleton(object):
    @classmethod
    def get_instance(cls, input):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(input)
        else:
            cls._instance.input = input
        return cls._instance

class MSP3520(Singleton):

    def __init__(self):
        print(D.PIN_BACK_LIGHT)
        return
        BACK_LIGHT = 25
        DC_RS = 5 
        CS_PIN = 8 
        RESET_PIN = 6 
        RESET = 0 
        RESET_RELEASE = 1 
        MODE_CMD = 0 
        MODE_DATA = 1 
    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BACK_LIGHT,GPIO.OUT,initial=1)
        GPIO.setup(RESET_PIN,GPIO.OUT,initial=RESET_RELEASE)
        GPIO.setup(DC_RS,GPIO.OUT,initial=1)
        GPIO.setup(CS_PIN, GPIO.OUT, initial=GPIO.HIGH)

        self.reset()

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 10000000
        self.spi.mode = 0 
        self.spi.bits_per_word = 8 

        self.write_command(0xF7)
        self.write_data(0xA9)
        self.write_data(0x51)
        self.write_data(0x2C)
        self.write_data(0x82)
        self.write_command(0xC0)
        self.write_data(0x11)
        self.write_data(0x09)
        self.write_command(0xC1)
        self.write_data(0x41)
        self.write_command(0xC5)
        self.write_data(0x00)
        self.write_data(0x0A)
        self.write_data(0x80)
        self.write_command(0xB1)
        self.write_data(0xB0)
        self.write_data(0x11)
        self.write_command(0xB4)
        self.write_data(0x02)
        self.write_command(0xB6)
        self.write_data(0x02)
        self.write_data(0x42)
        self.write_command(0xB7)
        self.write_data(0xc6)
        self.write_command(0xBE)
        self.write_data(0x00)
        self.write_data(0x04)
        self.write_command(0xE9)
        self.write_data(0x00)
        self.write_command(0x36)
        self.write_data((1<<3)|(0<<7)|(1<<6)|(1<<5))
        self.write_command(0x3A)
        self.write_data(0x66)
        self.write_command(0xE0)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_data(0x10)
        self.write_data(0x09)
        self.write_data(0x17)
        self.write_data(0x0B)
        self.write_data(0x41)
        self.write_data(0x89)
        self.write_data(0x4B)
        self.write_data(0x0A)
        self.write_data(0x0C)
        self.write_data(0x0E)
        self.write_data(0x18)
        self.write_data(0x1B)
        self.write_data(0x0F)
        self.write_command(0xE1)
        self.write_data(0x00)
        self.write_data(0x17)
        self.write_data(0x1A)
        self.write_data(0x04)
        self.write_data(0x0E)
        self.write_data(0x06)
        self.write_data(0x2F)
        self.write_data(0x45)
        self.write_data(0x43)
        self.write_data(0x02)
        self.write_data(0x0A)
        self.write_data(0x09)
        self.write_data(0x32)
        self.write_data(0x36)
        self.write_data(0x0F)
        self.write_command(0x11)
        time.sleep(0.12)
        self.write_command(0x29)

        dlog("initialized")

    def write_command(self, b):
        CS_PIN = 8
        DC_RS = 5
        MODE_CMD = 0
        MODE_DATA = 1

        GPIO.output(CS_PIN, GPIO.LOW)
        GPIO.output(DC_RS, MODE_CMD)

        self.spi.xfer([b])
        GPIO.output(CS_PIN, GPIO.HIGH)

    def write_data(self, b):
        CS_PIN = 8
        DC_RS = 5
        MODE_CMD = 0
        MODE_DATA = 1

        GPIO.output(CS_PIN, GPIO.LOW)
        GPIO.output(DC_RS, MODE_DATA)

        self.spi.xfer([b])
        GPIO.output(CS_PIN, GPIO.HIGH)

    def window(self, sx, sy, ex, ey):
        self.write_command(0x2a)
        self.write_data(sx >> 8)
        self.write_data(sx & 0xff)
        self.write_data(ex >> 8)
        self.write_data(ex & 0xff)

        self.write_command(0x2b)
        self.write_data(sy >> 8)
        self.write_data(sy & 0xff)
        self.write_data(ey >> 8)
        self.write_data(ey & 0xff)

        self.write_command(0x2c)

    def show(self, text, x, y):
        self.window(x, y, x + 8 - 1, y + 8 - 1)
        for i in range(16):
            for j in range(int(16 / 2)):
                self.window(i, j, i, j)
                self.write_data(0)
                self.write_data(0)
                self.write_data(0)

    def reset(self):
        RESET_PIN = 6
        RESET = 0
        RESET_RELEASE = 1

        GPIO.output(RESET_PIN, RESET)
        time.sleep(0.01)
        GPIO.output(RESET_PIN, RESET_RELEASE)
        time.sleep(0.2)

    def finalize(self):
        GPIO.cleanup()

