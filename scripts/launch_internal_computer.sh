#!/bin/bash

eval "$(cat ~/.bashrc | tail -n +10)"

until ntpdate -u 10.15.20.3
do 
  sleep 1 
done 

until ifconfig panther_can && rostopic list
do
  sleep 1
done
sleep 5
roslaunch panther_driver driver.launch