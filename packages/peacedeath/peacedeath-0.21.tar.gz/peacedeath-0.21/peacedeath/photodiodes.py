import numpy as np
import matplotlib.pyplot as plt
from peacedeath import pm


class Photodiodes:
    def __init__(self, pe):
        self.pe = pe
        self.dev = pe.dev

    def measure_current(self, tube, cycles=10, n_measurements=40, laserOnDelay=10, laserOffDelay=10,
                        filter_errors=True, verbose=False):
        current_front, current_side = _measure_current(dev=self.dev, tube=tube, cycles=cycles,
                                                       n_measurements=n_measurements, laserOnDelay=laserOnDelay,
                                                       laserOffDelay=laserOffDelay, filter_errors=filter_errors,
                                                       verbose=verbose)
        return current_front, current_side


def get_4_signals(dev, tube, resistor1=100, resistor2=10, laserOnDelay=10, laserOffDelay=1,
                  cycles=10, bias=0):
    tube_remapping = {0: 0,
                      1: 3,
                      2: 1,
                      3: 5,
                      4: 2,
                      5: 6,
                      6: 4}
    tube = tube_remapping[tube]

    s4 = dev.request(pm.dev_msg.ODMeasureRequest(tube=tube, laserOnDelay=laserOnDelay,
                                                 laserOffDelay=laserOffDelay,
                                                 cycles=cycles,
                                                 bias=bias,
                                                 resistor1=resistor1,
                                                 resistor2=resistor2))

    return s4.onFS, s4.onSS, s4.offFS, s4.offFS


def get_r2list(dev, tube=4, n=20):
    assert n > 5
    r1 = 200
    r2 = 128
    cycles = 1
    v = np.nan
    while not 0.9 < v < 1.1 and 5 < r2 < 255:
        a = get_4_signals(dev=dev, tube=tube, resistor1=r1, resistor2=r2, laserOnDelay=10, laserOffDelay=10,
                          cycles=cycles, bias=0)
        v = [(3.3 / 4095) * i / (10 * cycles) for i in a]
        v = v[0]  # onFS
        r2 /= (v - 0.1)
        r2 = min(255, r2)
        r2 = max(1, r2)
        r2 = int(r2)
    #         print(r2,v)

    rmax = min(int(r2 * 1.2), 255)
    rmax = max(rmax, 6)

    if r2 > 159 and v <= 0.2:
        rmax = 255
    if r2 > 159 and v > 0.2:
        rmax = 127
    r2list = list(range(0, rmax))
    if rmax > n:
        step = rmax // n
        step = max(1, step)
        r2list = r2list[1::step]
    return r2list


def measure_voltage(dev, tube, cycles=10, n_measurements=40, laserOnDelay=10, laserOffDelay=10):
    rlist = get_r2list(dev, tube, n=n_measurements)
    r1 = 200
    V = []
    Rfs = []
    Rss = []
    if len(rlist) < n_measurements:
        cycles *= n_measurements / len(rlist)
        cycles = int(cycles)
        print("Cycles=", cycles)
    for r1_binary, r2_binary in zip(np.linspace(1, 255, len(rlist)).astype(int), rlist):
        #         print(r1_binary,r2_binary)
        u = get_4_signals(dev=dev, tube=tube, resistor1=r1_binary, resistor2=r2_binary, laserOnDelay=laserOnDelay,
                             laserOffDelay=laserOffDelay, cycles=cycles, bias=0)
        u = [(3.3 / 4095) * i / (10 * cycles) for i in u]
        V += [u]
        r2 = int(52 + r2_binary * 10000 / 256)
        r1 = int(52 + r1_binary * 10000 / 256)
        Rfs += [r2]
        Rss += [r1]
    Vfs = np.array(V)[:, 0]  # onFS
    Vss = np.array(V)[:, 2]  # onFS
    Rfs = np.array(Rfs)
    Rss = np.array(Rss)
    return Vfs, Rfs, Vss, Rss


def calculate_current(V, R, filter_errors=True):
    R = R[(V < 1.6)]
    V = V[(V < 1.6)]
    n = len(R)

    A = np.vstack((R, np.ones(n))).T
    fit = np.linalg.lstsq(A, V, rcond=None)
    current, voltage_bias = fit[0]
    resid = fit[1]
    rsquared = 1 - resid / (n * np.var(V))
    rsquared = rsquared[0]

    if filter_errors:
        #         print("R2=%.6f, I=%.2fuA, V_bias=%.3f unfiltered"%(rsquared,current*1e6,voltage_bias))
        err = (current * R + voltage_bias - V) ** 2
        valid_range = err < err.mean() + err.std()
        if any(valid_range):
            R = R[valid_range]
            V = V[valid_range]
            n = len(R)
            A = np.vstack((R, np.ones(n))).T
            fit = np.linalg.lstsq(A, V, rcond=None)
            current, voltage_bias = fit[0]
            resid = fit[1]
            rsquared = 1 - resid / (n * np.var(V))
    if n < 5:
        print("fit with less than 5 points!")
    current *= 1e6  # microAmps

    #     print("R2=%.6f, I=%.2fuA, V_bias=%.3f"%(rsquared,current,voltage_bias))
    return current, voltage_bias, rsquared


def _measure_current(dev, tube, cycles=10, n_measurements=40, laserOnDelay=10, laserOffDelay=10, filter_errors=True,
                     verbose=False):
    Vfs, Rfs, Vss, Rss = measure_voltage(dev=dev, tube=tube, cycles=cycles, n_measurements=n_measurements,
                                         laserOnDelay=laserOnDelay, laserOffDelay=laserOffDelay)
    IFS, _, R2FS = calculate_current(Vfs, Rfs, filter_errors=filter_errors)
    ISS, _, R2SS = calculate_current(Vss, Rss, filter_errors=filter_errors)

    if verbose:
        fig, axs = plt.subplots(2, 1)
        axs[0].plot(Rfs, Vfs, "ro--", label="Front Detector, I=%.1f μA" % IFS)
        axs[0].legend()
        axs[1].plot(Rss, Vss, "bo--", label="Side Detector, I=%.1f μA" % ISS)
        axs[1].legend()
        plt.xlabel("Resistance (Ohms)")
        axs[1].set_ylabel("Voltage")
        axs[0].set_ylabel("Voltage")
        plt.show()
    return IFS, ISS
