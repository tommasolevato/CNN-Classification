# coding=utf-8
from os.path import isfile
__author__ = 'Tommaso Levato'

import logging

import numpy
import random
import os.path

from pylearn2.datasets import cache, dense_design_matrix
from pylearn2.expr.preprocessing import global_contrast_normalize
from pylearn2.utils import contains_nan
from scipy import misc
from PIL import Image
from pylearn2.datasets.mjsynth.config import Config



class MJSYNTH(dense_design_matrix.DenseDesignMatrix):
    classes = []
    
    def __init__(self, which_set, numOfClasses,
                 numOfExamplesPerClass, axes=('c', 0, 1, 'b')):
        self.height = 32
        self.width = 100
        self.axes = axes
        self.dtype = 'uint8'
        self.examples = []
        self.img_shape = (1, self.height, self.width)
        self.img_size = numpy.prod(self.img_shape)
        self.numOfClasses = numOfClasses
        self.numOfExamplesPerClass = numOfExamplesPerClass
        self.examplesPerClassCount = {}
        self.which_set = which_set
        if which_set == "train":
            self.fileToLoadFrom = "annotation_train.txt"
        elif which_set == "test":
            self.fileToLoadFrom = "annotation_test.txt"
        elif which_set == "valid":
            self.fileToLoadFrom = "annotation_val.txt"
        else:
            raise ValueError("Set not recognized")
        self.datapath = Config.getDatapath()
        self.preprocess = Config.doPreprocess()
        self.loadData()
        random.seed()

        view_converter = dense_design_matrix.DefaultViewConverter((self.height, self.width, 1),
                                                                   axes)


        super(MJSYNTH, self).__init__(X=numpy.cast['float32'](self.x), y=self.y, view_converter=view_converter,
                                       y_labels=self.numOfClasses)

        #assert not contains_nan(MJSYNTH.cache_set_dict[which_set]['X'])

    def findClasses(self):
        assert self.numOfClasses <= 88172
        while len(MJSYNTH.classes) < self.numOfClasses:
            randomClass = random.randint(0, 88171)
            if randomClass not in MJSYNTH.classes:
                MJSYNTH.classes.append(randomClass.__str__())
        assert len(MJSYNTH.classes) == self.numOfClasses

    def findExamples(self):
        for classToInitialize in MJSYNTH.classes:
            self.examplesPerClassCount[classToInitialize] = 0

        with open(self.datapath + self.fileToLoadFrom) as f:
            for line in f:
                exampleClass = line.split(" ")[1].rstrip()
                file = line.split(" ")[0].rstrip()
                try:
                    if self.examplesPerClassCount[exampleClass] < self.numOfExamplesPerClass:
                        self.examples.append(file[2:len(file)])
                        self.examplesPerClassCount[exampleClass] += 1
                    if len(self.examples) == self.numOfClasses * self.numOfExamplesPerClass:
                        break
                except KeyError:
                    pass

    def findOtherExamplesIfNeeded(self):
        if len(self.examples) < self.numOfClasses * self.numOfExamplesPerClass:
            with open(self.datapath + self.fileToLoadFrom) as f:
            	for line in f:
                	exampleClass = line.split(" ")[1].rstrip()
                	file = line.split(" ")[0].rstrip()
                	if exampleClass in MJSYNTH.classes and file not in self.examples:
                    		self.examples.append(file[2:len(file)])
                    		self.examplesPerClassCount[exampleClass] += 1
                	if len(self.examples) == self.numOfClasses * self.numOfExamplesPerClass:
                        	break
        assert len(self.examples) == self.numOfClasses * self.numOfExamplesPerClass

    def loadData(self):
        if MJSYNTH.classes == []:
            self.findClasses()
        self.findExamples()
        self.findOtherExamplesIfNeeded()
        self.loadImages()

    def loadImages(self):
        self.x = numpy.zeros((len(self.examples), self.img_size), dtype=self.dtype)
        i = 0
        tmp = []
        for example in self.examples:
            filename = self.datapath + example
            data = self.loadImage(filename)
            classLabel = self.loadClassLabel(filename)
            tmp.append(classLabel)
            self.x[i, :] = data.reshape(1, self.height * self.width)
            i += 1
        self.y = numpy.array(tmp)
        
    def loadImage(self, filename):
        if not isfile(filename):
            print filename + "does not exist"
        else:
            data = Image.open(filename)
            data = data.resize([self.width, self.height])
            data = data.convert("L")
            data = numpy.array(data)
            if self.preprocess:
                mean = numpy.mean(data)
                std = numpy.std(data)
                data = numpy.subtract(data, mean)
                data = numpy.divide(data, std)
            return data
        
    def loadClassLabel(self, filename):
        classLabelTokens = filename.split("_")
        classLabel = classLabelTokens[-1].split(".")[0]
        assert classLabel in MJSYNTH.classes
        tmp = []
        tmp.append(MJSYNTH.classes.index(classLabel))
        return tmp
