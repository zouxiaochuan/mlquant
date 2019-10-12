import uuid
import json
import datetime
import numpy as np
from collections import deque
import pytz


def get_temp_name(prefix='temp'):
    return prefix + '_' + str(uuid.uuid4()).replace('-', '_')


def file2list(filename):
    ret = []
    with open(filename) as fin:
        for line in fin:
            ret.append(line.strip())
            pass
        pass
    return ret


def load_json(filename):
    with open(filename) as fin:
        s = fin.read()
        pass

    return json.loads(s)


def dt_add(dt, days):
    return datetime.datetime.strftime(
        datetime.datetime.strptime(dt, '%Y-%m-%d') +
        datetime.timedelta(days=days), '%Y-%m-%d')


def date2dt(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d')


def dt2ms(dt):
    date = datetime.datetime.strptime(dt, '%Y-%m-%d')
    return int(date.timestamp() * 1000)


def dt_diff(dt1, dt2):
    date1 = datetime.datetime.strptime(dt1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(dt2, '%Y-%m-%d')
    return (date1-date2).days


def get_current_dt_us():
    return datetime.datetime.strftime(datetime.datetime.now().astimezone(
        pytz.timezone('US/Eastern')), '%Y-%m-%d')


def get_current_dt():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')


def min_sum_sublist(alist):
    best = cur = 0
    for v in alist:
        cur = min(cur + v, 0)
        best = min(best, cur)
        pass
    return best


def max_sum_sublist(alist):
    best = cur = 0
    for v in alist:
        cur = max(cur + v, 0)
        best = max(best, cur)
        pass
    return best


def slide_window_max(values, windowSize):
    q = deque()

    ret = []
    for i in range(len(values)):
        while len(q) > 0 and values[i] > values[q[-1]]:
            q.pop()
            pass
        q.append(i)
        if q[0] <= (i-windowSize):
            q.popleft()
            pass

        ret.append(values[q[0]])
        pass

    return ret


def slide_window_min(values, windowSize):
    values = [-i for i in values]
    ret = slide_window_max(values, windowSize)
    ret = [-i for i in ret]
    return ret


def slide_window_mean(values, windowSize):
    vsum = 0.0
    vnum = 0
    ret = []

    for i in range(len(values)):
        if i >= windowSize:
            vsum -= values[i-windowSize]
            vnum -= 1
            pass
        vsum += values[i]
        vnum += 1

        ret.append(vsum/vnum)
        pass

    return ret


def sharp_ratio(returns, noRiskReturn):
    if len(returns) <= 1:
        return 0.0
    std = np.std(returns)
    return (returns[-1]-noRiskReturn*len(returns))/std


def max_draw_down(returns):
    xs = returns
    i = np.argmax((np.maximum.accumulate(xs) - xs)/xs)  # end of the period
    if i == 0:
        return 0
    j = np.argmax(xs[:i])  # start of period

    return (returns[i]-returns[j])/returns[j]


def max_continous(vals, check_func):
    max_len = 0

    current_len = 0
    for v in vals:
        if check_func(v):
            current_len += 1
        else:
            current_len = 0
            pass
        max_len = max(current_len, max_len)
        pass
    return max_len


def slide_window_max_continuous(vals, window_size, check_func):
    ret = []

    for i in range(len(vals)):
        end = i+1
        start = end-window_size
        if start < 0:
            start = 0
            pass
        ret.append(max_continous(vals[start:end], check_func))
        pass
    return ret
    pass
