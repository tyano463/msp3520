# MSP3520 Library

 This is a Python wrapper for displaying text
on the MSP3520 display connected to a raspi.

## Dependency

- RPi.GPIO
- PIL
- spidev

## Installation

```bash
git clone git@github.com:tyano463/msp3520.git
cd msp3520
sudo python3 setup.py develop
```

## How to use

```python

from msp3520 import MSP3520
from PIL import Image
import random

# initialize
display = MSP3520()

# when use multibyte character, need font
# display = MSP3520(font_path='NotoSansCJKjp-Regular.otf')

display.clear()

# show text
display.show("Hello", 200, 100)

time.sleep(2)

# show image
f = "tomato.jpg"
img = Image.open(f)
display.show_image(img)

time.sleep(2)

# add line (with scroll)
sample_data = [''.join(chr(random.randint(0x21, 0x7d)) for _ in range(20)) for _ in range(100)]
display.clear()
for i in range(len(sample_data)):
    display.show_line(s)

```
