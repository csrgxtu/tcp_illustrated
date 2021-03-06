"""Demonstrates how to construct and send raw Ethernet packets on the
network.

You probably need root privs to be able to bind to the network interface,
e.g.:

    $ sudo python sendeth.py
"""

from socket import *

def sendeth(src, dst, eth_type, payload, interface = "ens33"):
  """Send raw Ethernet packet on interface."""

  assert(len(src) == len(dst) == 6) # 48-bit ethernet addresses
  assert(len(eth_type) == 2) # 16-bit ethernet type

  s = socket(AF_PACKET, SOCK_RAW)

  # From the docs: "For raw packet
  # sockets the address is a tuple (ifname, proto [,pkttype [,hatype]])"
  s.bind((interface, 0))
  return s.send(src + dst + eth_type + payload)

if __name__ == "__main__":
  print("Sent %d-byte Ethernet packet on eth0" %
    sendeth("\x00\x0c\x29\x63\xf6\xc6",
            "\x00\x0c\x29\x4b\xd5\xcb",
            "\x7A\x05",
            "hello"))