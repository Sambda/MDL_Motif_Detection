from main import run_main
import params as p

#data_list = ["ecg", "coffee", "olive"]
data_list = ["olive", "coffee"]# "ecg", "traveled_miles",
datanames = ["Traveled miles per month", "Olive Spectroscopy", "Coffee Spectroscopy"] #"ECH Heart Rate",
x_y_axis = [["months", "millions of miles"], ["wave number [1/cm]","arbitrary absorbance"], ["wave number [1/cm]","arbitrary absorbance"], ["sample points", "micro volts"]]
#data_list = ["coffee", "olive", "ecg", "traveled_miles"]
data_list = ["ecg"]
dict_number_to_reduce = {"ethanol": 100, "ecg": 6, "coffee": 21, "olive": 25, "traveled_miles": 2, "beer": 1, "ecg5D": 4, "faces": 2, "eyes": 65, "random": 3, "eyes_pca": 1, "Stand": 13}
dict_names = {"ecg": ["ECH Heart Rate","sample points", "micro volts"], "coffee": ["Coffee spectrograph","wave number [1/cm]","arbitrary absorbance"],  "olive": ["Olive oli spectrograph","wave number [1/cm]","arbitrary absorbance"], "traveled_miles": ["Traveled miles per month","months", "millions of miles"]}
alphabet_size_list = [5]
power_transform_list = [False]
differencing_list = [False]
smooth_fraction_list = [0.1]
z_norm_list = [False]
for da in data_list:
    for alphabet_size in alphabet_size_list:
        for differencing in differencing_list:
            if da == "traveled_miles" and differencing is False:
                pass
            else:
                for smooth_fraction in smooth_fraction_list:
                    for power_transform in power_transform_list:
                        for z_norm in z_norm_list:
                            p.ts_number = da
                            p.alphabet_size = alphabet_size
                            p.differencing = differencing
                            p.smooth_fraction = smooth_fraction
                            p.power_transformation = power_transform
                            p.z_norm = z_norm
                            p.data_name = dict_names[da][0]
                            p.x_axis = dict_names[da][1]
                            p.y_axis = dict_names[da][2]
                            p.number_to_reduce = dict_number_to_reduce[da]
                            print("DATA:", da)
                            run_main()
