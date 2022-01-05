from fredapi import Fred
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams as rc
import seaborn as sns

api_key = f'<insert key>'
fred = Fred(api_key=api_key)


def data_fetch():
    sp = fred.get_series("SP500", observation_start="2013", observation_end="2021").resample("W").first()
    m2 = list(fred.get_series("WM2NS", observation_start="2013", observation_end="2021"))
    m2.append(19345.2)  # added as an estimate, likely a low one
    m = pd.Series(m2)
    s = sp.reset_index()
    s = s.drop(columns=[0])
    mm = pd.concat([s, m], axis=1)
    mm = mm.set_index("index")
    mm.columns = [''] * len(mm.columns)

    tym = fred.get_series("MORTGAGE30US", observation_start="2013", observation_end="2021").resample("W").first()
    df = pd.concat([sp, tym, mm], axis=1)
    df.columns = ["S&P 500", "30 Year Mortgage", "M2 Money Supply"]

    return df


def graphic(data, save=False):
    d = data.corr()
    rc['figure.figsize'] = 13, 8
    plt.figure(facecolor='darkgrey')
    sns.heatmap(data=d)
    plt.title("Correlation between M2 Money Supply & Other Indicators", fontsize=20, x=.6, y=1.05)
    if save is False:
        plt.show()
    else:
        plt.savefig("Money & Rates")


if __name__ == "__main__":
    graphic(data_fetch(), True)
