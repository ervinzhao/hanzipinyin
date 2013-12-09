#!/usr/bin/python

t = open('table', 'r')
for line in t:
    columns = line.split()
    simp = columns[0][2:7]
    comp = columns[2][2:7]
    print("%s %s" % (simp, comp))
t.close()
