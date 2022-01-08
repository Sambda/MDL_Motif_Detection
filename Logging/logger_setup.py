import logging
import params as p


def init_logger(series, path):
    log = Logger(series, path + 'logger.txt')
    log.set_start_parameter(series)
    return log


class Logger(object):

    def __init__(self, series, filename):
        self.logger = logging.getLogger('DL Logger')
        self.data_number = series.data_number
        self.alphabet_size = series.alphabet_size
        self.power = series.power_transformation
        self.smooth = p.smooth
        self.smooth_degree = p.smooth_fraction
        self.filename = filename

        logging.basicConfig(filename=self.filename, level=logging.INFO, format='%(message)s')
        logging.FileHandler(filename=self.filename, mode="w")

    def set_start_parameter(self, series):
        self.logger.info("LOGGING:"
                         "\nData : {} "
                         "\nAlphabet size: {} "
                         "\nPower Transformation: {}"
                         "\nLength TS: {} "
                         "\nPAA Length TS: {}"
                         "\nDouble Sax: {} "
                         "\nSmooth: {} "
                         "\nSmooth Fraction: {}"
                         "\nFilename: {}"
                         "\nZ-Normalisation: {} "
                         "\nBreakpoint setting Value: {}"
                         "\nKind of breakpoints: {}"
                         "\nWindow size PAA: {},"
                         "\nDL_sax: {}" .format(
                             self.data_number,
                             self.alphabet_size,
                             self.power,
                             len(series.ts),
                             len(series.ts_norm),
                             series.double,
                             p.smooth,
                             p.smooth_fraction,
                             self.filename,
                             p.z_norm,
                             p.quantil,
                             p.kind_of_breakpoints,
                             p.number_to_reduce,
                             series.worst_case))

    def set_calculation_times(self, time_difference):
        sum_time_difference = sum(time_difference.time_list_complete)
        sum_pulp_difference = sum(time_difference.time_list_pulp)
        self.logger.info("Time complete: {} \nTime Pulp:".format
                         (sum_time_difference, sum_pulp_difference))

    def set_worst_case(self, worst_case):
        self.logger.info("\nMDL Worst Case: {}".format(worst_case))

    def set_mdl_values(self, key, value, indexes):
        self.logger.info("MDL for pattern length: {} is: {} with index: {}".format(key, value[1], indexes))

    def set_mdl_values_by_smaller_range(self, len_pattern, mdl, index_list):
        self.logger.info("MDL for k: {} is: {} with index: {}".format(len_pattern, mdl, index_list))

    def set_text(self, text):
        self.logger.info(text)

    def set_best_motifs(self, list_of_motifs):
        self.logger.info("__________ BEST MOTIFS ___________")
        for index, motif in enumerate(list_of_motifs):
            self.logger.info("Motif {}\nLength: {}\nPattern: {}\nIndexes: {}\nMDL: {}\n"
                             .format(index, motif, list_of_motifs[motif]["pattern_list"], list_of_motifs[motif]["indexes"], list_of_motifs[motif]["mdl"]))
