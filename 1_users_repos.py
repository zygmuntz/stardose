'get starred repos for a given user'

import sys
#import codecs
import cPickle as pickle
from github_utils import *
from settings import *

try:
	output_file = sys.argv[1]
except IndexError:
	output_file = '{}.pkl'.format( user )
	
starred = get_all_starred( user )

f = open( output_file, 'wb' )
pickle.dump( starred, f )

"""		
f = codecs.open( output_file, "wb", "utf-8" )
f.write( starred )
"""
