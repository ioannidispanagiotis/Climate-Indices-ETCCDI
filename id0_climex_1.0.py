import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: ID0
Definition: [Number of ice days]: Let TX be daily maximum temperature. Annual count when TX < 0 °C.
Version 1.0, 2021-07-08
"""
# csv input files must have the following format name "[station_number(5 digits)]_TX_d.csv"
for filename in glob.glob("*_TX_d.csv"):
    id0_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            id0 = len(df[df.index.year == y][df < 0].dropna())  # Counting days below 0 Celsius for every year
            id0_lst.append(id0)
        else:
            id0 = float("NaN")
            id0_lst.append(id0)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Year": dates, "ID0 (# of days)": id0_lst})
    df_output.to_csv("id0_" + filename[:5] + ".csv", sep=";", index=False)
