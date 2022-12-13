#!/bin/bash
import subprocess
import re
import time
import os


def check_ping(target, timeout, size):
    try:
        _ = subprocess.check_output([
            'ping',
            '-M', 'do',
            '-c', '1',
            '-w', str(timeout),
            '-n',
            '-s', str(size),
            target,
        ], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        return False


def main():
    target = os.environ.get("target")

    if not target:
        print("Empty target")
        return

    ipv6_regex = re.compile("((^|:)([0-9a-fA-F]{0,4})){1,8}$")
    ipv4_regex = re.compile("^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")
    host_regex = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)

    if ipv6_regex.match(target) or ipv4_regex.match(target):
        pass
    elif len(target) > 255 or not all(host_regex.match(part) for part in target.split(".")):
        print("Target is not valid")
        return
    elif not check_ping(target, 2, 0):
        print("Target unreachable")
        return

    # binary search
    l = 0
    r = 20000  # in case we have jumbos
    while l < r - 1:
        m = (l + r) // 2
        if check_ping(target, 2, m):
            l = m
        else:
            r = m
        time.sleep(0.1)  # to prevent too many pings

    print(f"PMTU to {target} = {l + 28} bytes")


if __name__ == '__main__':
    main()