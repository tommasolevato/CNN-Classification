# coding=utf-8
__author__ = 'Tommaso Levato'


import yaml
import numpy
import os
import pylearn2
import sys
from hyper_parameters_parser import Parser

from pylearn2.config import yaml_parse
from pylearn2.datasets.mjsynth.mjsynth import MJSYNTH
from pylearn2.datasets.mjsynth.config import Config


def output_file_string(params):
    string = []
    for key in params.keys():
        string.append(key + ": " + str(params[key]))
    return ' '.join(string)


p = Parser()


while p.has_other_configurations():
      with open(Config.getYamlFilename(), 'r') as f:
          yaml_file = f.read()
      hyper_params = p.get_next_configuration()
      outputFile = open('tests/' + p.get_num_configuration().__str__(), 'w')

      sys.stdout = outputFile
      sys.stderr = outputFile

      yaml_file = yaml_file % (hyper_params)
      print yaml_file

      train = yaml_parse.load(yaml_file)

      try:
          train.main_loop()
      except Exception as e:
          print e