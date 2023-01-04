import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: RX5day
Definition: [Max 5-day precipitation]. Monthly maximum 5-day precipitation in mm.
Version 1.0, 2021-07-09
"""

# csv input files must have the following format name "[station_number(5 digits)]_rr.csv"
for filename in glob.glob("*_RR_d.csv"):
    rx5day_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import

    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            df_year = df[df.index.year == y]
            for m in range(1, 13):
                if m in df_year.index.month:
                    # Monthly maximum consecutive 5 - day precipitation
                    consecutive_5_day_rr = []  # List of sums for specific month
                    q = 0
                    # In order to always check 5 consecutive days
                    while q < df_year[df_year.index.month == m].index.day[-4]:
                        rx5day_m = df_year[df_year.index.month == m][q:q+4].sum()  # Precipitation for 5 - day
                        consecutive_5_day_rr.append(rx5day_m[0])
                        q = q + 1
                    rx5day = max(consecutive_5_day_rr)  # Max value of 5 - day for specific month
                    rx5day_lst.append(round(rx5day, 2))
                else:
                    rx5day = float("NaN")
                    rx5day_lst.append(rx5day)
        else:
            rx5day = float("NaN")
            rx5day_lst.append(rx5day)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="M")  # Date column
    df_output = pd.DataFrame({"Date": dates, "RX5day (mm)": rx5day_lst})
    df_output.to_csv("rx5day_" + filename[:5] + ".csv", sep=";", index=False)
