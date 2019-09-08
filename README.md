# Autonomous  Albot UAV project

[![Build Status](https://travis-ci.com/mkeyno/KeynoRobot.svg?branch=master)](https://travis-ci.com/mkeyno/KeynoRobot)
[![Python](https://img.shields.io/badge/Python-3.6%2B-red.svg)](https://www.python.org/downloads/)
![GitHub](https://img.shields.io/github/license/mkeyno/KeynoRobot.svg) 
![PyPI](https://img.shields.io/pypi/v/KeynoRobot.svg?color=green&label=pypi%20release)
![PyPI - Downloads](https://img.shields.io/pypi/dm/KeynoRobot.svg?label=PyPi%20Downloads)
[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/mmphego)

This is a repository of code, project information and hardware-software design for Albot UAV drone.  This project has been started on Centre for Artificial Intelligence Research (CAIR) at Auckland University of Technology dedicated to using Actec Firefly Hexacopter drone as tesh bench of Dr. Albert Cognitive mapping theory.

Cognitive maps are a natural cognition of many species to understand spatial environmental and utilized it to orientation and localization purposeDr. Albert  Cognitive mapping theory is the Computational approach base on learning of empiricalobservation base on the relation of successive View s model. Similar to many species which they observed and  remember snapshots (important object of 2D images) of a place and use them as part of their navigation strategy and special localization

# Goal & Mission
The final mission comprises flying autonomously and recognize the special environment and learn important object and used this acquired knowledge for map surveying and route creation

[![AscTech FireFly Hexacopter](https://github.com/mkeyno/KeynoRobot/blob/master/doc/firefly.png)](https://www.youtube.com/watch?v=bicupEW7gRw "AscTech FireFly Hexacopter")

-   ![link to fly on YouTube](https://www.youtube.com/watch?v=bicupEW7gRw)

### Hardware
Hardware comprised of one set of autopilot platform which is connected to the auxiliary system on module (SoM) by serial link. Due to a huge amount of image processing   Raspberry pi 4 with 4 GB RAM has been selected. Primarily attitude control and stabilization perform by onboard autopilot and all navigation and compensation performed by high-level API programTechnical Information & specification about this UAV located![ here ]( http://wiki.asctec.de/display/AR/AscTec+Firefly)
### Firmware 
The core program consists three coroutines and one sub coroutine, 
- first is the webserver which served the web application and broadcast data/video link through the local network, 
- second coroutine is the OpenCV module which is responsible to processing images captured by two HD camera for object detection, optical flow stabilization. 
- third coroutine is ROS platform responsible to acquire data from a physical sensor (LiDAR, ToF range finder, ultrasonic) and delivered to TensorFlow node. 
  * TensorFlow-Keras is the sub coroutine for data acquisition, Semantic Segmentation and classifies structured data(object ) into the feature columns. Those datasets comprise the primary simple objects such as vertical-horizontal lines (door, wall, windows, table) and complex objects (obstacles, hazardous area, routes)

 ![-](https://github.com/mkeyno/Small-Raspberry-Picker-Robot/blob/master/resources/python.jpg) 
 ![-](https://github.com/mkeyno/Small-Raspberry-Picker-Robot/blob/master/resources/ros.jpg) 
 ![-](https://github.com/mkeyno/Small-Raspberry-Picker-Robot/blob/master/resources/TensorFlow.jpg)

### Current Status
 - coroutines of OpenCV & Webserver installed
 - serial connection to the Autopilot established
 

### Next  Stage
install & test of Denseb Optical Flow  (Gunnar Farneback) & sparse optical flow ( Lucas–Kanade) library
+ add TLS security layer to web application
+ install LiDAR or ToF range finder sensor and connect them  to ROS master node
 
 ### installation
 This project need python 3.6+. to install th e package use ``` pip install KeynoRobot```
 then use ```python3 -m  KeynoRobot```
 open the browser at address ```127.0.0.1:8080``` or ```CAIR.local:8080```
 use admin & admin for user & password for login page 
 
![-](https://github.com/mkeyno/KeynoRobot/blob/master/doc/web.png)
