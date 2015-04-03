# coding=utf-8
__author__ = 'Tommaso Levato'

from os import walk

bestFile = ''
bestValue = float("inf")

for (_, _, files) in walk('tests'):
    for experiment in files:
        for line in open('tests/' + experiment, 'r'):
            if "valid_y_misclass" in line and len(line.split(" ")) > 1:
                value = float(line.split(" ")[1])
                if value < bestValue:
                    bestFile = experiment
                    bestValue = value
print bestFile
print bestValue