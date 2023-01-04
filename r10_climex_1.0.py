import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: R10
Definition: [Number of heavy precipitation days]. Let PR be daily precipitation in mm.
            Annual count of days when PR >= 10 mm.
Version 1.0, 2021-07-08
"""
# csv input files must have the following format name "[station_number(5 digits)]_rr.csv"
for filename in glob.glob("*_RR_d.csv"):
    r10_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            # Counting days of precipitation greater than or equal to 10 mm
            r10 = len(df[df.index.year == y][df >= 10].dropna())
            r10_lst.append(r10)
        else:
            r10 = float("NaN")
            r10_lst.append(r10)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Year": dates, "R10 (# of days)": r10_lst})
    df_output.to_csv("r10_" + filename[:5] + ".csv", sep=";", index=False)
