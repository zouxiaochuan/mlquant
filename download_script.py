import download_data_high_frequency
import download_data_low_frequency
import multiprocessing
import utils_log
import logging
import time


if __name__ == '__main__':
    utils_log.setLevel(logging.DEBUG)
    logger = utils_log.console

    proc_high = None
    proc_low = None

    while True:
        if proc_high is None or not proc_high.is_alive():
            logger.info('restart proc_high')
            proc_high = multiprocessing.Process(
                target=download_data_high_frequency.download_loop)
            proc_high.start()
            pass
        if proc_low is None or not proc_low.is_alive():
            logger.info('restart proc_low')
            proc_low = multiprocessing.Process(
                target=download_data_low_frequency.download_loop)
            proc_low.start()
            pass

        time.sleep(30)
        pass

    pass
