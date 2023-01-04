import pandas as pd
import glob

"""
Climate indexes as defined by http://etccdi.pacificclimate.org/list_27_indices.shtml
Authors: Ioannidis Panagiotis (panagiwths.ioannidis117@gmail.com), Athanassios Argiriou (athanarg@upatras.gr)
github: ioannidispanagiotis, thanosargiriou
Laboratory of Atmospheric Physics - Department of Physics - University of Patras (https://www.atmosphere-upatras.gr/en)
"""
"""
Climate index: DTR 
Definition: [Daily temperature range]. Monthly mean difference between TX and TN. Let TXij and TNij be the daily maximum
            and minimum temperature respectively on day i in period j. Then: DTR daily = (TXij - TNij)
Version 1.0, 2021-11-23
"""
files_TX = glob.glob("*_TX_d_h.csv")
files_TN = glob.glob("*_TN_d_h.csv")

for filex, filen in zip(files_TX, files_TN):
    # Check if both files have the same stations code
    if filex[-16:-11] == filen[-16:-11]:
        dfx = pd.read_csv(filex, sep=",", index_col=0, parse_dates=True)
        dfn = pd.read_csv(filen, sep=",", index_col=0, parse_dates=True)

        dtrd = dfx - dfn  # Daily dtr calculation
        dtr = dtrd.resample("M").mean()
        dtrd.to_csv("dtr_" + filex[-16:-11] + "_d.csv", sep=";", float_format="%.2f")
