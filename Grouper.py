import requests
import numpy as np
import random

import Classes.Person
import Classes.Competition

def get_ans():
	'''Asks user for input. If the user types 'yes', true is returned'''
	ans = input()
	if ans.lower() == 'y' or ans.lower() == 'yes' or ans.lower() == '1':
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
		return WCIF.json()
	else:
		print('Response Error!')
		exit()

# Get comp name from user
print('Enter competition ID:')
comp = input()
#comp = 'Cubinginthe6ix2019'
WCIF = get_wcif(comp)
comp = Classes.Competition.Competition(WCIF)

flag = [0, 0, 0]

print('Would you like to create name tags?')
if get_ans():
	comp.write_nametags()
	flag[0] = 1

print('Would you like to create groups?')
if get_ans():
	print('Would you like to use the default of 16 competitors per group?')
	comp.group(choose_size = not get_ans())
	comp.write_tex_groups()
	flag[1] = 1

	print('Would you like to export the groups for the WCA?')
	if get_ans():
		comp.write_wca_groups()

	print('Would you like to export the groups to a csv?')
	if get_ans():
		comp.write_csv_groups()

print('Would you like to create scorecards?')
if get_ans():
	comp.write_scorecards()
	flag[2] = 1

print('What is the URL of the live results? (If none, leave blank)')
url = input()

comp.write_tex(url = url, flag = flag)
