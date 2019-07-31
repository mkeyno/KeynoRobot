# Fruit Detection by openCV , Tensorflow in ROS environment 

[![Build Status](https://travis-ci.com/mkeyno/KeynoRobot.svg?branch=master)](https://travis-ci.com/mkeyno/KeynoRobot)
[![Python](https://img.shields.io/badge/Python-3.6%2B-red.svg)](https://www.python.org/downloads/)
![GitHub](https://img.shields.io/github/license/mkeyno/KeynoRobot.svg) 
![PyPI](https://img.shields.io/pypi/v/KeynoRobot.svg?color=green&label=pypi%20release)
![PyPI - Downloads](https://img.shields.io/pypi/dm/KeynoRobot.svg?label=PyPi%20Downloads)
[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/mmphego)

 
The simplest code to catch the ripe red  berry fruit video frame in OpenCV and turn it to HSV format.then grab the upper and lower 
bounds of the color we would like to detect. In this case, we choose the values from yellow/red-ish to completely red.
We create a numpy array containing these and create mask to catch perfect color, but this simple approach prone to undesirable  
result, that's my many object detection  followed by **deep learning** module in OpenCV
***(dnn)***  is the OpenCV’s module to load a pre-trained object detection network. there are many method & framework for object 
detection using deep learning with different aspects of difficulty , implementation , speed and size
on platform such raspberry-pi 3b+ Network architectures such as  ***MobileNets*** along with SSD(Single Shot Detectors) framework is 
between our constraints and goals