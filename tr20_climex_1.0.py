import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: TR20
Definition: [Number of tropical nights]. Let TN be daily maximum temperature. Annual count of days when TN > 20°C.
Version 1.0, 2021-07-08
"""

# csv input files must have the following format name "[station_number(5 digits)]_TN_d.csv"
for filename in glob.glob("*_TN_d.csv"):
    tr20_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            tr20 = len(df[df.index.year == y][df > 20].dropna())  # Counting days above 20 Celsius for every year
            tr20_lst.append(tr20)
        else:
            tr20 = float("NaN")
            tr20_lst.append(tr20)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Year": dates, "TR20 (# of days)": tr20_lst})
    df_output.to_csv("tr20_" + filename[:5] + ".csv", sep=";", index=False)
