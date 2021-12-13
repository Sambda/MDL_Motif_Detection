from pulp import *


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def get_optimized_list_with_pulp(words, candidate, mdl_deviation, words_numeric, words_numeric_2):
    len_to_check = len(words[0])-1
    words_pulp = []
    for i, w in enumerate(words):
        words_pulp.append(f"{i:09d}" + "_" + w)

    prob = LpProblem("MotifProblem", LpMaximize)

    # Create dicts for conditions
    candidate_dict = dict(zip(words_pulp, candidate))
    mdl_deviation_dict = dict(zip(words_pulp, mdl_deviation))

    frequency_variables = LpVariable.dicts("p", words_pulp, lowBound=0, upBound=1, cat='Binary')

    prob += lpSum([1/(mdl_deviation_dict[j]+0.00000001) * frequency_variables[j] for j in words_pulp])

    # Block indexes behind a found candidate
    for i in range(len(words_pulp) - 1):
        if len(words_pulp) - i - 2 >= len_to_check :
            check_tmp = len_to_check
        else:
            check_tmp = len(words_pulp) - i - 1
        for j in range(check_tmp):
            j = j + 1
            prob += lpSum([frequency_variables[words_pulp[i]] + frequency_variables[words_pulp[i + j]]]) <= 1

    # Condition that only real candidates can be 1
    for key, val in candidate_dict.items():
        if val == 0:
            prob += lpSum([frequency_variables[key]]) == 0

    prob.solve(PULP_CBC_CMD(msg=0))

    pattern_list, pattern_list_numeric, pattern_list_numeric_2,  index_list, mdl_deviation_list = [], [], [], [], []

    for i, v in enumerate(prob.variables()):
        if v.varValue > 0:
            pattern_list.append([words[i]])
            pattern_list_numeric.append([words_numeric[i]])
            pattern_list_numeric_2.append([words_numeric_2[i]])
            index_list.append([i, i + len(words[0])])
            mdl_deviation_list.append(mdl_deviation[i])

    return pattern_list, pattern_list_numeric, pattern_list_numeric_2, index_list, mdl_deviation_list


if __name__ == "__main__":

    candidate = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    mdl_deviation = [1.51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.51, 0, 0, 0, 0, 3.3, 0, 0, 0, 2.1, 0, 0, 0, 0, 0]
    words_list = ['ababb', 'babbb', 'abbbb', 'bbbba', 'bbbaa', 'bbaac', 'baaca', 'aacab', 'acaba', 'cabab', 'ababb', 'babba',
             'abbab', 'bbaba', 'babab', 'ababa', 'babac', 'abaca', 'bacab', 'acabb', 'cabac', 'abacb', 'bacbc', 'acbca',
             'cbcaa']

    position_list, pattern_list, index_list, mdl_deviation_list = get_optimized_list_with_pulp(words_list, candidate,
                                                                                               mdl_deviation)
    print("position_list: {} \npattern: {} \nindexes: {} \nmdl_deviation: {}".format(position_list, pattern_list,
                                                                                     index_list, mdl_deviation_list))
