import pandas as pd
import numpy as np
import time
import os

OD_FRONT_CALIBRATION_FILENAME = "od_front_calibration_data.csv"
OD_SIDE_CALIBRATION_FILENAME = "od_side_calibration_data.csv"


class ODmeasurement:
    def __init__(self, pe):
        self.pe = pe
        self.dev = pe.dev
        self.calibration_file_front = os.path.join(self.pe.name, OD_FRONT_CALIBRATION_FILENAME)
        self.calibration_file_side = os.path.join(self.pe.name, OD_SIDE_CALIBRATION_FILENAME)
        if os.path.exists(self.calibration_file_front):
            self.calibration_functions = [self.fit_calibration_curve(t) for t in range(7)]

    def collect_calibration_data(self, calibration_OD_values=None, starting_index=0):

        CurrentFront = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6], index=calibration_OD_values)
        CurrentSide = pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6], index=calibration_OD_values)

        for i in range(starting_index, 7):
            instructions = "Please arrange tubes as follows:\n"
            for t in range(7):
                instructions += "OD_value {OD} in tube slot {t}\n".format(OD=calibration_OD_values[(i + t) % 7], t=t)
            instructions += "input x to exit"
            next_step = input(instructions)
            if next_step.lower() == "x":
                break
            else:
                for t in range(7):
                    self.pe.mix(100)
                    time.sleep(3)
                    self.pe.mix(0)
                    time.sleep(0.5)
                    IFS, ISS = self.pe.Photodiodes.measure_current(t)
                    CurrentFront.loc[calibration_OD_values[(i + t) % 7], t] = IFS
                    CurrentSide.loc[calibration_OD_values[(i + t) % 7], t] = ISS
                    CurrentFront.to_csv(self.calibration_file_front)
                    CurrentSide.to_csv(self.calibration_file_side)
                    print(CurrentFront)
                    print(CurrentSide)
            print("Done collecting calibration data!")

    def fit_calibration_curve(self, tube=0):
        df = pd.read_csv(self.calibration_file_front)
        current = df.loc[:, tube]
        OD = np.array(df.index).ravel()
        x = np.log(current)
        y = np.log(OD + 1)

        coefficients = np.polyfit(x, y, 4)
        poly = np.poly1d(coefficients)

        def current_to_OD(current):
            x = np.log(current)
            y = poly(x)
            OD = np.exp(y) - 1
            return OD

        return current_to_OD

    def calculate_OD(self, FrontCurrent, tube):
        f = self.calibration_functions[tube]
        return f(FrontCurrent)
