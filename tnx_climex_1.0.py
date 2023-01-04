import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: TNx
Definition: [Max Tmin]. Monthly maximum value of daily minimum temperature.
Version 1.0, 2021-07-08
"""

# csv input files must have the following format name "[station_number(5 digits)]_TN_d.csv"
for filename in glob.glob("*_TN_d.csv"):
    tnx_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over years
        if y in df.index.year:  # Checks if values for given year exist
            for m in range(1, 13):  # Iteration over months
                if m in df[df.index.year == y].index.month:  # Checks if values for given month exist
                    # Calculating max value of specific month and year
                    tnx = df[df.index.year == y][df[df.index.year == y].index.month == m][df.columns[0]].max()
                    tnx_lst.append(tnx)
                else:
                    tnx = float("NaN")
                    tnx_lst.append(tnx)
        else:
            pass

    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="m")  # Date column
    df_output = pd.DataFrame({"Date": dates, "TNx (°C)": tnx_lst})
    df_output.to_csv("tnx_" + filename[:5] + ".csv", sep=";", index=False)
