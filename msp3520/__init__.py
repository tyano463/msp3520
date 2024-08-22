#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import RPi.GPIO as GPIO
import spidev
import time
import msp3520.definitions as D
from PIL import Image, ImageDraw, ImageFont


class Singleton(object):
    @classmethod
    def get_instance(cls, input):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(input)
        else:
            cls._instance.input = input
        return cls._instance


class MSP3520(Singleton):
    DEFAULT_FONT_SIZE = 12
    text = []
    pin = [-1, -1, -1, -1]
    font = None
    font_path = None
    font_size = None

    def set_pin(self, bl, dc, rs, cs):
        if bl < 0:
            self.pin[D.iBACK_LIGHT] = D.PIN_BACK_LIGHT
        else:
            self.pin[D.iBACK_LIGHT] = bl
        if dc < 0:
            self.pin[D.iDC_RS] = D.PIN_DC_RS
        else:
            self.pin[D.iDC_RS] = dc
        if rs < 0:
            self.pin[D.iRESET] = D.PIN_RESET
        else:
            self.pin[D.iRESET] = rs
        if cs < 0:
            self.pin[D.iCS] = D.PIN_CS
        else:
            self.pin[D.iCS] = cs

    def set_font(self, font_path, font_size):
        self.font_path = font_path
        self.font_size = font_size
        if (not isinstance(font_path, str)) or (len(font_path) == 0) or (not os.path.isfile(font_path)):
            self.font = ImageFont.load_default()
            # print("font is default")
        else:
            self.font = ImageFont.truetype(font_path, font_size)
            # print("font is " + font_path + " (" + str(font_size) + ")")

    def __init__(self, font_path='', font_size=DEFAULT_FONT_SIZE, backlight_pin=-1, dc_rs_pin=-1, reset_pin=-1,
                 cs_pin=-1):

        self.set_pin(backlight_pin, dc_rs_pin, reset_pin, cs_pin)
        self.set_font(font_path, font_size)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin[D.iBACK_LIGHT], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.pin[D.iRESET], GPIO.OUT, initial=D.RESET_RELEASE)
        GPIO.setup(self.pin[D.iDC_RS], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.pin[D.iCS], GPIO.OUT, initial=GPIO.HIGH)

        self.reset()

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 40000000
        self.spi.mode = 0
        self.spi.bits_per_word = 8

        self.write_command(D.ILI9488_POWER_CONTROL_1)
        self.write_data(D.VREG1OUT_POSITIVE_GAMMA_46250)
        self.write_data(D.VREG2OUT_NEGATIVE_GAMMA_m41250)
        self.write_command(D.ILI9488_POWER_CONTROL_2)
        self.write_data(0x41)
        self.write_command(D.ILI9488_VOLTAGE_COMMON_CONTROL)
        self.write_data(0x00)
        self.write_data(0x0A)
        self.write_data(0x80)
        self.write_command(D.ILI9488_FRAME_RATE_CONTROL)
        self.write_data(0xB0)
        self.write_data(0x11)
        self.write_command(D.ILI9488_DISPLAY_INVERSION_CONTROL)
        self.write_data(0x02)
        self.write_command(D.ILI9488_DISPLAY_FUNCTION_CONTROL)
        self.write_data(0x02)
        self.write_data(0x42)
        self.write_command(D.ILI9488_ENTRY_MODE_SET)
        self.write_data(0xc6)
        self.write_command(D.ILI9488_HS_LANES_CONTROL)
        self.write_data(0x00)
        self.write_data(0x04)
        self.write_command(D.ILI9488_SET_IMAGE_FUNCTION)
        self.write_data(0x00)
        self.write_command(D.ILI9488_MEMORY_ACCESS_CONTROL)
        self.write_data((1 << 3) | (0 << 7) | (1 << 6) | (1 << 5))
        self.write_command(D.ILI9488_INTERFACE_PIXEL_FORMAT)
        self.write_data(0x66)
        self.write_command(D.ILI9488_POSITIVE_GAMMA_CONTROL)
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
        self.write_command(D.ILI9488_NEGATIVE_GAMMA_CONTROL)
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
        self.write_data(D.ILI9488_READ_DISPLAY_SELF_DIAGNOSTIC_RESULT)
        self.write_command(D.ILI9488_SLEEP_OUT)
        time.sleep(0.12)
        self.write_command(D.ILI9488_DISPLAY_ON)

    def write_command(self, b):

        GPIO.output(self.pin[D.iCS], GPIO.LOW)
        GPIO.output(self.pin[D.iDC_RS], D.MODE_CMD)

        self.spi.xfer([b])
        GPIO.output(self.pin[D.iCS], GPIO.HIGH)

    def write_data(self, b):
        GPIO.output(self.pin[D.iCS], GPIO.LOW)
        GPIO.output(self.pin[D.iDC_RS], D.MODE_DATA)

        self.spi.xfer([b])
        GPIO.output(self.pin[D.iCS], GPIO.HIGH)

    def write_data_array(self, data):
        GPIO.output(self.pin[D.iCS], GPIO.LOW)
        GPIO.output(self.pin[D.iDC_RS], D.MODE_DATA)
        self.spi.xfer(data)
        GPIO.output(self.pin[D.iCS], GPIO.HIGH)

    def window(self, sx, sy, ex, ey):
        self.write_command(D.ILI9488_COLUMN_ADDRESS_SET)
        self.write_data(sx >> 8)
        self.write_data(sx & 0xff)
        self.write_data(ex >> 8)
        self.write_data(ex & 0xff)

        self.write_command(D.ILI9488_PAGE_ADDRESS_SET)
        self.write_data(sy >> 8)
        self.write_data(sy & 0xff)
        self.write_data(ey >> 8)
        self.write_data(ey & 0xff)

        self.write_command(D.ILI9488_MEMORY_WRITE)

    def write_pixel(self, color):
        self.write_data((color >> 8) & 0xf8)
        self.write_data((color >> 3) & 0xfc)
        self.write_data((color & 0x1f) << 3)

    def show(self, _text, x, y, size=DEFAULT_FONT_SIZE, color=0):
        if not isinstance(_text, str):
            return

        if (not self.range_x(x)) or (not self.range_y(y)):
            return

        lh = size + int(size / 2)
        if (not self.range_x(x + lh)) or (not self.range_y(y + lh)):
            return

        self.clear()

        text = _text.split('\n')
        for i in range(len(text)):
            self.write_text_line(x, y + (i * lh), D.WIDTH, y + ((i + 1) * lh), text[i], size, color)

    def show_image(self, img):
        """
        :param img: PIL.Image.Image
        :return:
        """
        if not isinstance(img, Image.Image):
            return

        image = img.resize((D.WIDTH, D.HEIGHT))
        self.window(0, 0, D.WIDTH, D.HEIGHT)
        pixel_data = []
        for y in range(D.HEIGHT):
            for x in range(D.WIDTH):
                r, g, b = image.getpixel((x, y))
                pixel_data.append(Color.from_rgb(r, g, b))

        data_to_write = bytearray()
        for pixel_color in pixel_data:
            data_to_write.extend([
                (pixel_color >> 8) & 0xf8,
                (pixel_color >> 3) & 0xfc,
                (pixel_color & 0x1f) << 3
            ])
            if len(data_to_write) > (3 * D.MAX_TRANSFER_SIZE):
                self.write_data_array(data_to_write)
                data_to_write.clear()

        self.window(0, 0, D.WIDTH, D.HEIGHT)

    def show_line(self, _text, size=DEFAULT_FONT_SIZE, color=0xffffffff):
        """
        add line
        if exceed max line, scroll
        :param _text: string to display
        :param size:  font size
        :param color: font color
        :return:
        """
        if not isinstance(_text, str):
            return
        if color == 0xffffffff:
            color = Color.BLACK

        lh = size + int(size / 2)
        max_line = int(D.HEIGHT / lh)
        text = _text.split('\n')

        exists_lines = len(self.text)
        add_lines = len(text)
        if (exists_lines + add_lines) <= max_line:
            # print("l:" + str(add_lines))
            for i in range(add_lines):
                self.write_text_line(0, (exists_lines + i) * lh, D.WIDTH, (exists_lines + i + 1) * lh, text[i], size,
                                     color)
            self.text.extend(text)
        else:
            # need screen update
            self.text.extend(text)
            self.text = self.text[-max_line:]
            # print("len:" + str(len(self.text)) + " / " + str(max_line))
            self.clear()
            for i in range(len(self.text)):
                self.write_text_line(0, i * lh, D.WIDTH, (i + 1) * lh, self.text[i], size, color)

    def clear(self):
        self.window(0, 0, D.WIDTH - 1, D.HEIGHT - 1)
        self.write_pixel(Color.WHITE)
        self.text = []

    def reset(self):
        GPIO.output(self.pin[D.iRESET], D.RESET)
        time.sleep(0.01)
        GPIO.output(self.pin[D.iRESET], D.RESET_RELEASE)
        time.sleep(0.2)

    def finalize(self):
        GPIO.cleanup()

    def valid_position(self, v, s, e):
        return (s <= v) and (v <= e)

    def range_x(self, x):
        return self.valid_position(x, 0, D.WIDTH)

    def range_y(self, y):
        return self.valid_position(y, 0, D.HEIGHT)

    def write_text_line(self, sx, sy, ex, ey, text, size, color):
        if (not self.range_x(sx)) or (not self.range_x(ex) or (not self.range_y(sy)) or (not self.range_y(ey))):
            return

        image = Image.new("RGB", (ex - sx, ey - sy), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        position = (0, 0)

        # print(f"({sx}, {sy}), ({ex},{ey})")
        if size != self.font_size:
            self.set_font(self.font_path, size)

        draw.text(position, text, fill="black", font=self.font)
        color_map = {1: color, 0: Color.WHITE}
        pixel_data = []

        data_to_write = bytearray()
        for y in range(ey - sy):
            for x in range(ex - sx):
                r, g, b = image.getpixel((x, y))
                pixel_color = color_map[int(r < 100 and g < 100 and b < 100)]
                pixel_data.append(pixel_color)

        self.window(sx, sy, ex, ey)

        data_to_write.clear()
        for pixel_color in pixel_data:
            data_to_write.extend([
                (pixel_color >> 8) & 0xf8,
                (pixel_color >> 3) & 0xfc,
                (pixel_color & 0x1f) << 3
            ])
            if len(data_to_write) >= (3 * D.MAX_TRANSFER_SIZE):
                self.write_data_array(data_to_write)
                data_to_write.clear()

        self.window(0, 0, D.WIDTH - 1, D.HEIGHT - 1)


class Color:
    WHITE = 0xffff
    BLACK = 0
    RED = 0xF800
    Green = 0x7E0
    BLUE = 0x1f

    @staticmethod
    def from_rgb(r, g, b):
        # convert to 5,6,5 bit
        _r = int((r / 255) * (1 << 5))
        _g = int((g / 255) * (1 << 6))
        _b = int((b / 255) * (1 << 5))

        return (_r << 11) | (_g << 5) | _b

    @staticmethod
    def to_rgb(color):
        _r = (color & 0xf8) >> 11
        _g = (color & 0x7E) >> 5
        _b = (color & 0x1f)

        r = min(255, _r * 256 / (1 << 5))
        g = min(255, _g * 256 / (1 << 6))
        b = min(255, _b * 256 / (1 << 5))
        return r, g, b


__all__ = ['Color', 'MSP3520']
