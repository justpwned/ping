# Ping
Simple ping implementation in Python

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

## Sample output

**```sudo ./ping.py google.com -c 6```**
````
36 bytes from lo-in-f100.1e100.net (173.194.222.100): icmp_seq=1 ttl=58 rtt=42.61 ms
36 bytes from lo-in-f100.1e100.net (173.194.222.100): icmp_seq=2 ttl=58 rtt=42.11 ms
36 bytes from lo-in-f100.1e100.net (173.194.222.100): icmp_seq=3 ttl=58 rtt=42.12 ms
36 bytes from lo-in-f100.1e100.net (173.194.222.100): icmp_seq=4 ttl=58 rtt=42.17 ms
36 bytes from lo-in-f100.1e100.net (173.194.222.100): icmp_seq=5 ttl=58 rtt=42.11 ms
36 bytes from lo-in-f100.1e100.net (173.194.222.100): icmp_seq=6 ttl=58 rtt=42.20 ms
--- google.com ping statistics ---
6 transmitted, 6 received, 0% packet loss
rtt min/avg/max = 42.107/42.221/42.612 ms
```
