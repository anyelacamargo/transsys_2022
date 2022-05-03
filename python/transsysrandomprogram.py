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
transsys_name = 'dummy'
#optlist, args = getopt.getopt(sys.argv[1:], 'n:m:g:p:lvh')
#num_operation=10
#for opt, par in optlist :
#  if opt == '-h' :
#    print('-n <Transsys program name>: Transsys program name')
#    print('-m:<num>: specify how many transsys program models are to be created')
#    print('-g:<num>: gene to remove \'gdummy\' ')
#    print('-p:<Transsys program parameters>: Transsys program parameters')
#    print('-h: print this help and exit')
#    sys.exit()
#  if opt == '-n' :
#    transsys_name = par
#  elif opt == '-m' :
#    model = int(par)
#  elif opt == '-g' :
#    gremove = par
#  elif opt == '-p' :
#    parameters = par
#  else :
#    raise Exception('unhandled option "%s"' % opt)

# Validate input
p = open('parapl.dat', 'r')

ran = transsys.RandomTranssysParameters()
ran.parse(p)
for i in range(1,model+1) :
  # jtk: control parameter model overwritten here (!!!)
  model = open('%s%02d.tra'%(transsys_name,i),'w')
  # jtk: control parameter transsys_program  (!!!!!)
  transsys_program = ran.generate_transsys('Transsys_Model%s'%i)
  #if gremove is not None :
  #  i = transsys_program.find_gene_index(gremove)
  #  del transsys_program.gene_list[i]
  model.write('%s'%transsys_program)

