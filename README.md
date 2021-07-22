# Ping
Simple Ping implementation in Python

## Usage

```
usage: ping.py [-h] [-t TIMEOUT] [-n NUMBER] host

Ping utility

positional arguments:
  host                  host address

optional arguments:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        time to wait for response, in seconds (4s by default)
  -n NUMBER, --number NUMBER
                        number of packets to send
```

## ping google.com

```
36 bytes from 142.250.150.113: rtt=79.76 ms
36 bytes from 142.250.150.139: rtt=72.20 ms
36 bytes from lo-in-f100.1e100.net (173.194.222.100): rtt=78.61 ms
36 bytes from lo-in-f102.1e100.net (173.194.222.102): rtt=43.18 ms
36 bytes from lo-in-f102.1e100.net (173.194.222.102): rtt=43.45 ms
36 bytes from lo-in-f102.1e100.net (173.194.222.102): rtt=43.07 ms
--- google.com ping statistics ---
6 transmitted, 6 received, 0% packet loss
rtt min/avg/max = 43.070/60.045/79.759 ms
```
