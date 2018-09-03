#!/usr/bin/env python

from scapy.all import IP, TCP, sr1, send


src_ip = '127.0.0.1'
src_port = 59333
dst_ip = '127.0.0.1'
dst_port = 5000

# IP header
ip_header = IP(dst=dst_ip, src=src_ip)

# syn
syn = TCP(dport=dst_port, sport=src_port, ack=1000, flags='S')
# send syn
response = sr1(ip_header/syn)


# ack
ack = TCP(
    dport=dst_port,
    sport=src_port,
    ack=response.seq + 1,
    seq=response.ack + 1,
    flags='A'
)
# reply with ack
send(ip_header/ack)

print 'connection established: ....'
