# IOT Related Scripts

## Installation
1. Install the Humidity Sensor (Sense HAT) dependencies
```
sudo apt update
sudo apt install sense-hat
```

1. Install the CO2 CCS811 Sensor dependencies
```
cd ~/
sudo pip3 install --upgrade adafruit-python-shell
sudo pip3 install adafruit-circuitpython-ccs811
```

1. Open /boot/config.txt & find the dtparam block
```
sudo vim /boot/config.txt
```

1. Enable I2C clock stretching by adding or uncommenting the following lines
```
dtparam=i2c_arm=on
#dtparm=i2s=on
dtparam=spi=on
# Clock stretching by slowing down to 10KHz
dtparam=i2c_arm_baudrate-10000
```

1. Reboot the pi
```
sudo reboot
```

## Usage
1. Run the script to read the hardware
```
cd app/
./hardware.py --verbose
```