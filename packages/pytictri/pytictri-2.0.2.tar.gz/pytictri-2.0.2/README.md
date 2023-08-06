# pytictri - EDF teléinformation Python library

[![PyPI version](https://badge.fury.io/py/pytictri.svg)](https://badge.fury.io/py/pytictri)

This library allows you to retrieve teleinfo using serial port device (USBTICLCV2).

This library is a fork from pyticcom project. It adds three phases counter compatibility.

### Example

~~~
from pytictri import Teleinfo, Mode

with Teleinfo('/dev/tty.usbserial-DA4Y56SG', mode=Mode.HISTORY) as teleinfo:

    frame = teleinfo.read_frame()
    print(frame.get("PAPP"))
~~~
