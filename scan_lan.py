import signal
from scapy import all as scapy
import scapy.layers.l2 as l2
import scapy.layers.inet as inet
import sys, os

import interface
import arp_spoof

abort = False
selected_target_id=0
selected_target_ip="0.0.0.0"
selected_target_mac="ff:ff:ff:ff:ff:ff".upper()
ip_table=list()
mac_table=list()

def control_poison_is_run():
    if arp_spoof.ON:
        arp_spoof.ON=False

def select_target(target_len):
    while True:
        prompt = input("Target ID> ")
        try:
            prompt=int(prompt)
        except:
            print ("[-] Unknown Target ID...")

        if prompt <= target_len:
            return prompt
        else:
            print ("[-] Unknown Target ID...")

def catch_abort(_1,_2):
    global abort
    abort = True
    print ("[!] Aborting...")

def get_results(result):
    clients_ip = list()
    clients_mac = list()
    for j in range(0, len(result[0])):
        ip = result[0][j][1].psrc
        mac = result[0][j][1].src
        if ip not in clients_ip and mac not in clients_mac:
            clients_ip.append(ip)
            clients_mac.append(mac)

    return (clients_ip, clients_mac)

def print_table(scan_counter, ip_table, mac_table):
    os.system("clear")
    print (f"Scan Count: {scan_counter}"+" "*9+"Abort: Ctrl+Z\n")
    print (" "*3+" "*int(int(len(ip_table))/10)+"IP Address"+" "*9+"MAC Address")
    for i in range(0,len(ip_table)):
        print (f"{i+1}) "+str(ip_table[i])+" "*(len("IP Address"+" "*9)-len(ip_table[i]))+mac_table[i].upper())

def arp_scan(gateway="192.168.1.1/24", broadcast="ff:ff:ff:ff:ff:ff".upper()):
    global ip_table
    global mac_table

    ip_table = list()
    mac_table = list()
    scan_counter = 0

    while True:
        arp_packet = l2.ARP(pdst=gateway)
        ether_packet = l2.Ether(dst=broadcast)
        packet = ether_packet / arp_packet
        ip_list, mac_list = get_results(scapy.srp(packet, timeout=3, verbose=0))
        scan_counter += 1
        for ip in ip_list:
            if ip not in ip_table:
                ip_table.append(ip)
        for mac in mac_list:
            if mac not in mac_table:
                mac_table.append(mac)

        print_table(scan_counter, ip_table, mac_table)
        print ("Aborted: "+str(abort))
        if abort:
            return (ip_table, mac_table, scan_counter)

def run():
    global abort
    global selected_target_id
    global selected_target_ip
    global selected_target_mac
    global ip_table
    global mac_table

    control_poison_is_run()
    abort=False
    signal.signal(20, catch_abort)
    result = arp_scan()
    selected_target_id=str(select_target(len(result[0])))
    selected_target_ip=result[0][int(selected_target_id)-1]
    selected_target_mac=result[1][int(selected_target_id)-1]
    interface.show()
