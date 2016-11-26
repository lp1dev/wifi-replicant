#!/usr/bin/python

import wifi

nic1="wlan0"
nic2="wlan1"
cells=[]

#
id=None
passphrase=""

def write_conf(conf):
    with open("hostapd.conf", "a+") as f:
        f.write(conf)

def make_conf():
    cell = cells[id]
    conf = ""
    conf += "interface=%s\n" %nic2
    conf += "ssid=%s\n" %cell.ssid
    conf += "channel=%i\n" %cell.channel
    conf += "hw_mode=%s\n" %cell.mode
    conf += "macaddr_acl=0\n"
    if cell.encrypted:
        conf += "auth_algs=1\n"
        if cell.encryption_type == "wpa2":
            conf += "wpa=2\n"
            conf += "wpa_passphrase=%s\n" %passphrase
            conf += "wpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP"
    write_conf(conf)
    return

def scan():
    global cells
    print("Select a network to extend :")
    for idx, cell in enumerate(wifi.Cell.all(nic1)):
        cells.append(cell)
        print("[%i] : %s" %(idx, cell))

def connect():
    global passphrase
    if id > len(cells) or id < 0:
        exit("Invalid id")
    cell = cells[id]
    scheme = wifi.Scheme.find(nic1, cell.ssid)
    if scheme is None:
        if cell.encrypted:
            print(cell.encryption_type, end='')
            passphrase = input(" passphrase :")
            print("passphrase:[%s]" %passphrase)
            scheme = wifi.Scheme.for_cell(nic1, cell.ssid, cell, passphrase)
        else:
            scheme = wifi.Scheme.for_cell(nic1, cell.ssid, cell)
        scheme.save()
    scheme.activate()
    return

def main():
    global id
    scan()
    try:
        id = int(input(":"))
    except TypeError as e:
        exit("Invalid value")
    connect()
    make_conf()
    return 0

if __name__ == "__main__":
    main()
