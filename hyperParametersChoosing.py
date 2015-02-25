import numpy
import os
import pylearn2
import sys

from pylearn2.config import yaml_parse
from pylearn2.datasets.mjsynth import MJSYNTH

def output_file_string(params):
    string = []
    for key in params.keys():
        string.append(key + ": " + str(params[key]))
    return ' '.join(string)


hyper_params = {
                'norm_l1' : 0.08,
                'norm_l2' : 0.08,
                'norm_y' : 0.01,
                'init_l1' : 120,
                'init_l2' : 120,
                'irange_y' : 0.01,
                'l_r' : 0.01,
               }


for norm_l1 in numpy.linspace(0.01, 0.1, 10):
    for norm_l2 in numpy.linspace(0.01, 0.1, 10):
        with open('500AllMaxoutsWithDropout.yaml', 'r') as f:
            yaml_file = f.read()
        hyper_params['norm_l1'] = norm_l1
        hyper_params['norm_l2'] = norm_l2
        outputFile = open('tests/' + output_file_string(hyper_params), 'w')

        sys.stdout = outputFile
        sys.stderr = outputFile

        yaml_file = yaml_file % (hyper_params)
        print yaml_file

        train = yaml_parse.load(yaml_file)

        try:
            train.main_loop()
        except:
            pass