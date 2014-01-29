'try to load each pickle file in the users dir, finally output names of those with errors'

import sys
import cPickle as pickle
from glob import glob
from github_utils import *
from settings import *

input_files = glob( users_dir + '*.pkl' )
input_files.sort()

errors = []

for f in input_files: 
	print f
	
	try:
		data = pickle.load( open( f, 'rb' ))
	except:
		print "*** error ***\n"
		errors.append( f )
		
print "\nFiles with errors:"
for f in errors:
	print f
	


