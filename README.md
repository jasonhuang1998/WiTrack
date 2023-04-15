# WiTrack
## Table of Content
- [Introduction](#introduction)
- [Input Files](#input-files)
- [Configs](#configs)
- [Output](#output)
- [Usage](#usage)
- [Requirements](#requirements)
- [Reference](#reference)
## Introduction
Implement the algorithm in "WiTrack: Human-to-Human Mobility Relationship Tracking in Indoor Environments Based on Spatio-Temporal Wireless Signal Strength".
## Input Files
1. Create a folder in ./rawdata named with the date of the experiment.
2. Put wireless files in it.
## Output
The Confusion Matrix and classification report of the result.
## Configs
Create a yaml config file in ./config and put all the parameters in the config file in the format shown in the example already in ./config.
- date : experiment date
- module : run selected modules
- model : 
    * leader follower max time : the max shift time to calculate leader follower feature
    * show shift time : the time window
    * time shift : shift time for each testing data
    * independent threshold : if the similarity between the two cellphones is below this value, they will be considered independent.
    * companion threshold : if the difference between the maximum value and the value without any shift is greater than it, then it will be considered as a leader-follower
- savgol : the parameter of savgol smoothing filter
- sniffer list : the list of sniffers that needs to be calculated
- mobile list : the mobile list and their uuid
- relation list : the relation between each pair of cellphones
    * 0 : companion
    * 1 : leader-follower
    * 2 : independent
- start/end time : the start/end time of the experiment
## Usage
```
pip install pipenv
pipenv install
pipenv run python main.py
```
# Reference
T. -H. Chen, S. -I. Sou and Y. Lee, "WiTrack: Human-to-Human Mobility Relationship Tracking in Indoor Environments Based on Spatio-Temporal Wireless Signal Strength," 2019 IEEE Intl Conf on Dependable, Autonomic and Secure Computing, Intl Conf on Pervasive Intelligence and Computing, Intl Conf on Cloud and Big Data Computing, Intl Conf on Cyber Science and Technology Congress (DASC/PiCom/CBDCom/CyberSciTech), Fukuoka, Japan, 2019, pp. 788-795, doi: 10.1109/DASC/PiCom/CBDCom/CyberSciTech.2019.00146.