import pandas as pd
import numpy as np
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: TN90p
Definition: [Percentage of days when TN > 90th percentile] Let TNij be the daily maximum temperature on day i
            in period j and let TNin90 be the calendar day 90th percentile centred on a 5-day window
            for the base period 1961-1990. The percentage of time for the base period is determined where:
                                               TNij > TNin90
            To avoid possible inhomogeneity across the in-base and out-base periods, the calculation
            for the base period (1961-1990) requires the use of a bootstrap procedure. 
            Details are described in Zhang et al. (2005) .
Version 1.0, 2021-07-17
"""


def leap_year(year):
    if (year % 4) != 0:
        return "False"
    elif (year % 100) != 0:
        return "True"
    elif (year % 400) != 0:
        return "False"
    else:
        return "True"


base_start = 1961  # First year of base period
base_end = 1990  # Last year of base period

# csv input files must have the following format name "[station_number(5 digits)]_TN_d.csv"
for filename in glob.glob("*_TN_d.csv"):
    df = pd.read_csv(filename, sep=",", index_col=[0], parse_dates=True)  # Data import
    df = df.dropna()
    df_base_period = df[(df.index.year >= base_start) & (df.index.year <= base_end)]  # Data for base period
    tn90p = []  # List to append calculated percentile
    variable = filename[:5]  # Variable under calculation

    # Not in base period percentile calculation
    for m in range(1, 13):  # Iteration over months
        df_month = df_base_period[df_base_period.index.month == m]  # Data for specific month

        for d in range(1, 32):  # Iteration over days
            df_centered = pd.DataFrame()  # Dataframe reset
            df_to_add = pd.DataFrame()  # Dataframe reset
            if d not in df_month.index.day:  # Needed in order to avoid index errors caused by values that do not exist
                pass  # for months without day 30 or 31 days
            else:
                df_day = df_month[df_month.index.day == d]  # Data for specific day
                d1 = (pd.Timestamp(df_day.index[0]) - pd.DateOffset(days=2))  # Selecting date 2 days before given day d
                d2 = (pd.Timestamp(df_day.index[0]) + pd.DateOffset(days=2))  # Selecting date 2 days after given day d
                # Dataframe with 5 values centered on given day d
                df_centered = df_base_period[(df_base_period.index <= d2) & (df_base_period.index >= d1)]

                if m == 2 and d == 29:  # loop for leap years
                    t = df_centered.index.year[0]  # First leap year of under study data
                    while t < 1990:
                        t = t + 4  # In order to iterate over leap years
                        # Replacing year of 2 days before given day d in order to move to next year's values
                        d1 = d1.replace(t)
                        d2 = d1 + pd.DateOffset(days=4)  # Adding 4 days to d1 in order to have the 2 days after d
                        # The following dataframe selects values for specific 5 consecutive days, with day d as centered
                        df_to_add = df_base_period[(df_base_period.index <= d2) & (df_base_period.index >= d1)]
                        # Appending values to a dataframe for percentile calculation
                        df_centered = df_centered.append(df_to_add)

                elif m == 12 and d in [30, 31]:  # Loop for centered days 30/12 and 31/12 that need different iteration
                    # The procedure is the same as past loop
                    for w in range(df_base_period.index.year.unique()[0] + 1, df_base_period.index.year.unique()[-1] + 1):
                        d1 = d1.replace(w)
                        d2 = d1 + pd.DateOffset(days=4)
                        df_to_add = df_base_period[(df_base_period.index <= d2) & (df_base_period.index >= d1)]
                        df_centered = df_centered.append(df_to_add)

                elif m == 1 and d in [1, 2]:
                    for y in range(df_base_period.index.year.unique()[0], df_base_period.index.year.unique()[-1]):
                        d1 = d1.replace(y)
                        d2 = d1 + pd.DateOffset(days=4)
                        df_to_add = df_base_period[(df_base_period.index <= d2) & (df_base_period.index >= d1)]
                        df_centered = df_centered.append(df_to_add)

                else:  # Loop for remaining cases with corresponding procedure
                    for y in range(df_base_period.index.year.unique()[0], df_base_period.index.year.unique()[-1]):
                        d1 = d1.replace(y)
                        d2 = d1 + pd.DateOffset(days=4)
                        df_to_add = df_base_period[(df_base_period.index <= d2) & (df_base_period.index >= d1)]
                        df_centered = df_centered.append(df_to_add)

                percentile = df_centered.quantile(q=0.9)  # Calculation of percentile for each day
                tn90p.append(percentile[0])  # Adding calculated percentile to corresponding list

    # Index calculation for out of base period data
    df_not_in_base = pd.concat([df[df.index.year < base_start], df[df.index.year > base_end]])  # Data out of base period
    tn_lst_final = []  # list to append calculated indexes
    dates = []
    year_lst = list(df_not_in_base.index.year.unique())

    for i in year_lst:
        df_not_in_base_y = df_not_in_base[df_not_in_base.index.year == i]

        if leap_year(i) == "True":
            count = 0
            for check_day in range(len(df_not_in_base_y.index)):  # Iteration over year dataframe
                doy = df_not_in_base_y.index[check_day].dayofyear  # Day of the year starting 1 to 365-366
                # -1 because python numbering starts from 0
                if df_not_in_base_y[df_not_in_base_y.index.dayofyear == doy][variable][0] > tn90p[doy - 1]:
                    count = count + 1
                else:
                    pass
        else:
            count = 0
            tn90p_not_leap = tn90p[:59] + tn90p[60:]
            for check_day in range(len(df_not_in_base_y.index)):  # Iteration over year dataframe
                doy = df_not_in_base_y.index[check_day].dayofyear  # Day of the year starting 1 to 165-366
                # -1 because python numbering starts from 0
                if df_not_in_base_y[df_not_in_base_y.index.dayofyear == doy][variable][0] > tn90p_not_leap[doy - 1]:
                    count = count + 1
                else:
                    pass

        count = (count / len(df_not_in_base_y.index)) * 100
        tn_lst_final.append(count)
        dates.append(df_not_in_base_y.index.year[0])

    # Dataframe with index values for out of base period data
    df_output_out_of_base = pd.DataFrame({"Date": dates, "tn90p (% of days)": tn_lst_final})

    # Base period percentile calculation - Bootstrap method
    base_year_lst = []  # List to append years
    index_base_list = []  # List to append calculated final indexes of base period years

    for o in range(df_base_period.index.year[0], df_base_period.index.year[-1] + 1):  # Iteration over base period years
        print(f"out of base year {o}")
        df_boot = df_base_period[df_base_period.index.year != o]  # Removes index calculation year
        index_lst = []  # List to append calculated indexes for a year and then use to it to get the mean value
        iter_years = list(df_boot.index.year.unique())
        for p in iter_years:  # Iteration over 29 remaining base period years
            df_bootstrap = pd.concat([df_boot[df_boot.index.year == p], df_boot])  # Adds year to complete 30 - year period
            df_bootstrap = df_bootstrap.sort_index()
            tn90p_bootstrap = []  # List to append calculated percentile

            for m in range(1, 13):  # Iteration over months
                df_m = df_bootstrap[df_bootstrap.index.month == m]  # Data for specific month

                for d in range(1, 32):  # Iteration over days
                    df_c = pd.DataFrame()  # Dataframe reset
                    df_add = pd.DataFrame()  # Dataframe reset
                    # Conditional needed in order to avoid index errors caused by values that do not exist for months
                    # without day 30 or 31 days
                    if d not in df_m.index.day:
                        pass
                    else:
                        df_d = df_m[df_m.index.day == d]  # Data for specific day
                        # Selecting date 2 days before given day d
                        d1 = (pd.Timestamp(df_d.index[0]) - pd.DateOffset(days=2))
                        # Selecting date 2 days after given day d
                        d2 = (pd.Timestamp(df_d.index[0]) + pd.DateOffset(days=2))
                        # Dataframe with 5 values centered on given day d
                        df_c = df_bootstrap[(df_bootstrap.index <= d2) & (df_bootstrap.index >= d1)]

                        if m == 2 and d == 29:  # loop for leap years
                            t = df_c.index.year[0]  # First leap year of under study data
                            while t < 1990:
                                t = t + 4  # In order to iterate over leap years
                                # Replacing year of 2 days before given day d in order to move to next year's values
                                d1 = d1.replace(t)
                                d2 = d1 + pd.DateOffset(days=4)  # Adding 4 days to d1 in order to have the 2 days after d
                                # Dataframe selects values for specific 5 consecutive days, with day d as centered
                                df_add = df_bootstrap[(df_bootstrap.index <= d2) & (df_bootstrap.index >= d1)]
                                # Appending values to a dataframe for percentile calculation
                                df_c = df_c.append(df_add)
                        # Loop for centered days 30/12 and 31/12 that need different iteration
                        elif m == 12 and d in [30, 31]:
                            # The procedure is the same as past loop
                            for w in iter_years:
                                d1 = d1.replace(w)
                                d2 = d1 + pd.DateOffset(days=4)
                                df_add = df_bootstrap[(df_bootstrap.index <= d2) & (df_bootstrap.index >= d1)]
                                df_c = df_c.append(df_add)

                        elif m == 1 and d in [1, 2]:
                            for y in range(df_base_period.index.year.unique()[0],
                                           df_base_period.index.year.unique()[-1]):
                                d1 = d1.replace(y)
                                d2 = d1 + pd.DateOffset(days=4)
                                df_add = df_bootstrap[(df_bootstrap.index <= d2) & (df_bootstrap.index >= d1)]
                                df_c = df_c.append(df_add)

                        else:  # Loop for remaining cases with corresponding procedure
                            for y in iter_years:
                                d1 = d1.replace(y)
                                d2 = d1 + pd.DateOffset(days=4)
                                df_add = df_bootstrap[(df_bootstrap.index <= d2) & (df_bootstrap.index >= d1)]
                                df_c = df_c.append(df_add)

                        percentile = df_c.quantile(q=0.9)  # Calculation of percentile for each day
                        tn90p_bootstrap.append(percentile[0])  # Adding calculated percentile to corresponding list

            # Dataframe of the year to calculate the index
            df_bootstrap_one_year = df_base_period[df_base_period.index.year == o]

            if leap_year(o) == "True":
                counter = 0
                for check in range(len(df_bootstrap_one_year.index)):  # Iteration over year dataframe
                    day = df_bootstrap_one_year.index[check].dayofyear  # Day of the year starting 1 to 365-366
                    # -1 because python numbering starts from 0
                    if df_bootstrap_one_year[df_bootstrap_one_year.index.dayofyear == day][variable][0] > \
                            tn90p_bootstrap[day - 1]:
                        counter = counter + 1
                    else:
                        pass
            else:
                counter = 0
                tn90p_no_leap = tn90p_bootstrap[:59] + tn90p_bootstrap[60:]
                for check in range(len(df_bootstrap_one_year.index)):  # Iteration over year dataframe
                    day = df_bootstrap_one_year.index[check].dayofyear  # Day of the year starting 1 to 165-366
                    # -1 because python numbering starts from 0
                    if df_bootstrap_one_year[df_bootstrap_one_year.index.dayofyear == day][variable][0] > \
                            tn90p_no_leap[day - 1]:
                        counter = counter + 1
                    else:
                        pass

            counter = (counter / len(df_bootstrap_one_year.index)) * 100  # Calculating percent
            index_lst.append(counter)

        base_year_lst.append(o)  # Appends years
        index_base_list.append(np.mean(index_lst))  # Averages over one year and calculates index

    # Dataframe with index values for base period data
    df_output_base_period = pd.DataFrame({"Date": base_year_lst, "tn90p (% of days)": index_base_list})

    # Joins out of base and in base period indexes dataframes
    df_output = pd.concat([df_output_base_period, df_output_out_of_base]).sort_values(by="Date")
    df_output.to_csv("tn90p_" + filename[:5] + ".csv", sep=";", index=False, float_format="%.2f")
