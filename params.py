# _______________________ DATA SET _____________________
ts_number = "coffee"  #coffee, olive_oil, ecg, sinus, traveled_miles, StandWalkJump, Ethanol
alphabet_size = 7

# _____________________ PREPROCESSING _______________________

# Power Transformation
power_transformation = False

# PAA
number_to_reduce = 15
reduce_ts_with_max_series_length = False
max_series_length = 600
paa = True

# Smoothing
smooth = True
smooth_fraction = 0.01

# Differencing
differencing = True

# Z Normalisation
z_norm = True


# ________________________ SEARCH _______________________
kind_of_search = "fs"  # hs, fs


# ____________________ SAX PARAMETER _______________________

double_sax = True
kind_of_breakpoints = "density"  # statistical, linear, density
# For density
quantil = 0.8
# Kind of double sax
three_double_sax = False
# doule val # 2 not possible because mono. decreasing for kind of binning, only if three_double_sax is true
threshold_double = 2.5


# ______________ HIERACHICHAL SEARCH _______________________
search_again_in_neighborhood = True
search_again_for_best_ks = True


# ___________________ RUNTIME _______________________________
steps_to_overjump = 1


# ____________________DL ENCODING _______________________


# _________________ NEW TGS ____________________________
check_if_other_center_would_be_better = True

# ________________ SAVE RESULT PLOTS -------------------
save = True

# _______________ PLOT RUNTIME AND TSS AMOUNT DICT VALUES ______
plot_dict_values = True
