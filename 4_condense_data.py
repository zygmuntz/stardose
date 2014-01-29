'condense data from users/ into a one file'

import sys
import os
import codecs
import cPickle as pickle
from glob import glob
from pprint import pprint
from github_utils import *
from settings import *

try:
	output_file = sys.argv[1]
except IndexError:
	output_file = 'condensed_users_and_repos.pkl'	

input_files = glob( users_dir + '/*.pkl' )
input_files.sort()

errors = []
users = {}	# user_name: repo_names
repos = {}	# repo_name: data   ( repos for all users )
counter = 0

for f in input_files:
	counter += 1

	try:
		data = pickle.load( open( f, 'rb' ))
	except:
		print "*** couldn't load ***\n"
		errors.append( f )
		continue
		
	file_name = os.path.basename( f )	
	user_name = file_name.split( '.' )[0]
	print user_name		
	
	user_repos = {}	
	for r in data:
		
		repos[r] = data[r]
		user_repos[r] = True		# dictionary for fast searching
		
	users[user_name] = user_repos
	
	# tmp saves
	if counter % 5000 == 0:
		print "saving to {}...".format( output_file )
		pickle.dump( { 'users': users, 'repos': repos }, open( output_file, 'wb' ))
	
if errors:	
	print "\nFiles with errors:"
	for f in errors:
		print f
	
print "saving to {}...".format( output_file )

pickle.dump( { 'users': users, 'repos': repos }, open( output_file, 'wb' ))


