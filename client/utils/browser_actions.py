import random
from time import sleep


def random_sleep():
    sleep_range_seconds = [1, 2.5]
    sleep_duration = random.uniform(sleep_range_seconds[0], sleep_range_seconds[1])
    sleep(sleep_duration)
