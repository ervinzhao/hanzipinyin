#! /usr/bin/python3

import sqlite3

convertionTable = {}
reverseTable = {}
convertionFile = open('simplified2traditional.txt', 'r')
for line in convertionFile:
    columns = line.split()
    sim = int(columns[0], 16)
    tra = int(columns[1], 16)
    convertionTable[sim] = tra
    reverseTable[tra] = sim
convertionFile.close()

conn = sqlite3.connect('hanzi.db')
cursor = conn.cursor()

# unicode : codec for the hanzi
# pinyin  : pinyin
# type    : 1 for simplified Chinese charactor, 2 for traditional, 0 for others.
# map     : corresponding simplified/traditional Chinese charactor for
#           traditional/simplified Chinese charactor.
# freq    : frequency for this Chinese charactor.
cursor.execute('create table if not exists hanzi(unicode int primary key, pinyin text, type int, map int, freq int)')

hanziFile = open('hzpy-utf8.txt', 'r')
hanziTable = {}
for line in hanziFile:
    columns = line.split(',')
    uni = int(columns[4], 16)
    pinyin = columns[1]
    freq = int(columns[5])
    
    t = 0
    m = 0
    if uni in convertionTable:
        t = 1
        m = convertionTable[uni]
    elif uni in reverseTable:
        t = 2
        m = reverseTable[uni]
    if uni in hanziTable:
        hanzi = hanziTable[uni]
        if freq > hanzi[4]:
            hanzi[1] = pinyin + ',' + hanzi[1]
            hanzi[4] = freq
        else:
            hanzi[1] = hanzi[1] + ',' + pinyin
    else:
        hanzi = []
        hanzi.append(uni)
        hanzi.append(pinyin)
        hanzi.append(t)
        hanzi.append(m)
        hanzi.append(freq)
        hanziTable[uni] = hanzi
hanziFile.close()
for uni in hanziTable:
    sql = "insert into hanzi values(%d, '%s', %d, %d, %d)" % tuple(hanziTable[uni])
    cursor.execute(sql)
conn.commit()
conn.close()

