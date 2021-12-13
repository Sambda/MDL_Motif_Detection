# _______________________ DATA SET _____________________
ts_number = "ecg"  #coffee, olive_oil, ecg, sinus, traveled_miles
alphabet_size = 6

# _____________________ PREPROCESSING _______________________

# Power Transformation
power_transformation = False

# PAA
number_to_reduce = 10
reduce_ts_with_max_series_length = True
max_series_length = 100
paa = True

# Smoothing
smooth_fraction = 0.01

# Differencing
differencing = False

# Z Normalisation
z_norm = False


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
search_again_in_neighborhood = False
search_again_for_best_ks = True


# ___________________ RUNTIME _______________________________
steps_to_overjump = 3


# ____________________DL ENCODING _______________________


# _________________ NEW TGS _________________-
check_if_other_center_would_be_better = True
