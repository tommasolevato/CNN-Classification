# coding=utf-8
__author__ = 'Tommaso Levato'


import numpy


class Parser:

    def __init__(self):
        self.hyper_parameters = {}
        self.hyper_parameters_list = {}
        for line in open('hyper_parameters', 'r'):
            key = line.split("=")[0].rstrip()
            value_token = line.split("=")[1].rstrip().split(":")
            if len(value_token) == 1:
                value = self.parse_token(value_token[0])
                self.hyper_parameters[key] = [value]
                self.hyper_parameters_list[key] = 1
            elif len(value_token) == 3:
                start = self.parse_token(value_token[0])
                stop = self.parse_token(value_token[1])
                num_of_elements = self.parse_token(value_token[2])
                self.hyper_parameters[key] = numpy.linspace(start, stop, num_of_elements)
                self.hyper_parameters_list[key] = num_of_elements
            else:
                raise Exception("Sintax Error")
            if "_prob" in key:
                prefix = key.split("_")[0]
                input_scales = prefix + "_input_scales"
                input_scales_value = 1 / self.hyper_parameters[key]
                self.hyper_parameters[input_scales] = input_scales_value
                self.hyper_parameters_list[input_scales] = len(input_scales_value)

                w_lr_scale = "w_scale_" + prefix
                w_lr_scale_value = self.hyper_parameters[key]*self.hyper_parameters[key]
                self.hyper_parameters[w_lr_scale] = w_lr_scale_value
                self.hyper_parameters_list[w_lr_scale] = len(w_lr_scale_value)
        self.configuration_indexes = {}
        for key in self.hyper_parameters_list:
            self.configuration_indexes[key] = 0
        self.terminated = False

    def get_next_configuration(self):
        dict = {}
        if self.is_last_configuration():
            self.terminated = True
        for key in self.hyper_parameters:
            dict[key] = self.hyper_parameters[key][self.configuration_indexes[key]]
        self.increase_index(key)
        return dict

    def increase_index(self, key):
        if self.configuration_indexes[key] < self.hyper_parameters_list[key] - 1:
            self.configuration_indexes[key] += 1
            self.reset_next_indexes(key)
        else:
            if self.first_key() != key:
                self.increase_index(self.prev_key(key))

    def is_last_configuration(self):
        for key in self.configuration_indexes.keys():
            if self.configuration_indexes[key] != self.hyper_parameters_list[key] - 1:
                return False
        return True


    def prev_key(self, key):
        it = iter(self.configuration_indexes.keys())
        candidate = it.next
        assert candidate != key
        for key_to_test in it:
            if key == key_to_test:
                return candidate
            candidate = key_to_test

    def first_key(self):
        it = iter(self.configuration_indexes.keys())
        key = it.next()
        return key

    def reset_next_indexes(self, key):
        it = iter(self.configuration_indexes.keys())
        while it.next() != key:
            pass
        for key_to_reset in it:
            assert key_to_reset != key
            self.configuration_indexes[key_to_reset] = 0

    def parse_token(self, token):
        if '.' in token:
            return round(float(token),2)
        else:
            return int(token)
        raise Exception

    def has_other_configurations(self):
        return not self.terminated