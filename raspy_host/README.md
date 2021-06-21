# raspy_host
Test on raspberry pi OS lite - Linux raspberrypi 5.4.83+

## Install
clone to ~/

run script in setup folder

resulting executable is "raspy_host/src/raspy_host" 

add something to /etc/rc.local (before "exit 0") that does something like:

```bash
cur_dir=$(pwd)
cd /home/pi/raspy_host/src
sudo ./raspy_host &
cd $cur_dir
```

## Use

1) boot pi
2) connect USB midi adapter and USB midi instrument 
3) ???????????
4) Profit 




# Resources
Display:
https://thepihut.com/products/52pi-0-91-128x32-oled-screen-for-raspberry-pi
https://wiki.52pi.com/index.php/0.91_Inch_OLED_Module_SKU:_EP-0060
https://wiki.52pi.com/index.php/0.91_OLED_(English)

USB Hub:
http://www.waveshare.com/wiki/USB_HUB_HAT
https://thepihut.com/products/4-port-usb-hub-phat-for-raspberry-pi-zero

USB midi adapter - any
