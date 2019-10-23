import download_data_high_frequency
import download_data_low_frequency
import multiprocessing
import utils_log
import logging


if __name__ == '__main__':
    utils_log.setLevel(logging.DEBUG)
    proc_high = multiprocessing.Process(
        target=download_data_high_frequency.download_loop)
    proc_low = multiprocessing.Process(
        target=download_data_low_frequency.download_loop)

    proc_high.start()
    proc_low.start()

    proc_high.join()
    proc_low.join()

    pass
