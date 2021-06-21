#!/bin/bash
sudo apt-get install -y build-essential git-core libi2c-dev i2c-tools lm-sensors

if [[ $(cat /etc/modules | grep bcm2708 | wc -l) -eq 0 ]]; then
  echo "i2c-bcm2708" | sudo tee -a /etc/modules
fi

if [[ $(cat /etc/modules | grep "i2c-dev" | wc -l) -eq 0 ]]; then
  echo "i2c-dev" | sudo tee -a /etc/modules
fi

root_dir=$(git rev-parse --show-toplevel)
cd "${root_dir}/oled"
sudo make
cd ../src
make
cd ..
