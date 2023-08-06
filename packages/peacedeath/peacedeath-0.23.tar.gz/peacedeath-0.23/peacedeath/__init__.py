from typing import Callable

from peacedeath.valves import Valves
from peacedeath.photodiodes import Photodiodes
from peacedeath.od_measurement import ODmeasurement
from peacedeath.pumps import Pumps
from peacedeath import pm
import pandas as pd
import os

OD_CALIBRATION_DATA_FILENAME = "OD_calibration_data.csv"
PUMP_CALIBRATION_DATA_FILENAME = "PUMP_calibration_data.csv"
RAW_OD_DATA_FILENAME = "RAW_OD_data.csv"
OD_DATA_FILENAME = "OD_data.csv"


class Experiment:
    def __init__(self, name="NewExperiment", connect=True, device_serial="auto"):
        """
        :param name: Experiment name with no spaces, e.g. starting date
        :param device_serial: board serial number or "auto" to auto-connect
        """
        assert " " not in name
        self.directory = name
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        if connect:
            self.dev = self.connect_device(device_serial=device_serial)
        else:
            self.dev = None
            print("Not connected to device")
        self.Valves = Valves(self)
        self.Photodiodes = Photodiodes(self)
        self.OD_measurement = ODmeasurement(self)
        self.Pumps = Pumps(self)

    def mix(self, speed=70, period=3000):
        assert 30 <= speed <= 100 or speed == 0
        if speed > 0:
            state = 1
        else:
            state = 0
        pulseWidth = int(period*speed/100)
        period = int(period)
        self.dev.request(pm.dev_msg.SetMixerStateRequest(state=state, period=period, pulseWidth=pulseWidth))
        return

    def connect_device(self, device_serial="auto"):
        # hub = pm.PMHub.local()
        hub = pm.PMHub("tcp://localhost:5555")
        if device_serial == "auto":
            dev = hub.get_devices()[0]
            self.dev = dev
            return dev
    def test_device(self):
        for t in range(7):
            self.Photodiodes.measure_current(t,3,20)

