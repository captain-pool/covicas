# Covicas - A Light Weight Face Recognizer for Multiple Recoginizer Network

## Settings File
---------------------------
All the Cofiguration should be done in the settings file.
- The settings file Contains the `CAM_NUM` parameter, which specifies the ID of the camera of the Slave Network
- The `labelmap` parameter is generated during training time. **Do Not Touch!**
- The `slaves` parameter contains the list of IPs of the Camera Modules. To Add New Slave, add the IP of the Slave in the List.
  *The MQTT Ports of all the Slaves should be SAME.*

## Configuring the Runtime Parameters
----------------------------------------

``` bash
python3 main.py --help
python3 logger.py --help
python3 __trainer.py --help
```
To get the list of parameters.

## Setting Up
---------------------
-  On both the Master and the Slaves:
```bash
      bash ./opencv_install.sh
      sudo apt install mosquitto
```

## Starting Up the network
----------------------------
Add the IP of the Network to the `slaves` in settings file.
On the Nodes:
```bash
python3 main.py --nomaster
```
On the Master:
```bash
python3 main.py --master
```

To see the logs, run
```bash
python3 logger.py
```
To Follow while the Log Grows:
```bash
python3 logger.py --follow
```
