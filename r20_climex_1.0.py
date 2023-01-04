import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: R20
Definition: [Number of very heavy precipitation days]. Let PR be daily precipitation in mm.
            Annual count of days when PR >= 20 mm.
Version 1.0, 2021-07-08
"""
# csv input files must have the following format name "[station_number(5 digits)]_rr.csv"
for filename in glob.glob("*_RR_d.csv"):
    r20_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            # Counting days of precipitation greater than or equal to 10 mm
            r20 = len(df[df.index.year == y][df >= 20].dropna())
            r20_lst.append(r20)
        else:
            r20 = float("NaN")
            r20_lst.append(r20)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Year": dates, "R20 (# of days)": r20_lst})
    df_output.to_csv("r20_" + filename[:5] + ".csv", sep=";", index=False)
