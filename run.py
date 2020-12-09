
import os
import time
import subprocess

from typing import Optional


def main():
    results = ['???'] * 25
    for i in range(1, 1 + 25):
        result = run_day(i)
        if result:
            results[i - 1] = result

    print('=' * 25)
    for i in range(25):
        print('Day %2d | %s' % (i + 1, results[i]))


def run_day(day: int) -> Optional[str]:
    os.chdir('day%02d' % day)
    try:
        print('Day %2d | Running' % day)
        part1 = part2 = ''
        now = time.time()
        proc = subprocess.Popen('python day%d.py' % day, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            output = proc.stdout.readline().decode('utf-8').replace('\r', '').replace('\n', '')
            if output != '':
                print('Day %2d |' % day, output)
        ret = proc.wait()
        then = time.time()
        delta = format_time(then - now)
        if ret == 0:
            print('Day %2d - Finished' % day)
        else:
            print('Day %2d - Failed with return value %d' % (day, ret))
        return delta
    except:
        return None
    finally:
        os.chdir('../')


def format_time(delta: float) -> str:
    if delta > 1:
        return '%d s' % int(delta)
    elif delta > 0.0001:
        return '%d ms' % int(delta * 1000)
    elif delta > 0.000_0001:
        return '%d us' % int(delta * 1000_000)
    else:
        return '%d ns' % int(delta * 1000_000_000)


if __name__ == '__main__':
    main()
