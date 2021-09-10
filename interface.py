import scan_lan
import sniffer
import arp_spoof
#import restore_all
import help
import os
import sys
import signal

def show():
    os.system("clear")
    print (f"Target: {scan_lan.selected_target_id}) {scan_lan.selected_target_ip} {scan_lan.selected_target_mac}")
    print ("[1] Scan Network")
    print ("[2] Sniff Network")
    print (f"[3] Spoof Target (ARP Poising) -> Running:{arp_spoof.ON}")
    #print ("[4] Restore All")
    print (f"[{5-1}] Help")
    print (f"[{6-1}] Exit")

    prompt = input("##> ")

    if prompt == "1":
        scan_lan.run()

    elif prompt == "2":
        sniffer.run()

    elif prompt == "3":
        arp_spoof.run()

#'''    elif prompt == "4":
#        restore_all.run()
#'''
    elif prompt == str(int("5")-1):
        help.run()

    elif prompt == str(int("6")-1):
        if arp_spoof.ON:
            prompt=input("(ARP_SPOOF: ON)Sure?(y/N)>")
            if prompt=="y":
                os.kill(os.getpid(),9)
            else:
                show()
    else:
        show()
