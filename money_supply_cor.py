from fredapi import Fred
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams as rc
import seaborn as sns

"""
This app uses macroeconomic data from FRED to give some context as to what's happening in the economy. It focuses
on how the M2 money supply relates to the S&P 500, GDP, Home Prices, and for good measure incorporates the 30 Year 
mortgage rate as that's probably the most important rate to the consumer.  
"""

api_key = f'<YOUR_KEY_HERE>'
fred = Fred(api_key=api_key)


def macro_data():
    """
    Imports data from FRED. Slices into DataFrame
    :return: DataFrame
    """
    sp = fred.get_series("SP500", observation_start="2012-12-31", observation_end="2021-07-01 ").resample("Q").first()
    sp = sp[:-1]
    m2 = fred.get_series("WM2NS", observation_start="2012-12-31").resample("Q").first()
    m2 = m2[:-2]
    tym = fred.get_series("MORTGAGE30US", observation_start="2012-12-22").resample("Q").first()
    tym = tym[:-3]
    hp = fred.get_series("MSPUS", observation_start="2013")
    gdp = fred.get_series("GDP", observation_start="2013")
    idx = gdp.reset_index()
    id = list(idx["index"])
    the_d = {"index": id, "S&P500": list(sp), "M2": list(m2), "ThirtyYearMortgage": list(tym),
             "HousingPrices": list(hp), "GDP": list(gdp)}
    data = pd.DataFrame(the_d)
    data = data.set_index("index")

    return data


def graphic(data, save=False):
    """
    Makes Heatmap of data
    :param data: dataframe from macro_data()
    :param save: False=Shows in IDE, True=Saved as png
    """
    d = data.corr()
    rc['figure.figsize'] = 13, 8
    plt.figure(facecolor='darkgrey')
    sns.heatmap(data=d)
    plt.title("Correlation between M2 Money Supply & Other Indicators", fontsize=20, x=.6, y=1.05)
    if save:
        plt.savefig("Money & assets")

    else:
        plt.show()
    plt.clf()


def normalized_graph(data, save=False):
    """
    Normalizes and graphs data from macro_data()
    :param data: DataFrame
    :param save: False=Shows in IDE, True=Saved as png
    :return:
    """
    hello = {}
    for col in data:
        mi = data[col].min()
        ma = data[col].max()
        temp = []
        for point in data[col]:
            nd = (point - mi) / (ma - mi)
            temp.append(nd)
        hello[col] = temp

    x = data.reset_index()
    df = pd.DataFrame(hello)
    df["index"] = x["index"]
    df = df.set_index("index")
    df = df[:-1]

    rc['figure.figsize'] = 13, 8
    plt.figure(facecolor='darkgrey')
    sns.set_style("darkgrid")
    ax = sns.lineplot(data=df)
    ax.set(yticklabels=[], xlabel="By Quarter", ylabel="Normalized Data")
    plt.title("Normalized Metrics by Quarter", fontsize=20, y=1.05)
    if save:
        plt.savefig("normalized graph")
    else:
        plt.show()


if __name__ == "__main__":
    df = macro_data()
    graphic(df, True)
    normalized_graph(df, True)
    print("Complete")





