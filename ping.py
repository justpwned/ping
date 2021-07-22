#!/usr/bin/env python3

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Ping utility")
    parser.add_argument('host', help='host address')
    parser.add_argument('-t', '--timeout', help='time to wait for response, in ms (4000 ms by default)', default=4000)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
