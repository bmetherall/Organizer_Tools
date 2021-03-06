import numpy
import random
import Classes.Person

class Competition:
	####################
	# Event Dictionary #
	####################

	# First element: LaTeX. Second element: plain text.
	event_dict = {
		'222': ['2$\\times$2$\\times$2 Cube', '2x2x2 Cube'],
		'333': ['3$\\times$3$\\times$3 Cube', '3x3x3 Cube'],
		'444': ['4$\\times$4$\\times$4 Cube', '4x4x4 Cube'],
		'555': ['5$\\times$5$\\times$5 Cube', '5x5x5 Cube'],
		'666': ['6$\\times$6$\\times$6 Cube', '6x6x6 Cube'],
		'777': ['7$\\times$7$\\times$7 Cube', '7x7x7 Cube'],
		'333bf': ['3$\\times$3$\\times$3 Blindfolded', '3x3x3 Blindfolded'],
		'333oh': ['3$\\times$3$\\times$3 One-Handed', '3x3x3 One-Handed'],
		'333fm': ['3$\\times$3$\\times$3 Fewest Moves', '3x3x3 Fewest Moves'],
		'333mbf': ['3$\\times$3$\\times$3 Multi-Blindfolded', '3x3x3 Multi-Blindfolded'],
		'minx': ['Megaminx', 'Megaminx'],
		'clock': ['Clock', 'Clock'],
		'pyram': ['Pyraminx', 'Pyraminx'],
		'skewb': ['Skewb', 'Skewb'],
		'sq1': ['Square-1', 'Square-1'],
		'444bf': ['4$\\times$4$\\times$4 Blindfolded', '4x4x4 Blindfolded'],
		'555bf': ['5$\\times$5$\\times$5 Blindfolded', '5x5x5 Blindfolded']
	}

	#############
	# Name Tags #
	#############
	def write_nametags(self, f_name = None, num_blank = 0):
		if f_name == None:
			f_name = self.id + '-Tags.tex'
		self.competitors.sort(key=lambda i: i.name) # Sort by name
		f = open(f_name, 'w')
		for pers in self.competitors:
			f.write('\\nametag{%s}{%s}{%s}%%\n' % (pers.name, pers.role.upper(), pers.wcaid))
		for i in range(num_blank): # Include blank nametags for day-of registrations
			f.write('\\nametag{}{COMPETITOR}{}%\n')
		f.close()

	##########
	# Groups #
	##########
	def event_group(self, eventid, index, g_size = 16, choose_size = False):
		if choose_size:
			print('Enter target group size for ' + self.event_dict[eventid][1] + ':')
			g_size = int(input())

		# Extracts persons competing in eventid
		competing = [i for i in self.competitors if eventid in i.events]
		random.shuffle(competing) # Randomized groups

		N = len(competing) # Number of competitors in event
		num_g = int(numpy.round(N / float(g_size))) # Number of groups

		count = 0
		for pers in competing:
			if eventid in ['333fm', '333mbf', '444bf', '555bf']: # 1 group for long events
				pers.groups[index] = '1'
				count += 1
			else:
				pers.groups[index] = str(int(count * num_g / N) + 1) # Record group
				count += 1

	def group(self, choose_size = False):
		for i in range(len(self.events)):
			self.event_group(self.events[i], i, choose_size = choose_size)

	def write_tex_groups(self, f_name = None):
		if f_name == None:
			f_name = self.id + '-Groups.tex'
		self.competitors.sort(key = lambda i: i.name) # Sort by name
		f = open(f_name, 'w')
		for pers in self.competitors:
			f.write('\\groups{%s}{' % (pers.name))
			for i in range(len(self.events)):
				f.write('%s & %s \\\\ ' % (self.event_dict[self.events[i]][0], pers.groups[i]))
			f.write('}% \n')
		f.close()

	def write_csv_groups(self, f_name = None):
		if f_name == None:
			f_name = self.id + '-Groups.csv'
		self.competitors.sort(key = lambda i: i.name) # Sort by name
		f = open(f_name, 'w')
		for pers in self.competitors:
			f.write(pers.name)
			for i in range(len(self.events)):
				f.write(',%s' % (pers.groups[i]))
			f.write('\n')
		f.close()

	def write_wca_groups(self, f_name = None):
		if f_name == None:
			f_name = self.id + '-WCA.md'
		self.competitors.sort(key = lambda i: i.name) # Sort by name
		f = open(f_name, 'w')
		# Header
		f.write('| Name |')
		for i in self.events:
			f.write(' %s |' % (self.event_dict[i][1]))
		f.write('\n|' + ' --- |' * (1 + len(self.events)) + '\n')
		# Groups
		for pers in self.competitors:
			f.write('| %s |' % (pers.name))
			for i in range(len(self.events)):
				f.write(' %s |' % (pers.groups[i]))
			f.write('\n')
		f.close()

	##############
	# Scorecards #
	##############
	def write_scorecards(self, f_name = None, num_blank = 0):
		if f_name == None:
			f_name = self.id + '-Cards.tex'
		f = open(f_name, 'w')

		# First round cards
		count = 0
		for event in self.events:
			if event != '333fm':
				self.competitors.sort(key = lambda i: (i.groups[count], i.name)) # Sort by group then by name
				for pers in [i for i in self.competitors if event in i.events]:
					if event in ['666', '777', '333bf', '333mbf', '444bf', '555bf']:
						f.write('\scorecard[1]')
					else:
						f.write('\scorecard')
					f.write('{%s}{%s}{%s}{%s}{1}{%s}%%\n' % (pers.name, str(pers.id), self.event_dict[event][0], self.cutoffs[count], pers.groups[count]))
			count += 1
			f.write('\pagereset\n')

		# Subsequent round cards
		count = 0
		for event in self.events:
			if event != '333fm':
				for i in range(len(self.rounds[count])): # Round number
					for j in range(self.rounds[count][i]): # card number
						if event in ['666', '777', '333bf', '333mbf', '444bf', '555bf']:
							f.write('\scorecard[1]')
						else:
							f.write('\scorecard')
						f.write('{}{}{%s}{}{%s}{}%%\n' % (self.event_dict[event][0], str(i + 2)))
					f.write('\pagereset\n')
				count += 1

		# Blank cards
		for i in range(num_blank):
			f.write('\\scorecard{}{}{}{}{}{}%\n')
		f.write('\pagereset\n')

		f.close()

	#######
	# TeX #
	#######
	def write_tex(self, f_name = None, url = '', flag = [0, 0, 0]):
		if f_name == None:
			f_name = self.id + '.tex'
		f = open(f_name, 'w')

		f.write('\documentclass[fast]{scorecard}\n\n\comp{%s}\n\\url{%s}\n' % (self.name, url))
		f.write('\events{')
		for event in self.events:
			f.write('\img{./Icons/%s} ' % (event))
		f.write('}\n\n')

		f.write('\\begin{document}\n\sffamily\n\centering\n\n')

		if flag[0]:
			f.write('\input{%s-Tags}\n\pagereset\n\n' % (self.id))
		if flag[1]:
			f.write('\input{%s-Groups}\n\pagereset\n\n' % (self.id))
		if flag[2]:
			f.write('\\newgeometry{margin=0in}\n\crosssize{0mm}\n\n')
			f.write('\input{%s-Cards}\n\pagereset\n\n' % (self.id))

		f.write('\end{document}')
		f.close()

	#############
	# Functions #
	#############
	@staticmethod
	def centi2min(centi):
		'''Converts a time in centiseconds to minute:second format'''
		minute = int(numpy.floor(centi / 6000)) # Compute number of minutes
		sec = int(numpy.ceil((centi - 6000 * minute) / 100)) # Compute remainder
		return str(minute) + ':' + str(sec).zfill(2) # Format string (zfill zero pads)

	###########
	# Getters #
	###########
	@staticmethod
	def get_events(WCIF):
		'''Build a list of events held at the competition'''
		lst = [None] * len(WCIF['events'])
		for i in range(len(WCIF['events'])):
			lst[i] = WCIF['events'][i]['id']
		return lst

	@staticmethod
	def get_cutoffs(WCIF):
		'''Build a list of cutoffs for the competition. Note: Assumes cutoffs only in the first round'''
		lst = [None] * len(WCIF['events'])
		for i in range(len(WCIF['events'])):
			if WCIF['events'][i]['rounds'][0]['cutoff'] == None:
				lst[i] = ''
			else:
				lst[i] = Competition.centi2min(WCIF['events'][i]['rounds'][0]['cutoff']['attemptResult'])
		return lst

	@staticmethod
	def get_limits(WCIF):
		'''Build a list of time limits for the competition'''
		lst = [None] * len(WCIF['events'])
		for i in range(len(WCIF['events'])):
			if WCIF['events'][i]['rounds'][0]['cutoff'] == None:
				lst[i] = ''
			else:
				lst[i] = Competition.centi2min(WCIF['events'][i]['rounds'][0]['timeLimit']['centiseconds'])
		return lst

	@staticmethod
	def get_rounds(WCIF):
		'''Build a list of additional rounds for the competition'''
		lst = [[] for i in range(len(WCIF['events']))]
		for i in range(len(WCIF['events'])):
			if WCIF['events'][i]['rounds'][0]['advancementCondition'] != None:
				for j in range(len(WCIF['events'][i]['rounds']) - 1):
					lst[i].append(WCIF['events'][i]['rounds'][j]['advancementCondition']['level'])
		return lst

	########
	# init #
	########
	def __init__(self, WCIF):
		'''Competition constructor'''
		self.name = WCIF['name']
		self.id = WCIF['id']
		self.events = self.get_events(WCIF)
		self.cutoffs = self.get_cutoffs(WCIF)
		self.limits = self.get_limits(WCIF)
		self.rounds = self.get_rounds(WCIF)
		self.competitors = Classes.Person.Person.get_persons(WCIF)
