import numpy as np
import math
import params as p


# Calculate L0/ log*
def log_star(integer):
    cost = 0
    if int(integer) != 0:
        last_interim_result = np.log2(int(integer))
        while last_interim_result > 0:
            cost += last_interim_result
            last_interim_result = np.log2(last_interim_result)
    const = np.log2(2.865064)
    return round(cost + const, 2)


# c * log2(n)
def log_2(c, n):
    x = c * math.log2(n)
    return round(x,2)


# calc the array between two strings: abc,abb,abb -> [0,0,1] | aab,cbb,cbb -> [2,1,0]
def get_difference_array_double(s_1, s_2, s_3, s_4):
    difference_between_string = []
    for s1, s2, s3, s4 in zip(s_1, s_2, s_3, s_4):
        diff_1 = abs(int(s3) - int(s1))
        diff_2 = abs(int(s4) - int(s1))
        diff_3 = abs(int(s3) - int(s2))
        diff_4 = abs(int(s4) - int(s2))
        min_value = min(diff_1, diff_2, diff_3, diff_4)
        difference_between_string.append(min_value)
    return difference_between_string


# Calculate the sum of costs per element in the distance array
def get_logs_for_change_costs(distance):
    distance_cost = 0
    for i in distance:
        if i != 0:
            distance_cost = distance_cost + -1 * log_2(1, 0.5**i) + 1
    return distance_cost


# Get MDL values for the distance Arrays od two pattern
def calc_mdl_for_distance_array(sum_of_position_of_changes, k, difference_array):
    sum_of_differences = log_star(sum_of_position_of_changes)
    location_of_differences = log_2(sum_of_position_of_changes, k)
    distance_cost = get_logs_for_change_costs(difference_array)

    mdl_deviation_sum = sum_of_differences + location_of_differences + distance_cost  # + alphabet_size_mdl_cost
    return mdl_deviation_sum