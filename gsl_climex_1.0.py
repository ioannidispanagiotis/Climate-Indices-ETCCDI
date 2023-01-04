import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: GSL
Definition: [Growing season length]: Annual (1st Jan to 31st Dec in North Hemisphere) count between first span of at
            least 6 days with TG>5°C and first span after July 1st of 6 days with TG<5°C.
Version 1.0, 2021-07-09
"""
# csv input files must have the following format name "[station_number(5 digits)]_TG_d.csv"
for filename in glob.glob("*_TG_d.csv"):
    df = pd.read_csv(filename, index_col=[0], sep=",", parse_dates=True)  # Data import
    gsl_lst = []
    for y in range(df.index.year[0], df.index.year[-1] + 1):  # Iteration over years
        df_year = df[df.index.year == y]
        if y in df.index.year:  # Checks if values for given year exist
            tg_bigger = df_year[df_year > 5].dropna()  # Find days with TG > 5°C from 1st of January
            df_july = df_year[df_year.index.month >= 7]  # 7 for July
            tg_smaller = df_july[df_july < 5].dropna()  # Find days with TG < 5°C from 1st of January
            if len(tg_bigger) < 6:  # Check in case i have zero days that satisfy my conditional
                gsl = float("NaN")
                gsl_lst.append(gsl)
            else:
                count1 = 0  # Check if the days are consecutive
                for q in range(1, len(tg_bigger.index)):
                    if (tg_bigger.index[q] - tg_bigger.index[q - 1]).days != 1 and count1 < 6:
                        count1 = 0
                    elif count1 < 6:
                        count1 = count1 + 1
                    else:  # If we find 6 consecutive days we stop the loop
                        break
                # minus 2, - 1 because of python index numbering and - 1 because q starts from 2nd day in dataframe
                jan_span = tg_bigger.index[q - 2]  # Last day of first span
            # Find days with TG < 5°C from 1st of July
            if len(tg_smaller) < 6:  # Check in case i have zero days that satisfy my conditional
                gsl = float("NaN")
                gsl_lst.append(gsl)
            else:
                count2 = 0  # Check if the days are consecutive
                for w in range(1, len(tg_smaller.index)):
                    if (tg_smaller.index[w] - tg_smaller.index[w - 1]).days != 1 and count2 < 6:
                        count2 = 0
                    elif count2 < 6:
                        count2 = count2 + 1
                    else:
                        break
                # minus 2, - 1 because of python index numbering and - 1 because w starts from 2nd day in dataframe
                july_span = tg_smaller.index[w - 2]  # Last day of first span
                gsl = (july_span - jan_span).days  # Annual count of days between two spans
                gsl_lst.append(gsl)
        else:
            gsl = float("NaN")
            gsl_lst.append(gsl)
    # Dataframe to save files
    dates = pd.date_range(start=str(df.index.year[0]), end=str(df.index.year[-1] + 1), freq="Y")  # Date column
    df_output = pd.DataFrame({"Date": dates, "GSL (# of days)": gsl_lst})
    df_output.to_csv("GSL_" + filename[:5] + ".csv", sep=";", index=False)
