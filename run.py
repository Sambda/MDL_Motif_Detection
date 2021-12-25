from main import run_main
import params as p

data_list = ["ecg", "coffee", "olive"]
data_list = ["ecg", "ecg5D"]
data_list = ['olive']
dict_number_to_reduce = {"ecg": 6, "coffee": 6, "olive": 13, "traveled_miles": 1, "beer": 1, "ecg5D": 4, "faces": 5}

alphabet_size_list = [5]
power_transform_list = [False]
differencing_list = [True, False]
smooth_fraction_list = [0.01]
z_norm_list = [True]

for data in data_list:
    for alphabet_size in alphabet_size_list:
        for differencing in differencing_list:
            for smooth_fraction in smooth_fraction_list:
                for power_transform in power_transform_list:
                    for z_norm in z_norm_list:
                        p.ts_number = data
                        p.alphabet_size = alphabet_size
                        p.differencing = differencing
                        p.smooth_fraction = smooth_fraction
                        p.power_transformation = power_transform
                        p.z_norm = z_norm
                        p.number_to_reduce = dict_number_to_reduce[data]
                        print("DATA:", data)
                        run_main(data)
