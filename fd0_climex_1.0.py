import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: FD0
Definition: [Number of frost days]. Let TN be daily maximum temperature. Annual count of days when TN < 0 °C.
Version 1.0, 2021-07-08
"""
# csv input files must have the following format name "[station_number(5 digits)]_TN_d.csv"
for filename in glob.glob("*_TN_d.csv"):
    fd0_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            fd0 = len(df[df.index.year == y][df < 0].dropna())  # Counting days below 0 Celsius for every year
            fd0_lst.append(fd0)
        else:
            fd0 = float("NaN")
            fd0_lst.append(fd0)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Year": dates, "FD0 (# of days)": fd0_lst})
    df_output.to_csv("fd0_" + filename[:5] + ".csv", sep=";", index=False)
