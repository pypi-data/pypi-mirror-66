from spaceone.core.error import *


class ERROR_DIFF_TIME_RANGE(ERROR_INVALID_ARGUMENT):
    _message = 'There are less than two items in time, so it cannot be compared. (start = {start}, end = {end})'
