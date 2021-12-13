from main import run_main
import params as p

data_list = ["ecg", "coffee", "olive_oil"]
data_list = ["olive_oil"]

alphabet_size_list = [5]
power_transform_list = [False]
differencing_list = [True, False]
smooth_fraction_list = [0.03]
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
                        run_main()
