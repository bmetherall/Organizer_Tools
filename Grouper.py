from __future__ import print_function
import numpy as np
import pandas as pd
import sys
import requests

def get_ans():
	'''Asks user for input. If the user types yes true is returned'''
	ans = input()
	if ans.lower == 'y' or ans.lower == 'yes' or ans == '1':
		return True
	else:
		return False

def get_wcif(comp):
	'''Pulls WCIF from WCA and return json object. If there is a problem with the request the program terminates'''
	print('Attempting to pull competition info...')
	# Send GET request for WCIF
	WCIF = requests.get('https://www.worldcubeassociation.org/api/v0/competitions/' + comp + '/wcif/public')
	# If response code is 200 everything good, otherwise something bad
	if WCIF.status_code == 200:
		print('Success!')
		return WCIF = WCIF.json()
	else:
		print('Response Error!')
		exit()

# Get comp name from user
print('Enter competition ID:')
#comp = input()
comp = 'Cubinginthe6ix2019'
#comp_file = comp + '-registration.csv'


WCIF = get_wcif(comp)





print('Would you like to create nametags? (y/n)')
if get_ans():
	print('yes')
	# make nametags

print('Would you like to create groups? (y/n)')
if get_ans():
	print('yes')
	# make groups

print('Would you like to create scorecards? (y/n)')
if get_ans():
	print('yes')
	# make scorecards




# # Read data into a Pandas DataFrame
# data = pd.read_csv(comp_file, delimiter = ',', keep_default_na = False)
#
# # Save a copy of the DataFrame sorted by name
# s_data = data.sort_values(by = ['Name']).copy()
# s_data.reset_index(inplace = True)
#
# print('Creating name tags...')
# write_nametags(s_data)
# print('Done!\n')
#
# print('Creating groups...')
# group_df = make_groups(s_data)
# write_groups(group_df)
# print('Done!\n')
#
# print('Creating scorecards...')
# wca_df = pd.read_html('https://www.worldcubeassociation.org/competitions/' + comp + '#competition-events', keep_default_na = False)[1]
# write_scorecards(group_df, get_cutoffs(wca_df), get_rounds(wca_df))
# print('Done!')
