from .base import *
from .itertools import *
from .misc import *

# get everything from these libraries
from toolz.itertoolz import *
from toolz.functoolz import *
from toolz.dicttoolz import *

from fn import _, F
# for interactive notebook _ means last evaluation
# so i give an alias here
# different aliases
it_ = x_ = _
