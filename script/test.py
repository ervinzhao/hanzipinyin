#! /usr/bin/python3


import os
import sys

hanzilist = open('hzpy-utf8.txt', 'r')

last = 0x4e00
lack = 0
highuse = 0
for line in hanzilist:
    columns = line.split(',')
    uni = int(columns[4], 16)
    use = int(columns[5])
    if last == uni or last == uni - 1:
        pass
    else:
        for i in range(last + 1, uni):
            print(hex(i))
            lack += 1
    if use == 1:
        highuse += 1
    last = uni
print("Total result :")
print(lack)
print("Total high use")
print(highuse)
