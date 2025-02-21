# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 22:21:09 2025

@author: Violet
"""

# Import Libraries
from Modules.GLComponents import ssi, wells, well_callback

# Configure the Wells
wells.configure(
    [7,1,2,3,4,5,6],        #  Well Ports
    [15,9,10,11,12,13,14],  #  Pump Ports
    {'all': ((0, 12), 7)}   #  Uncued, Reward Function 12 (150uL)
)

# Activate the Wells, and Turn On the LEDs
wells.activate('all', True)

@ssi.command
def UP(well):
    well.led.on()

@ssi.command
def DOWN(well):
    well.led.off()
    well.activate()

callback = well_callback