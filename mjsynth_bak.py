# coding=utf-8
__author__ = 'Tommaso Levato'

import logging

import numpy

from pylearn2.datasets import cache, dense_design_matrix
from pylearn2.expr.preprocessing import global_contrast_normalize
from pylearn2.utils import contains_nan
from scipy import misc
from PIL import Image


class MJSYNTH(dense_design_matrix.DenseDesignMatrix):

    def __init__(self, which_set, numOfClasses,
                 numOfExamplesPerClass, axes=('b', 0, 1, 'c')):
        self.height = 32
        self.width = 100
        self.axes = axes
        self.dtype = 'uint8'
        self.examples = []
        self.img_shape = (1, self.height, self.width)
        self.img_size = numpy.prod(self.img_shape)
        self.numOfClasses = numOfClasses
        self.numOfExamplesPerClass = numOfExamplesPerClass
        self.classes = []
        self.examplesPerClassCount = {}
        if which_set == "train":
            self.fileToLoadFrom = "annotation_train.txt"
        elif which_set == "test":
            self.fileToLoadFrom = "annotation_test.txt"
        elif which_set == "valid":
            self.fileToLoadFrom = "annotation_val.txt"
        else:
            raise ValueError("Set not recognized")
        self.datapath = "/media/tommaso/Lacie/mnt/ramdisk/max/90kDICT32px/"

        self.loadData()
        X = numpy.cast['float32'](self.x)

        view_converter = dense_design_matrix.DefaultViewConverter((self.height, self.width, 1),
                                                                   axes)

        super(MJSYNTH, self).__init__(X=X, y=self.y, view_converter=view_converter,
                                       y_labels=numOfClasses)

        assert not contains_nan(self.X)

    def findClasses(self):
        with open(self.datapath + "annotation_train.txt") as f:
            for line in f:
                exampleClass = line.split(" ")[1].rstrip()
                if exampleClass not in self.classes:
                    self.classes.append(exampleClass)
                if len(self.classes) == self.numOfClasses:
                    break

    def findExamples(self):
        for classToInitialize in self.classes:
            self.examplesPerClassCount[classToInitialize] = 0
            self.examplesPerClassCount[classToInitialize] = 0

        with open(self.datapath + self.fileToLoadFrom) as f:
            for line in f:
                exampleClass = line.split(" ")[1].rstrip()
                file = line.split(" ")[0].rstrip()
                try:
                    if self.examplesPerClassCount[exampleClass] < self.numOfExamplesPerClass:
                        self.examples.append(file[2:len(file)])
                        self.examplesPerClassCount[exampleClass] +=1
                    if len(self.examples) == self.numOfClasses*self.numOfExamplesPerClass:
                        break
                except KeyError:
                    pass

    def findOtherExamplesIfNeeded(self):
        if len(self.examples) < self.numOfClasses*self.numOfExamplesPerClass:
            with open(self.datapath + self.fileToLoadFrom) as f:
            	for line in f:
                	exampleClass = line.split(" ")[1].rstrip()
                	file = line.split(" ")[0].rstrip()
                	if exampleClass in self.classes and file not in self.examples:
                    		self.examples.append(file[2:len(file)])
                    		self.examplesPerClassCount[exampleClass] +=1
                	if len(self.examples) == self.numOfClasses*self.numOfExamplesPerClass:
                        	break
        assert len(self.examples) == self.numOfClasses*self.numOfExamplesPerClass


    def loadData(self):
        self.findClasses()
        self.findExamples()
        self.findOtherExamplesIfNeeded()
        self.loadImages()

    def loadImages(self):
        i = 0
        self.x = numpy.zeros((len(self.examples), self.img_size), dtype=self.dtype)
        tmp = []
        for example in self.examples:
            filename = self.datapath + example
            data = Image.open(filename)
            data = data.resize([self.width, self.height])
            data = data.convert("L")
            labelTokens = filename.split("_")
            label = labelTokens[-1].split(".")[0]
            if label not in self.classes:
                self.classes.append(label)
            self.x[i, :] = list(data.getdata())
            labelList = []
            labelList.append(self.classes.index(label))
            tmp.append(labelList)
            i += 1
        self.y = numpy.array(tmp)