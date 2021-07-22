#!/usr/bin/env python3

import argparse
import socket
import struct
import os
import time
import select
import signal
import sys


def compute_checksum(data):
    checksum = 0
    count = 0
    countTo = len(data) // 2 * 2
    while count < countTo:
        low_byte = data[count]
        high_byte = data[count + 1]
        checksum += (high_byte << 8) | low_byte
        count += 2

    if count + 1 < len(data):
        checksum += data[count + 1]

    checksum = (checksum & 0xffff) + (checksum >> 16)
    checksum += checksum >> 16
    result = ~checksum & 0xffff
    return result


class ICMPError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PingError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PingStats:
    def __init__(self):
        self.rtts = []
        self.transmitted = 0
        self.received = 0

    def compute_rtt_stats(self):
        if len(self.rtts) == 0:
            raise PingError('Not enough data to make a computation')

        rtt_min = 10000000000
        rtt_max = 0
        rtt_sum = 0
        for rtt in self.rtts:
            rtt_min = min(rtt_min, rtt)
            rtt_max = max(rtt_max, rtt)
            rtt_sum += rtt

        return rtt_min, rtt_max, rtt_sum / len(self.rtts)


class Ping:
    def __init__(self, host, timeout, interval):
        self.host = host
        self.timeout = timeout
        self.interval = interval
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.stats = PingStats()
        self.icmp_type_echo = 8
        self.icmp_code_echo = 0

    def create_icmp_echo_message_packet(self, id, seq, data):
        checksum = 0
        icmp_packet = struct.pack('BBHHHd', self.icmp_type_echo, self.icmp_code_echo, checksum, id, seq, data)
        checksum = compute_checksum(icmp_packet)
        icmp_packet = struct.pack('BBHHHd', self.icmp_type_echo, self.icmp_code_echo, checksum, id, seq, data)
        return icmp_packet

    def recv_ping(self, id):
        while True:
            timeStarted = time.time()
            ready = select.select([self.socket], [], [], self.timeout)
            if len(ready[0]) == 0:
                raise PingError('Request timed out')
            timeFinished = time.time()

            if timeFinished - timeStarted > self.timeout:
                raise PingError('Request timed out')

            recvdata, host = self.socket.recvfrom(1024)
            self.stats.received += 1
            type, code, checksum, pid, seq, data = struct.unpack('BBHHHd', recvdata[20:36])
            if type == 0:
                if code == 0 and pid == id:
                    rtt = (time.time() - data) * 1000
                    self.stats.rtts.append(rtt)
                    return host[0], rtt, len(recvdata)
            elif type == 3:
                if code == 0:
                    raise ICMPError('Destination Network Unreachable')
                if code == 1:
                    raise ICMPError('Destination Host Unreachable')

    def send_ping(self):
        id = os.getpid()
        icmp_packet = self.create_icmp_echo_message_packet(id, 1, time.time())
        self.socket.sendto(icmp_packet, (self.host, 1))
        self.stats.transmitted += 1
        return id

    def ping(self):
        id = self.send_ping()
        try:
            host, rtt, length = self.recv_ping(id)
            fqdn = socket.getfqdn(host)
            if fqdn != host:
                print(f'{length} bytes from {fqdn} ({host}): rtt={rtt:.2f} ms')
            else:
                print(f'{length} bytes from {host}: rtt={rtt:.2f} ms')
        except ICMPError as ex:
            print(ex)
            sys.exit(0)
        except PingError as ex:
            print(ex)
        time.sleep(self.interval)

    def print_stats(self):
        print(f'--- {self.host} ping statistics ---')
        packet_loss = (1 - self.stats.received / self.stats.transmitted) * 100
        print(f'{self.stats.transmitted} transmitted, {self.stats.received} received, {packet_loss:.0f}% packet loss')
        try:
            rtt_min, rtt_max, rtt_avg = self.stats.compute_rtt_stats()
            print(f'rtt min/avg/max = {rtt_min:.3f}/{rtt_avg:.3f}/{rtt_max:.3f} ms')
        except PingError as ex:
            print(ex)

    def signal_handler(self, signum, frame):
        self.print_stats()
        sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description="Ping utility")
    parser.add_argument('host', help='host address')
    parser.add_argument('-t', '--timeout', help='time to wait for response, in seconds (4s by default)',
                        type=float, default=4)
    parser.add_argument('-c', '--count', help='number of packets to send', type=int, default=0)
    parser.add_argument('-i', '--interval', help='wait interval seconds between sending each packet (1s by default)',
                        type=float, default=1)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    ping = Ping(args.host, args.timeout, args.interval)
    signal.signal(signal.SIGINT, lambda signum, frame: ping.signal_handler(signum, frame))

    count = args.count
    if count == 0:
        while True:
            ping.ping()
    else:
        for i in range(count):
            ping.ping()

    ping.print_stats()