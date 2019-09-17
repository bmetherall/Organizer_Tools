import numpy as np
import pandas as pd

def write_nametags(df, f_name = 'NameTags.tex'):
	# Write the data for the name tags formatted for the scorecard class
	np.savetxt(f_name, (r'\nametag{' + df['Name'].map(str) + '}{COMPETITOR}{' + df['WCA ID'] + '}%').values, fmt = '%s')

def write_groups(df, tex_f = 'Groups.tex', wca_f = 'Groups.md', csv_f = 'Groups.csv'):
	# String array for LaTeX code and WCA website for groups
	tex_groups = np.array(r'\groups{' + df['Name'].map(str) + '}{')
	wca_groups = np.array(df['Name'].map(str) + ' |')
	wca_header = np.array(['Name |', ' --- |'])
	for i in list(df)[2:]:
		tex_groups += event_dict[i][0] + ' & ' + df[i].map(str) + ' \\\ '
		wca_groups += ' ' + df[i].map(str) + ' |'
		#wca_header += np.array([' ' + event_dict[i][1] + ' |', ' :---: |'])
		wca_header = np.core.defchararray.add(wca_header, [' ' + event_dict[i][1] + ' |', ' :---: |']) # There's got to be an easier way
	tex_groups += '}%' # Close the bracket in the string array
	# Write groups to files
	np.savetxt(tex_f, tex_groups, fmt = '%s')
	np.savetxt(wca_f, np.hstack((wca_header, wca_groups)), fmt = '%s')
	df.to_csv(csv_f, index = False)

# Create groups for one event
def event_group(df, g_size = 16):
	# df should be two columns, Name and an eventID
	df_old = df
	df = df[df.iloc[:, 1] == 1] # Extract only competitors in event
	df = df.sample(frac = 1) # Randomize groups
	n = len(df) # Number of competitors in event
	num_g = int(np.round(n / float(g_size))) # Number of groups
	if list(df)[1] in ['333fm', '333mbf', '444bf', '555bf']:
		# For long events, only 1 group
		group = np.ones(n).astype(int)
	else:
		group = np.arange(n) * num_g / n + 1
	df['Group'] = group.astype(str) # Append column formatted as a string
	return df_old.merge(df, how = 'left').fillna('') # Return merged groups with old DataFrame, filling blanks with an empty string

def make_groups(df):
	group_df = df[['index', 'Name']].copy()
	# Iterate through columns of registration file to calculate groups for each event
	for i in list(df)[7:-3]:
		g_num = event_group(df[['Name', i]])['Group'].map(str)
		group_df[i] = g_num
	return group_df

def clean_cutoff(ds):
	ds = ds.str.replace('1 attempt to get < ', '')
	ds = ds.str.replace('2 attempts to get < ', '')
	ds = ds.str.replace('\.00', '')
	return ds

def get_cutoffs(df):
	cutoffs = df[['Event', 'Cutoff']].copy()
	cutoffs.replace('', np.nan, inplace = True)
	cutoffs.dropna(how = 'all', inplace = True)
	cutoffs.replace(np.nan, '', inplace = True) # There's probably a better way for this too
	return np.array(clean_cutoff(cutoffs['Cutoff']))

def write_scorecards(df, cutoffs, f_name = 'Cards.tex'):
	f = open(f_name, 'wb')
	f.close()
	f = open(f_name, 'ab')
	count = 0
	for i in list(df)[2:]:
		if i != '333fm':
			curr_group = df[df.iloc[:, count + 2] != ''].copy()
			curr_group.sort_values(by = [i, 'Name'], inplace = True)
			if i in ['666', '777', '333bf', '333mbf', '444bf', '555bf']:
				cards = np.array(r'\scorecard[1]{' + curr_group['Name'].map(str) + '}{' + (curr_group['index'] + 1).map(str) + '}{' + event_dict[i][0] + '}{' + cutoffs[count] + '}{1}{' + curr_group[i] + '}%')
			else:
				cards = np.array(r'\scorecard{' + curr_group['Name'].map(str) + '}{' + (curr_group['index'] + 1).map(str) + '}{' + event_dict[i][0] + '}{' + cutoffs[count] + '}{1}{' + curr_group[i] + '}%')
			count += 1
			np.savetxt(f, cards, fmt = '%s')
			f.write('\pagereset\n')
	f.close()


	#% \scorecard[EVENT FLAG (any nonempty string will create a score card with only three times)]{NAME}{CUBECOMPS ID}{EVENT}{CUTOFF}{ROUND}{GROUP}%
	#\scorecard{Brady Metherall}{45}{5$\times$5$\times$5}{2:00}{1}{3}%

	#tex_groups = np.array(r'\groups{' + df['Name'].map(str) + '}{')
	#wca_groups = np.array(df['Name'].map(str) + ' |')
	#wca_header = np.array(['Name |', ' --- |'])
	#for i in list(df)[2:]:
	#	tex_groups += event_dict[i][0] + ' & ' + df[i].map(str) + ' \\\ '
	#	wca_groups += ' ' + df[i].map(str) + ' |'
	#	#wca_header += np.array([' ' + event_dict[i][1] + ' |', ' :---: |'])
	#	wca_header = np.core.defchararray.add(wca_header, [' ' + event_dict[i][1] + ' |', ' :---: |']) # There's got to be an easier way
	#tex_groups += '}%' # Close the bracket in the string array
	## Write groups to files
	#np.savetxt(tex_f, tex_groups, fmt = '%s')
	#np.savetxt(wca_f, np.hstack((wca_header, wca_groups)), fmt = '%s')
	#df.to_csv(csv_f, index = False)



# Dictionaries to translate event ID to event name
# First element: LaTeX. Second element: plain text.
event_dict = {
	'222': ['2$\\times$2 Cube', '2x2 Cube'],
	'333': ['3$\\times$3 Cube', '3x3 Cube'],
	'444': ['4$\\times$4 Cube', '4x4 Cube'],
	'555': ['5$\\times$5 Cube', '5x5 Cube'],
	'666': ['6$\\times$6 Cube', '6x6 Cube'],
	'777': ['7$\\times$7 Cube', '7x7 Cube'],
	'333bf': ['3$\\times$3 Blindfolded', '3x3 Blindfolded'],
	'333oh': ['3$\\times$3 One-Handed', '3x3 One-Handed'],
	'333fm': ['3$\\times$3 Fewest Moves', '3x3 Fewest Moves'],
	'333mbf': ['3$\\times$3 Multi-Blindfolded', '3x3 Multi-Blindfolded'],
	'333ft': ['3$\\times$3 with Feet', '3x3 with Feet'],
	'minx': ['Megaminx', 'Megaminx'],
	'clock': ['Clock', 'Clock'],
	'pyram': ['Pyraminx', 'Pyraminx'],
	'skewb': ['Skewb', 'Skewb'],
	'sq1': ['Square-1', 'Square-1'],
	'444bf': ['4$\\times$4 Blindfolded', '4x4 Blindfolded'],
	'555bf': ['5$\\times$5 Blindfolded', '5x5 Blindfolded']
}

# Registration file
comp = 'Comp2019-registration.csv'

# Read data into a Pandas DataFrame
data = pd.read_csv(comp, delimiter = ',', keep_default_na = False)

# Save a copy of the DataFrame sorted by name
s_data = data.sort_values(by = ['Name']).copy()
s_data.reset_index(inplace = True)

#write_nametags(s_data)
group_df = make_groups(s_data)
#write_groups(group_df)

wca_df = pd.read_html('https://www.worldcubeassociation.org/competitions/Cubinginthe6ix2019#competition-events', keep_default_na = False)[1]

write_scorecards(group_df, get_cutoffs(wca_df))


#% \scorecard[EVENT FLAG (any nonempty string will create a score card with only three times)]{NAME}{CUBECOMPS ID}{EVENT}{CUTOFF}{ROUND}{GROUP}%
#\scorecard{Brady Metherall}{45}{5$\times$5$\times$5}{2:00}{1}{3}%






















