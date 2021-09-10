from scapy import all as scapy
import signal
import interface, sys

def abort_sniff(_1,_2):
    interface.show()
    sys.exit(0)

def sniff_packets():
    packets=scapy.sniff(prn=lambda packet: packet.summary())

def run():
    signal.signal(20,abort_sniff)
    sniff_packets()
