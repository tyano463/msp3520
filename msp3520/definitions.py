#!/usr/bin/env python3
# -*- coding: utf-8 -*-

iBACK_LIGHT = 0
iDC_RS = 1
iCS = 2
iRESET = 3

PIN_BACK_LIGHT = 25
PIN_DC_RS = 5
PIN_CS = 8
PIN_RESET = 6
MODE_CMD = 0
MODE_DATA = 1

RESET = 0
RESET_RELEASE = 1

WIDTH = 480
HEIGHT = 320

MAX_TRANSFER_SIZE = 1024

ILI9488_READ_DISPLAY_SELF_DIAGNOSTIC_RESULT = 0x0f
ILI9488_SLEEP_OUT = 0x11
ILI9488_DISPLAY_ON = 0x29
ILI9488_COLUMN_ADDRESS_SET = 0x2a
ILI9488_PAGE_ADDRESS_SET = 0x2b
ILI9488_MEMORY_WRITE = 0x2c
ILI9488_MEMORY_ACCESS_CONTROL = 0x36
ILI9488_INTERFACE_PIXEL_FORMAT = 0x3a
ILI9488_FRAME_RATE_CONTROL = 0xb1
ILI9488_DISPLAY_INVERSION_CONTROL = 0xb4
ILI9488_DISPLAY_FUNCTION_CONTROL = 0xb6
ILI9488_ENTRY_MODE_SET = 0xb7
ILI9488_HS_LANES_CONTROL = 0xbe
ILI9488_POWER_CONTROL_1 = 0xc0
ILI9488_POWER_CONTROL_2 = 0xc1
ILI9488_VOLTAGE_COMMON_CONTROL = 0xc5
ILI9488_POSITIVE_GAMMA_CONTROL = 0xe0
ILI9488_NEGATIVE_GAMMA_CONTROL = 0xe1
ILI9488_SET_IMAGE_FUNCTION = 0xe9

VREG1OUT_POSITIVE_GAMMA_46250 = 0x11
VREG2OUT_NEGATIVE_GAMMA_m41250 = 0x09
