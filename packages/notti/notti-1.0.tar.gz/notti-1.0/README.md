# python-notti
Python control for Notti lights
=========================================

A Python API for controlling Notti lights manufactured by Witti.

Example use
-----------

This will connect and set the Notti to the indicated RGB color.
```
import notti

light = notti.notti("78:A5:04:00:00:01")
light.connect()
#             red   green blue
light.set_rgb(0x00, 0x00, 0xff)
```

This will turn the bulb on (equivalent of light.set_rgb(0xff, 0xff, 0xff)
```
light.on()
```

This will turn the bulb off (equivalent of light.set_rgb(0x00, 0x00, 0x00)
```
light.off()
```

