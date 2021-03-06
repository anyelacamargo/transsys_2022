#!/usr/bin/env python

# $Id: utils.py 322 2008-07-24 19:38:51Z jtk $

# $Log$
# Revision 1.1  2005/03/08 17:12:02  jtk
# Initial revision
#
# Revision 1.2  2003/02/04 23:46:21  kim
# added RouletteWheel
#
# Revision 1.1  2003/01/28 21:12:05  kim
# initial toolbox assembly
#


"""Miscellaneous utilities.
"""

from __future__ import absolute_import
#import types
import math
import random
import re
from six.moves import range
from functools import reduce


def is_nan(x) :
  """Determine whether x is NaN.

This function is a temporary solution, to be replaced if and when
python provides this functionality. The current implementation
returns x != x; this works with current versions of python and Linux,
but cannot be guaranteed to work generally.

@param x: the floating point object to be tested
@return: C{True} if C{x} is NaN
@rtype: boolean
"""
  return x != x


def parse_int(f, label, allowNone = False) :
  """retrieves an int from a line of the form::

<label>: <int>

Raises an error if label is not matched or not followed by a
colon (optionally flanked by whitespace) and an int.
"""
  r = '%s\\s*:\\s*(([0-9]+)|(None))' % label
  line = f.readline()
  m = re.match(r, line.strip())
  if m is None :
    raise Exception('parse_int: failed to obtain int "%s" in "%s"' % (label, line.strip()))
  if m.group(2) is None :
    if allowNone :
      return None
    raise Exception('parse_int: None not permitted')
  return int(m.group(1))


def parse_float(f, label, allowNone = False) :
  """retrieves a float from a line of the form::

<label>: <float>

Raises an error if label is not matched or not followed by a
colon (optionally flanked by whitespace) and a float.
"""
  r = '%s\\s*:\\s*(([+-]?([0-9]+((\\.[0-9]+)?)|(\\.[0-9]+))([Ee][+-]?[0-9]+)?)|(None))' % label
  line = f.readline()
  m = re.match(r, line.strip())
  if m is None :
    raise Exception('parse_float: failed to obtain float "%s" in "%s"' % (label, line.strip()))
  if m.group(2) is None :
    if allowNone :
      return None
    raise Exception('parse_float: None not permitted')
  # print m.group(), '-->', float(m.group(1))
  return float(m.group(1))


def parse_string(f, label) :
  """retrieves a string from a line of the form::

<label>:<string>

Raises an error if label is not matched or not followed by a
colon (optionally preceded by whitespace) and a (possibly empty) string.
"""
  r = '%s\\s*:(.*)' % label
  line = f.readline()
  if len(line) > 0 :
    line = line[:-1]
  m = re.match(r, line)
  if m is None :
    raise Exception('parse_string: failed to obtain string "%s" in "%s"' % (label, line.strip()))
  return m.group(1)


def parse_boolean(f, label, allowNone = False) :
  """retrieves a boolean value from a line of the form::

<label>: <booleanvalue>

Raises an error if label is not matched or not followed by a
colon (optionally flanked by whitespace) and a boolean value,
i.e. C{True}, C{False} or, if allowed, C{None}.
"""
  r = '%s\\s*:\\s*((False)|(True)|(None))' % label
  line = f.readline()
  m = re.match(r, line.strip())
  if m is None :
    raise Exception('parse_boolean: failed to obtain boolean "%s" in "%s"' % (label, line.strip()))
  if m.group(1) == None :
    if allowNone :
      return None
    raise Exception('parse_boolean: None not permitted')
  return m.group(1) == 'True'


def name_value_pair(x, label) :
  """Encode a labelled quantity in a parseable way.

This function can be thought of as an inverse to C{parse_int},
C{parse_float} and C{parse_string}.

@param x: the value to be encoded
@param label: the label to be used
"""
  if x is None :
    return '%s: None' % label
  elif type(x) is int :
    return '%s: %d' % (label, x)
  elif type(x) is float :
    return '%s: %1.17e' % (label, x)
  elif type(x) is bytes :
    return '%s: %s' % (label, x)
  elif type(x) is bool :
    return '%s: %s' % (label, str(x))
  raise Exception('unsupported type %s' % str(type(x)))


def tablecell(x) :
  """Render C{x} as a string suitable as an R table element.

Currently supported types are:
  - C{None}, rendered as C{NA}
  - C{int}
  - C{float}, formatted using C{'%1.17e'} as a format string
  - C{boolean}, rendered as C{TRUE} or C{FALSE}.

@param x: the value to be converted to a table element
@return: a string representing C{x}
@rtype: C{String}
"""
  if x is None :
    return 'NA'
  elif type(x) is int :
    return '%d' % x
  elif type(x) is float :
    return '%1.17e' % x
  elif type(x) is bytes :
    return x
  elif type(x) is bool :
    if x :
      return 'TRUE'
    else :
      return 'FALSE'
  raise Exception('unsupported type %s' % str(type(x)))


def table_row(l) :
  """Render elements of C{l} as a whitespace separated row."""
  s = ''
  glue = ''
  for x in l :
    s = s + glue + tablecell(x)
    glue = ' '
  return s


def dictionary_tablestring(d, row_format = '# %s: %s\n') :
  """Render a dictionary as a 'table', consisting of name/value rows,
formatted by the format string.

The format string C{row_format} must contain exactly two string
format conversions.

@param d: the dictionary to be rendered as a table
@type d: C{dictionary}
@param row_format: the format string for the rows of the table
@type row_format C{String}
@return: the table as a string
@rtype: C{String}
"""
  s = ''
  for k in d.keys() :
    s = s + row_format % (str(k), str(d[k]))
  return s
    

def hamming_distance(s1, s2) :
  """Compute the Hamming distance (number of different elements)
between two strings (or other sequence types).

Notice that this function compares objects for identity, not for
equality.

@param s1: first sequence
@param s2: second sequence
@return: Hamming distance between C{s1} and C{s2}
@rtype: int
"""
  if len(s1) != len(s2) :
    raise Exception('length mismatch')
  n = 0
  for i in range(len(s1)) :
    if s1[i] != s2[i] :
      n = n + 1
  return n


def inner_product(v1, v2) :
  """Compute the inner product of two vectors.

@param v1: the first vector (any sequence consisting of numeric elements)
@param v2: the second vector (a sequence of the same length)
@return: the inner product of C{v1} and C{v2}
@rtype: float
"""
  if len(v1) != len(v2) :
    raise Exception('unequal vector lengths')
  s = 0.0
  for i in range(len(v1)) :
    s = s + v1[i] * v2[i]
  return s


def euclidean_distance_squared(v1, v2) :
  """Compute the square of the Euclidean distance between C{v1} and C{v2}."""
  if len(v1) != len(v2) :
    raise Exception('length mismatch')
  d2 = 0.0
  for i in range(len(v1)) :
    d = v1[i] - v2[i]
    d2 = d2 + d * d
  return d2


def euclidean_distance(v1, v2) :
  """Compute the Euclidean distance between C{v1} and C{v2}."""
  return math.sqrt(euclidean_distance_squared(v1, v2))


def euclidean_norm_squared(v) :
  """Compute the square of the euclidean norm of C{v}."""
  return sum([x * x for x in v])


def euclidean_norm(v) :
  """Compute the euclidean norm of C{v}."""
  return math.sqrt(euclidean_norm_squared(v))


def normalised_vector(v) :
  """Normalise a vector.

Computes a vector colinear with C{v} and with unit length.

@return: the normalised vector
"""
  n = float(euclidean_norm(v))
  if n == 0 :
    raise Exception('cannot normalise a vector of length 0')
  return [x / n for x in v]


def mean_and_stddev(l) :
  """Compute mean and standard deviation of a list of floating point values.

@return: the mean and the standard deviation
@rtype: tuple
"""
  if len(l) <= 1 :
    raise Exception('cannot compute the standard deviation of less than 2 values (%d values given)' % len(l))
    # return l[0], 0.0
  m = sum(l) / float(len(l))
  d = [x - m for x in l]
  d2 = [x * x for x in d]
  v = sum(d2) / float(len(l) - 1)
  # print 'v = %f' % v
  # print l
  # print v
  sd = math.sqrt(v)
  return m, sd


def shannon_entropy(v) :
  """Compute the Shannon entropy of C{v}, normalised so components add up to 1, in bits.
"""
  if min(v) < 0.0 :
    raise Exception('negative components in entropy computation')
  s = sum(v)
  v1 = [x / s for x in v]
  e = 0
  for p in v1 :
    if p > 0.0 :
      e = e - p * math.log(p, 2.0)
  return e


def uncentered_correlation(x, y) :
  """Uncentered correlation of C{x} and C{y}.

The uncentered correlation is the cosine of the angle of
C{x} and C{y}. This amounts to computing the correlation,
"but without centering".

Notice that this is not a proper correlation. This function is used
as a similarity score of gene expression profiles by Eisen et.al.,
and it is provided only as a means to implement their approach.

@param x: vector
@type x: iterable of numeric
@param y: vector
@type y: iterable of numeric
@return: cosine of angle of x and y
@rtype: C{float}
"""
  if len(x) != len(y) :
    raise Exception('x and y have unequal length')
  if len(x) == 0 :
    raise Exception('x and y have 0 components')
  nx = euclidean_norm(x)
  if nx == 0.0 :
    raise Exception('euclidean norm of x is 0')
  ny = euclidean_norm(y)
  if ny == 0.0 :
    raise Exception('euclidean norm of y is 0')
  r = inner_product(x, y) / nx / ny
  return r


def correlation_coefficient(x, y) :
  """Compute the Pearson correlation coefficient of C{x} and C{y}.

@param x: vector
@type x: iterable of numeric
@param y: vector
@type y: iterable of numeric
@return: Pearson correlation coefficient
@rtype: C{float}
"""
  if len(x) != len(y) :
    raise Exception('x and y have unequal length')
  if len(x) == 0 :
    raise Exception('x and y have 0 components')
  x_mean = float(sum(x)) / float(len(x))
  xc = [float(v) - x_mean for v in x]
  nx = euclidean_norm(xc)
  if nx == 0.0 :
    raise Exception('standard deviation of x is zero')
  y_mean = float(sum(y)) / float(len(y))
  yc = [float(v) - y_mean for v in y]
  ny = euclidean_norm(yc)
  if ny == 0.0 :
    raise Exception('standard deviation of y is zero')
  r = inner_product(xc, yc) / nx / ny
  return r


class UniformRNG :
  """Callable class producing random floating point values from
a uniform distribution.

Based on the standard random module.
"""

  def __init__(self, rndseed, min_value = 0.0, max_value = 1.0) :
    """
@param rndseed: random seed
@param min_value: minimal value (inclusive)
@param max_value: maximal value (exclusive)
@return: a random value r from [min_value, max_value[
@rtype: float
"""    
    self.rng = random.Random(rndseed)
    self.min_value = min_value
    self.max_value = max_value


  def __call__(self) :
    return self.rng.uniform(self.min_value, self.max_value)


def randomise_transsys_values(transsys_program, random_function, gene_name_list = None, factor_name_list = None) :
  """Randomise numerical values in value nodes by replacing them
with values obtained from the random_function.

gene_name_list and factor_name_list identify the genes and the
factors to have their numerical values randomised. The default value
of None indicates that all genes / factors should be randomised.
"""
  value_expression_list = []
  if factor_name_list is None :
    value_expression_list.extend(transsys_program.getFactorValueNodes())
  else :
    for fn in factor_name_list :
      factor = transsys_program.find_factor(fn)
      value_expression_list.extend(factor.getValueNodes())
  if gene_name_list is None :
    value_expression_list.extend(transsys_program.getGeneValueNodes())
  else :
    for gn in gene_name_list :
      gene = transsys_program.find_gene(gn)
      value_expression_list.extend(gene.getValueNodes())
  for n in value_expression_list :
    n.value = random_function()


def interval_list(interval_size_list, x0 = 0.0) :
  """Make a list of interval borders of contiguous intervals of given sizes."""
  return reduce(lambda x, y : x + [x[-1] + y], interval_size_list, [x0])


def find_interval_index(x, borders) :
  """Find the index of the interval within which C{x} is located.

Uses binary search.

@return: index C{i} such that C{borders[i] <= x < borders[i + 1]},
  -1 if C{x < borders[0]}, C{len(borders)} if C{x >= borders[-1]}.
@rtype: int
"""
  if x < borders[0] :
    return -1
  if x >= borders[-1] :
    return len(borders) - 1
  imin = 0
  imax = len(borders) - 1
  while imax - imin > 1 :
    i = (imin + imax) / 2
    # print i, borders[i], x, borders[i] < x
    if borders[i] <= x :
      imin = i
    else :
      imax = i
    # print imin, imax, i
  return imin


def unique(l) :
  """Compute a nonredundant list of elements in C{l}.

The order of elements is preserved. Redundant elements are determined
by comparison, and the first element is placed in the nonredundant list.
Notice that if elementa are equal but not identical (e.g. 0 and 0.0),
only the first one in C{l} appears in the unique list.

@param l: a list or other iterable type
@type l: iterable
@return: list of unique elements
@rtype: C{list}
"""
  u = []
  for e in l :
    if e not in u :
      u.append(e)
  return u


class transrnd :
  """Random number generator class.

This is a legacy random number generator which was introduced before
the standard Python random package appeared. It is a Python implementation
of the random number generator implemented by the C{random} function
in the GNU C standard library.

This class should not be used anymore in new projects.
"""

  def __init__(self, seed = 1, state = None, fptr = None, rptr = None) :
    self.rand_type = 4
    self.rand_deg = 63
    self.rand_sep = 1
    self.RAND_MAX = 0x7fffffff
    self.gset = None
    if state is not None and fptr is not None and rptr is not None :
      raise Exception('transrnd::__init__: restarting from saved state info not implemented')
      self.state = copy.deepcopy(state)
      self.fptr = fptr
      self.rptr = rptr
    else :
      self.fptr = 2
      self.rptr = 1
      self.seed = seed
      self.srandom(seed)


  def srandom(self, seed) :
    self.state = [0] * self.rand_deg
    self.state[0] = int(seed)
    self.gset = None
    for i in range(1, self.rand_deg) :
      self.state[i] = 1103515245 * self.state[i - 1] + 12345;
      # self.state[i] = 1103515145L * self.state[i - 1] + 12345L;  # linux libc version
    self.fptr = self.rand_sep
    self.rptr = 0
    for i in range(10 * self.rand_deg) :
      self.random()


  def random(self) :
    self.state[self.fptr] = (self.state[self.fptr] + self.state[self.rptr]) & 0xffffffff
    i = (self.state[self.fptr] >> 1) & 0x7fffffff
    self.fptr = self.fptr + 1
    if self.fptr >= self.rand_deg :
      self.fptr = 0
      self.rptr = self.rptr + 1
    else :
      self.rptr = self.rptr + 1
      if self.rptr >= self.rand_deg :
        self.rptr = 0
    return int(i)


  def rnd(self) :
    return float(self.random()) / (float(self.RAND_MAX) + 1)


  def random_range(self, rceil) :
    m = int(self.RAND_MAX) + 1
    m = m - m % rceil
    r = self.random()
    while r >= m :
      r = self.random()
    return r % rceil


  def gauss(self) :
    """adapted from Numerical Recipes in C"""
    if self.gset is None :
      v1 = 2.0 * self.random() / 0x7fffffff - 1.0
      v2 = 2.0 * self.random() / 0x7fffffff - 1.0
      rsq = v1 * v1 + v2 * v2
      while rsq >= 1.0 or rsq == 0.0 :
        v1 = 2.0 * self.random() / 0x7fffffff - 1.0
        v2 = 2.0 * self.random() / 0x7fffffff - 1.0
        rsq = v1 * v1 + v2 * v2
      fac = math.sqrt(-2.0 * math.log(rsq) / rsq)
      self.gset = v1 * fac
      return v2 * fac
    else :
      gset = self.gset
      self.gset = None
      return gset
    

class RouletteWheel :
  """Roulette wheel for evolutionary algorithms and similar purposes.
"""
  def __init__(self, rng, d = None) :
    if d is None :
      d = [1.0]
    self.set_wheel(d)
    self.rng = rng


  def gnuplot(self, fname) :
    f = open(fname, 'w')
    for w in self.wheel :
      f.write('%f\n' % w)


  def set_wheel(self, d) :
    x = 0.0
    for v in d :
      x = x + v
    self.wheel = [0.0]
    for v in d :
      self.wheel.append(self.wheel[-1] + v / x)


  def pocket(self) :
    x = self.rng.rnd()
    i = 1
    j = len(self.wheel)
    while i < j :
      k = (i + j) / 2
      # print x, self.wheel[k - 1], self.wheel[k], i, j, k
      if self.wheel[k - 1] <= x and x < self.wheel[k] :
        return k - 1
      elif x >= self.wheel[k] :
        i = k
      else :
        j = k
    raise ValueError('RouletteWheel::slot: bad value ' % x)


