"get actual recommendations"
"tweak below"

import sys
import codecs
import cPickle as pickle
from collections import defaultdict
from math import log1p, sqrt
from github_utils import *
from settings import *

# TODO: move to settings
input_file = 'condensed_users_and_repos.pkl'
similiarity_file = 'similiarity.pkl'
target_file = '{}.pkl'.format( user )
output_file = 'recommendations.txt'

print "loading data..."

data = pickle.load( open( input_file ))
similiarity = pickle.load( open( similiarity_file ))
target_starred = get_target_starred( target_file )

###

# TODO: move to settings
threshold = 1
user_weights = get_weights( similiarity, threshold )


popularity = defaultdict( float )

for u in data['users']:
	weight = user_weights[u]
	for r in data['users'][u]:
		popularity[r] += weight
		
# remove already starred repos
popularity = { x: popularity[x] for x in popularity if x not in target_starred }


##########################
### LOOK AND EDIT HERE ###
##########################

# if you want to select only less popular repos...
# popularity = { x: popularity[x] for x in popularity if data['repos'][x]['stargazers_count'] < 200 }

# downplay popular repos
# sqrt seems to work well
# need to add + k, +1 is too little (repos with 1 star showing high)
popularity = { x: popularity[x] / ( sqrt( data['repos'][x]['stargazers_count'] + 10 )) for x in popularity if x not in target_starred }
		
most_popular = sorted( popularity, key = popularity.get, reverse = True )		

o_f = codecs.open( output_file, "wb", "utf-8" )

# when 'ascii' codec can't encode character (...) in description,
# omit description when writing
for r in most_popular[:3000]:
	try:
		line = "github.com/{}\nscore: {}\t stars:{}\n{}\n\n".format( r, popularity[r], data['repos'][r]['stargazers_count'], data['repos'][r]['description'] )
		o_f.write( line )
	except Exception, e:
		#print e
		print "omitted description of {}".format( r )
		line = "github.com/{}\nscore: {}\t stars:{}\n\n".format( r, popularity[r], data['repos'][r]['stargazers_count'] )		
		o_f.write( line )
		
