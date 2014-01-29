"get gazers' data for repos in a given dir"
"specifically, what other repos each user has starred"
'save to users/<user>.pkl'

"this script takes a while to download data from GitHub. It can be stopped and re-run, it will resume."

import sys
import codecs
import cPickle as pickle
from glob import glob
from github_utils import *
from settings import *

repo_files = glob( repos_dir + '/*.pkl' )
repo_counter = 0
repos_count = len( repo_files )

for f in repo_files: 
	print "{} ({}/{})".format( f, repo_counter, repos_count )
	print

	repo_counter += 1

	gazers = pickle.load( open( f, 'rb' ))
	gazers_count = len( gazers )
	counter = 0
	
	for g in gazers:
		counter += 1
		gazer = g['login']
		
		# skip already downloaded
		if data_available_for( gazer ):
			continue
			
		print "{} ({}/{})".format( gazer, counter, gazers_count )
		starred = get_all_starred( gazer )
		save_gazer( gazer, starred )
		
	print

