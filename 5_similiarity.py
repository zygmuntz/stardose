"compute similiarity data between target user and the other users"

import cPickle as pickle
from github_utils import *
from settings import *

# TODO: move to settings
target_file = '{}.pkl'.format( user )
input_file = 'condensed_users_and_repos.pkl'
output_file = 'similiarity.pkl'

print "loading data..."

data = pickle.load( open( input_file ))
target_starred = get_target_starred( target_file )

print "{} target starred.".format( len( target_starred ))

user_star_counts = {}
user_stars_in_common = {}

for u in data['users']:
	user_star_counts[u] = len( data['users'][u] )

	repos_in_common = [ x for x in data['users'][u] if x in target_starred and not x.startswith( 'zygmuntz/' ) ]
	user_stars_in_common[u] = len( repos_in_common )
	
#print user_star_counts
#print user_stars_in_common	
	
pickle.dump( { 'user_star_counts': user_star_counts, 'user_stars_in_common': user_stars_in_common }, open( output_file, 'wb' ))
