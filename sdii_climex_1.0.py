import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: PRCPTOT
Definition: [Simple daily intensity index]. Let RR be daily precipitation. Annual total precipitation divided by the
            number of wet days in the year. A wet day is considered when RR >= 1mm.
Version 1.0, 2021-07-08
"""

# csv input files must have the following format name "[station_number(5 digits)]_rr.csv"
for filename in glob.glob("*_RR_d.csv"):
    sdii_lst = []  # List to save index values per year
    df = pd.read_csv(filename, index_col=[0], parse_dates=True)  # Data import

    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over every year
        if y in df.index.year:  # Checks if values for given year exist
            df_year = df[df.index.year == y]
            wet_days_df = df_year[df_year >= 1].dropna()  # Days with daily precipitation >= 1 mm
            annual_precip = wet_days_df[wet_days_df.columns[0]].sum()  # Calculates the sum of precipitation in wet days
            wet_days = len(df_year[df_year >= 1].dropna())  # Number of days with daily precipitation >= 1 mm
            sdii = annual_precip / wet_days
            sdii_lst.append(round(sdii, 2))
        else:
            sdii = float("NaN")
            sdii_lst.append(sdii)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Date": dates, "SDII (mm/day)": sdii_lst})
    df_output.to_csv("sdii_" + filename[:5] + ".csv", sep=";", index=False)
