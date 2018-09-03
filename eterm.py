### Ethernet packet sender/receiver (for Linux raw socket) ###
#
# Public domain software
#
# Coded by Yasusi Kanada
# 2014-7-29

import optparse, socket, time, binascii

BUF_SIZE = 1600		# > 1500

ETH_P_ALL = 3		# To receive all Ethernet protocols

# Interface = "eth0"
Interface = "ens33"

# host = socket.gethostbyname(socket.gethostname())


### Packet field access ###

def SMAC(packet):
   return binascii.hexlify(packet[6:12]).decode()

def DMAC(packet):
   return binascii.hexlify(packet[0:6]).decode()

def EtherType(packet):
   return binascii.hexlify(packet[12:14]).decode()

def Payload(packet):
   return binascii.hexlify(packet[14:]).decode()



### Packet handler ###

def printPacket(packet, now, message):
   # print(message, len(packet), "bytes  time:", now,
   #       "\n  SMAC:", SMAC(packet), " DMAC:", DMAC(packet),
   #       " Type:", EtherType(packet), "\n  Payload:", Payload(packet)) # !! Python 3 !!
   print message, len(packet), "bytes time:", now, \
       "\n  SMAC:", SMAC(packet), " DMAC:", DMAC(packet), " Type:", \
       EtherType(packet), "\n  Payload:", Payload(packet) # !! Python 2 !!


def terminal():
   # Parse command line
   parser = optparse.OptionParser()
   parser.add_option("--p", "--port", dest = "port", type="int",
                     help = "Local network port id")
   parser.add_option("--lm", "--lmac", "--localMAC", dest = "lmac", type="str",
                     help = "Local MAC address")
   parser.add_option("--rm", "--rmac", "--remoteMAC", dest = "rmac", type="str",
                     help = "Remote MAC address")
   parser.add_option("--receiveOnly", "--receiveonly",
                     dest = "receiveOnly", action = "store_true")
   parser.add_option("--sendOnly", "--sendonly", dest = "sendOnly", action="store_true")
   # parser.add_option("--promiscuous", dest = "promiscuous", action = "store_true")
   parser.set_defaults(lmac = "ffffffffffff", rmac = "ffffffffffff")
   opts, args = parser.parse_args()

   # Open socket
   sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
   sock.bind((Interface, ETH_P_ALL))
   sock.setblocking(0)

   # Contents of packet to send (constant)
   sendPacket = binascii.unhexlify(opts.rmac) + binascii.unhexlify(opts.lmac) + b'\x88\xb5' + binascii.hexlify(b'hello')


   # Repeat sending and receiving packets
   if opts.sendOnly:
      sendBytes = sock.send(sendPacket)
      print 'send packet to {} from {}'.format(opts.rmac, opts.lmac)
   elif opts.receiveOnly:
       while True:
          try:
              packet = sock.recv(BUF_SIZE)
              dmac = DMAC(packet)
              smac = SMAC(packet)
              ether_type = EtherType(packet)
              payload = Payload(packet)
              if smac == '000c2963f6c6':
                print 'received packet from {}'.format(smac)
                print 'ether_type: {}'.format(ether_type)
                print 'payload: {}'.format(payload)
          except socket.error:
              pass
          time.sleep(0.001001)

terminal()