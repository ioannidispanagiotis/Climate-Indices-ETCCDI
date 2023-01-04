import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: CWD
Definition: [Consecutive wet days]. Let RR be daily precipitation. Maximum number of consecutive days with RR >= 1 mm 
            per year.
Version 1.0, 2021-07-08
"""
# csv input files must have the following format name "[station_number(5 digits)]_rr.csv"
for filename in glob.glob("*_RR_d.csv"):
    cwd_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import

    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            df_year = df[df.index.year == y]
            # Yearly count of consecutive days with daily precipitation >= 1 mm
            cwd_df = df_year[df_year >= 1].dropna()
            # Check if the days are consecutive
            count = 0
            count_lst = []
            for q in range(1, len(cwd_df.index)):
                if (cwd_df.index[q] - cwd_df.index[q-1]).days != 1:
                    count = 0
                else:
                    count = count + 1
                count_lst.append(count)
            if len(count_lst) == 0:  # Added in order to avoid error in finding the max() of an empty list
                pass
            else:
                cwd = max(count_lst) + 1
            cwd_lst.append(cwd)
        else:
            cwd = float("NaN")
            cwd_lst.append(cwd)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Date": dates, "CWD per year (# of days)": cwd_lst})
    df_output.to_csv("CWD_yearly_" + filename[:5] + ".csv", sep=";", index=False)
