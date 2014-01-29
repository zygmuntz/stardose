'basic building blocks for the system'

import requests as reqs
import re
import cPickle as pickle
import os
from settings import *

def get_all_starred( user ):
	starred, links, remaining_queries = get_starred( user )
	while True:
		if not links:
			break

		try:
			next_url = links['next']	
		except KeyError:
			break

		page, links, remaining_queries = get_starred( user, next_url )
		starred.extend( page )

	print "Total: {}, remaining queries: {}".format( len( starred ), remaining_queries )
	return starred


'return a page of starred repos'
def get_starred( user, url = None, format = 'json' ):
	
	global auth
	
	if not url:
		url = "https://api.github.com/users/{}/starred?per_page=100".format( user )
		
	print url
	r = reqs.get( url, auth = auth )
	
	ret_links = {}
	try: 
		ret_links = get_links( r.headers['link'] )
	except KeyError:
		pass
		
	remaining_queries = int( r.headers['x-ratelimit-remaining'] )	
		
	if format == 'text':
		return ( r.text, ret_links, remaining_queries )
	else:
		return ( r.json(), ret_links, remaining_queries )
	
	
###	
	
'call get_gazers as many times as needed'	
def get_all_gazers( repo ):
	gazers, links, remaining_queries = get_gazers( repo )
	while True:
		if not links:
			break

		try:
			next_url = links['next']	
		except KeyError:
			break

		page, links, remaining_queries = get_gazers( repo, next_url )
		gazers.extend( page )

	print "Total: {}, remaining queries: {}".format( len( gazers ), remaining_queries )
	return gazers
	
	
'return a page of users who starred a given repo in text format'
def get_gazers( repo, url = None ):	

	global auth
	
	if not url:
		url = "https://api.github.com/repos/{}/stargazers?per_page=100".format( repo )
	
	print url
	r = reqs.get( url, auth = auth )
	
	ret_links = {}
	try: 
		ret_links = get_links( r.headers['link'] )
	except KeyError:
		pass
		
	remaining_queries = int( r.headers['x-ratelimit-remaining'] )
		
	return ( r.json(), ret_links, remaining_queries )
	
	
'parse pagination links returned by github'
def get_links( link_header ):

	ret_links = {}

	links = link_header.split( ', ' )
	for link in links:
		match_href = re.match( '<(.+?)>', link )
		href = match_href.group( 1 )

		match_rel = re.search( 'rel="(.+?)"', link );
		rel = match_rel.group( 1 )

		ret_links[rel] = href		
		
	return ret_links
	
# save a repo's gazers
def save_repo( repo, gazers ):
	global repos_dir
	repo = get_saveable_repo_name( repo )
	output_file = '{}/{}.pkl'.format( repos_dir, repo )
	f = open( output_file, 'wb' )
	pickle.dump( gazers, f )
	
def get_saveable_repo_name( repo ):
	a, r = repo.split( '/' )
	return a + '_' + r
	
# save a user's starred repos
def save_gazer( gazer, starred ):
	global users_dir
	
	# save only some selected data for each repo
	repos = {}
	for r in starred:
	
		# ignore user's own repos
		try:
			if r['owner']['login'] == gazer:
				continue
		except Exception, e:
			print e
			pprint( r )
			continue	
	
		repo_name = r['full_name']
		repo_data = { x: r[x] for x in ( 'id', 'description', 'stargazers_count', 'watchers' ) }
		repos[repo_name] = repo_data	
		
		
	
	output_file = '{}/{}.pkl'.format( users_dir, gazer )
	f = open( output_file, 'wb' )
	pickle.dump( repos, f )
	
# check if there's starred data for a given user
def data_available_for( gazer ):
	global users_dir
	
	target_file = '{}/{}.pkl'.format( users_dir, gazer )
	if os.path.isfile( target_file ):
		return True	
	
	"""
	try:
		open( target_file, 'rb' )
		return True
	except:
		return False
	"""
		
# check if there's data for a given repo
def repo_data_available( repo ):
	global repos_dir
	
	repo = get_saveable_repo_name( repo )
	target_file = '{}/{}.pkl'.format( repos_dir, repo )
	if os.path.isfile( target_file ):
		return True
	
def get_target_starred( input_file ):
	data = pickle.load( open( input_file, 'rb' ))
	target_starred = {}
	for r in data:
		full_name = r['full_name']
		target_starred[full_name] = True
	return target_starred
	
def get_weights( similiarity, threshold = 2 ):
	weights = {}
	user_star_counts = similiarity['user_star_counts']
	user_stars_in_common = similiarity['user_stars_in_common']
	
	for u in user_star_counts:
	
		stars_in_common = user_stars_in_common[u]
		if stars_in_common < threshold:
			weights[u] = 0.0
			continue
			
		try:
			weights[u] = 1.0 * stars_in_common / user_star_counts[u]
		except ZeroDivisionError:
			weights[u] = 0.0
			
	return weights	