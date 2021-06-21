1)如何启动Pi 2的支持,首先需要查看以下文档Pi 2配置部分:
http://www.airspayce.com/mikem/bcm2835/
2)在所有编译之前,需要安装以下包,以启用I2C DMA硬件访问.
sudo apt-get install build-essential git-core libi2c-dev i2c-tools lm-sensors
3)需要修改/etc/modules加入以下字段启动I2C硬件配置.
i2c-bcm2708
i2c-dev
4)在主目录进行sudo make编译库,安装库.在example目录进行make编译范例.