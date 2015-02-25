import os
import pylearn2
import sys
import numpy
from pylearn2.config import yaml_parse


def output_file_string(params):
    string = []
    for key in params.keys():
        string.append(key + ": " + str(params[key]))
    return ' '.join(string)


hyper_params = {'norm_l1' : 0.08,
                'norm_l2' : 0.08,
                'norm_y' : 0.08,
                'init_l1' : 120,
                'init_l2' : 120,
                'irange_y' : 0.08,
                'l_r' : 0.01,
               }


for norm_l1 in numpy.linspace(0.01, 0.1, 10):
    for norm_l2 in numpy.linspace(0.01, 0.1, 10):
        for norm_y in numpy.linspace(0.01, 0.1, 10):
            for irange_y in numpy.linspace(0.01, 0.1, 10):
                for l_r in numpy.linspace(0.01, 0.1, 10):
                        with open('500AllMaxoutsWithDropout.yaml', 'r') as f:
                            yaml_file = f.read()
                        hyper_params['norm_l1'] = norm_l1
                        hyper_params['norm_l2'] = norm_l2
                        hyper_params['norm_y'] = norm_y
                        hyper_params['irange_y'] = irange_y
                        hyper_params['l_r'] = l_r
                        outputFile = open(output_file_string(hyper_params), 'w')

                        sys.stdout = outputFile
                        sys.stderr = outputFile

                        yaml_file = yaml_file % (hyper_params)
                        print yaml_file

                        train = yaml_parse.load(yaml_file)

                        try:
                            train.main_loop()
                        except:
                            pass





















