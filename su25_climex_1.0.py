import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: SU25
Definition: [Number of summer days]: Let TX be daily maximum temperature. Annual count when TX > 25 °C.
Version 1.0, 2021-07-08
"""

# csv input files must have the following format name "[station_number(5 digits)]_TX_d.csv"
for filename in glob.glob("*_TX_d.csv"):
    su25_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            su25 = len(df[df.index.year == y][df > 25].dropna())  # Counting days above 25 Celsius for every year
            su25_lst.append(su25)
        else:
            su25 = float("NaN")
            su25_lst.append(su25)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Year": dates, "SU25 (# of days)": su25_lst})
    df_output.to_csv("su25_" + filename[:5] + ".csv", sep=";", index=False)
