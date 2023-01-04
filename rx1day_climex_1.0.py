import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: RX1day
Definition: [Max 1-day precipitation]. Monthly maximum 1-day precipitation in mm.
Version 1.0, 2021-07-08
"""

# csv input files must have the following format name "[station_number(5 digits)]_rr.csv"
for filename in glob.glob("*_RR_d.csv"):
    rx1day_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import

    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            df_year = df[df.index.year == y]
            for m in range(1, 13):
                if m in df_year.index.month:
                    # Monthly 1 -day maximum precipitation
                    rx1day = df_year[df_year.index.month == m].max()
                    rx1day_lst.append(rx1day[0])
                else:
                    rx1day = float("NaN")
                    rx1day_lst.append(rx1day)
        else:
            rx1day = float("NaN")
            rx1day_lst.append(rx1day)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="M")  # Date column
    df_output = pd.DataFrame({"Date": dates, "RX1day (mm)": rx1day_lst})
    df_output.to_csv("rx1day_" + filename[:5] + ".csv", sep=";", index=False)
