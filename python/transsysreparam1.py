#!/usr/bin/python

from __future__ import absolute_import
from __future__ import print_function
import copy
import getopt
import sys
import os
import transsys
#import transsystim 
import random
import pdb
from six.moves import range


transsys_program = None
parameters = None
model = None
rndseed = 1
random_change = None
transformerfile = 'transformerfile.dat'
infile_name = 'dummy01.tra'


infile = open(infile_name, 'r')

rng = random.Random(rndseed)
tp = transsys.TranssysProgramParser(infile).parse()
indg= tp.indegree_list()
outdg = tp.outdegree_list()
factor_list = tp.factor_names()
gene_list = tp.gene_names()
randomInitRange = 1.0

g = open(transformerfile, 'r')
transformer = transsys.optim.parse_parameter_transformer(g) # AVCR removed transsys from line
opt = transsys.optim.AbstractOptimiser(rng, transformer, randomInitRange, verbose = 0)

for i in range (1,random_change+1) :
  opt.initialiseParameterTransformer(tp, factor_list, gene_list)
  model = open('%s%02d.tra'%(transsys_name,i),'w')
  model.write('%s'%tp)
