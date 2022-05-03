#!/usr/bin/python

from __future__ import absolute_import
from __future__ import print_function
import copy
import getopt
import sys
import os
import transsys
#import optim 
from six.moves import range

transsys_program = None
parameters = None
model = 1
gremove = None
transsys_name = 'pol'

# Validate input
p = open('parapl.dat', 'r')

ran = transsys.RandomTranssysParameters()
ran.parse(p)
for i in range(1,model+1) :
  # jtk: control parameter model overwritten here (!!!)
  model = open('%s%02d.tra'%(transsys_name,i),'w')
  # jtk: control parameter transsys_program  (!!!!!)
  transsys_program = ran.generate_transsys('Transsys_Model%s'%i)
  model.write('%s'%transsys_program)

