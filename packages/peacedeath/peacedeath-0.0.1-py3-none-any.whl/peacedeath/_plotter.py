import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot(self, maximum=1, index=1, xmin=0, xmax=None, figsize=[14, 6], savefig=False,
         fast=False, tubes=None,
         tubenames=["0-Ctrl", "1-E.Coli", "2-E.Coli", "3-Ctrl", "4-MilkyXG", "5-Ctrl", "6-Ctrl"]):
    assert index in [1, 2, 3, 4]
    assert maximum is None or maximum == 1 or type(maximum) == list
    if not fast:
        self.df_update()

    l, h = [0, self.df.shape[0]]

    if type(xmin) is int:
        xmin = str(xmin) + "h"
    if type(xmax) is int:
        xmax = str(xmax) + "h"
    timemin = self.df.time[0] + pd.Timedelta(xmin)
    if xmax is not None:
        timemax = self.df.time.iloc[0] + pd.Timedelta(xmax)
    else:
        timemax = self.df.time.iloc[-1]

    # Transmittance measurements
    # meas=self.df.iloc[int(l+(h-l)*xmin):int(h-(h-l)*(1-xmax)),index::4].astype(int)
    meas = self.df[(self.df.time > timemin) & (self.df.time < timemax)].iloc[:, index::4].astype(int)

    meas.columns = tubenames
    if tubes is not None:
        assert all(x in range(7) for x in tubes)
        meas = meas.iloc[:, tubes]
    else:
        tubes = list(range(7))

    #         pe.pumptimes=pe.pumptimes[pe.pumptimes.tube<7]
    #         assert all(t in [0,1,2,3,4,5,6] for t in self.pumptimes.tube.unique())

    if maximum == 1:
        meas = meas / meas.max(0)
    if type(maximum) == list:
        maximum=np.array(maximum)
        meas = 0.4*(meas - maximum) / (11500-maximum)
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=figsize, gridspec_kw={"height_ratios": [3, 1]})
    ax_OD, ax_pump = axs

    #         plt.tight_layout()
    ax_OD.plot(self.df.time[(self.df.time > timemin) & (self.df.time < timemax)], meas, "o:", markersize=0.4)
    ax_OD.invert_yaxis()
    pumptimes = self.pumptimes[(self.pumptimes.time > timemin) & (self.pumptimes.time < timemax)].copy()

    #         pumptimes.vol/=10 #total pumped volume
    #         pumptimes.vol*=50 #ug/ml

    for t in tubes:
        plt.plot("time", "vol", data=pumptimes[(pumptimes.tube == t) & (pumptimes.pump == "death")],
                 marker="x", linestyle=":")
    plt.gca().set_prop_cycle(None)
    for t in tubes:
        plt.plot("time", "vol", data=pumptimes[(pumptimes.tube == t) & (pumptimes.pump == "peace")],
                 marker="o", linestyle=":", fillstyle="none", alpha=0.7)
    plt.gca().set_prop_cycle(None)
    for t in tubes:
        plt.plot("time", "vol", data=pumptimes[(pumptimes.tube == t) & (pumptimes.pump == "vacuum")],
                 marker="^", linestyle="None", fillstyle="none", alpha=0.2)

    if len(tubes) == 1:
        t = tubes[0]
        data = pumptimes[(pumptimes.tube == t) & (pumptimes.pump == "death")]
        A = data.time
        B = data.vol
        for xy in zip(A, B):  # <--
            plt.annotate('%.1f' % xy[1], xy=xy, textcoords='data')  # <--

    ax_pump.set_title("Pumped volumes blablablablabla")
    ax_pump.set_ylabel("Vol [ml]")
    ax_OD.set_ylabel("OD")
    ax_OD.legend(meas.columns)
    ax_OD.set_title("Growth curve")
    #         ax_OD.set_yticks([])

    plt.xticks(rotation="vertical");
    axs[0].grid()
    axs[1].grid()
    if savefig:
        plt.savefig(self.files.main_folder + "/" + savefig, dpi=300, bbox_inches='tight')
        plt.close()
    return axs