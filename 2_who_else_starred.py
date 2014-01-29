'given starred repos for the target user, get other gazers for these repos'
'save to repos/<repo>.pkl'

import sys
#import codecs
import cPickle as pickle
from github_utils import *
from settings import *

try:
	input_file = sys.argv[1]
except IndexError:
	input_file = '{}.pkl'.format( user )

starred = pickle.load( open( input_file, 'rb' ))

for r in starred:
	full_name = r['full_name']
	print full_name
	
	if repo_data_available( full_name ):
		continue
	
	gazers = get_all_gazers( full_name )
	save_repo( full_name, gazers )
	print
	

