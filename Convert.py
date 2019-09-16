import numpy as np
import pandas as pd

# Create groups for one event
def group(df, g_size = 16):
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

# Dictionary to translate event ID to event name
event_dict = {
	'222': '2$\\times$2 Cube',
	'333': '3$\\times$3 Cube',
	'444': '4$\\times$4 Cube',
	'555': '5$\\times$5 Cube',
	'666': '6$\\times$6 Cube',
	'777': '7$\\times$7 Cube',
	'333bf': '3$\\times$3 Blindfolded',
	'333oh': '3$\\times$3 One-Handed',
	'333fm': '3$\\times$3 Fewest Moves',
	'333mbf': '3$\\times$3 Multi-Blindfolded',
	'333ft': '3$\\times$3 with Feet',
	'minx': 'Megaminx',
	'clock': 'Clock',
	'pyram': 'Pyraminx',
	'skewb': 'Skewb',
	'sq1': 'Square-1',
	'444bf': '4$\\times$4 Blindfolded',
	'555bf': '5$\\times$5 Blindfolded'
}

# Registration file
comp = 'Comp2019-registration.csv'

# Read data into a Pandas DataFrame
data = pd.read_csv(comp, delimiter = ',', keep_default_na = False)

# Save a copy of the DataFrame sorted by name
s_data = data.sort_values(by = ['Name'])

# Write the data for the name tags formatted for the scorecard class
np.savetxt(r'NameTags.tex', (r'\nametag{' + s_data['Name'].map(str) + '}{COMPETITOR}{' + s_data['WCA ID'] + '}%').values, fmt = '%s')

# String array for LaTeX code for groups
tex_groups = np.empty(len(data))
tex_groups = np.array(r'\groups{' + s_data['Name'].map(str) + '}{')

# Iterate through columns of registration file to calculate groups for each event
for i in list(data)[6:-3]:
	# Calculate groups for the event and append to the string array
	tex_groups += (event_dict[i] + ' & ' + group(s_data[['Name', i]])['Group'].map(str) + ' \\\ ').values
tex_groups += '}%' # Close the bracket in the string array

# Write groups to tex file
np.savetxt(r'Groups.tex', tex_groups, fmt = '%s')


#% \scorecard[EVENT FLAG (any nonempty string will create a score card with only three times)]{NAME}{CUBECOMPS ID}{EVENT}{CUTOFF}{ROUND}{GROUP}%
#\scorecard{Brady Metherall}{45}{5$\times$5$\times$5}{2:00}{1}{3}%
