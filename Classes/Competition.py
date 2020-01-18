class Competition:
    def event_group(self, eventid, index, g_size = 16):
        # Extracts persons competing in eventid
        competing = [i for i in self.competitors if eventid in i.events]
        random.shuffle(competing) # Randomized groups

        N = len(competing) # Number of competitors in event
        num_g = int(np.round(N / float(g_size))) # Number of groups

        count = 0
        for pers in competing:
            if eventid in ['333fm', '333mbf', '444bf', '555bf']: # 1 group for long events
                pers.groups[index] = '1'
                count += 1
            else:
                pers.groups[index] = str(int(count * num_g / N) + 1) # Record group
                count += 1

    def group(self):
        for i in range(len(self.events)):
            self.event_group(self.events[i], i)

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

    def write_tex_groups(self, f_name = None):
        if f_name == None:
            f_name = self.id + '-Groups.tex'
        self.competitors.sort(key = lambda i: i.name) # Sort by name
        f = open(f_name, 'w')
        for pers in self.competitors:
            f.write('\\groups{%s}{' % (pers.name))
            for i in range(len(self.events)):
                f.write('%s & %s \\\\ ' % (event_dict[self.events[i]][0], pers.groups[i]))
            f.write('}% \n')
        f.close()

    def write_wca_groups(self, f_name = None):
        if f_name == None:
            f_name = self.id + '-WCA.md'
        self.competitors.sort(key = lambda i: i.name) # Sort by name
        f = open(f_name, 'w')
        # Header
        f.write('| Name |')
        for i in self.events:
            f.write(' %s |' % (event_dict[i][1]))
        f.write('\n|' + ' --- |' * (1 + len(self.events)) + '\n')
        # Groups
        for pers in self.competitors:
            f.write('| %s |' % (pers.name))
            for i in range(len(self.events)):
                f.write(' %s |' % (pers.groups[i]))
            f.write('\n')
        f.close()

    @staticmethod
    def centi2min(centi):
        '''Converts a time in centiseconds to minute:second format'''
        minute = int(np.floor(centi / 6000)) # Compute number of minutes
        sec = int(np.ceil((centi - 6000 * minute) / 100)) # Compute remainder
        return str(minute) + ':' + str(sec).zfill(2) # Format string (zfill zero pads)

    @staticmethod
    def build_events(WCIF):
        '''Build a list of events held at the competition'''
        lst = [None] * len(WCIF['events'])
        for i in range(len(WCIF['events'])):
            lst[i] = WCIF['events'][i]['id']
        return lst

    @staticmethod
    def build_cutoffs(WCIF):
        '''Build a list of cutoffs for the competition. Note: Assumes cutoffs only in the first round'''
        lst = [None] * len(WCIF['events'])
        for i in range(len(WCIF['events'])):
            if WCIF['events'][i]['rounds'][0]['cutoff'] == None:
                lst[i] = ''
            else:
                lst[i] = Competition.centi2min(WCIF['events'][i]['rounds'][0]['cutoff']['attemptResult'])
        return lst

    @staticmethod
    def build_limits(WCIF):
        '''Build a list of time limits for the competition'''
        lst = [None] * len(WCIF['events'])
        for i in range(len(WCIF['events'])):
            if WCIF['events'][i]['rounds'][0]['cutoff'] == None:
                lst[i] = ''
            else:
                lst[i] = Competition.centi2min(WCIF['events'][i]['rounds'][0]['timeLimit']['centiseconds'])
        return lst

    @staticmethod
    def build_rounds(WCIF):
        '''Build a list of additional rounds for the competition'''
        lst = [[] for i in range(len(WCIF['events']))]
        for i in range(len(WCIF['events'])):
            if WCIF['events'][i]['rounds'][0]['advancementCondition'] != None:
                for j in range(len(WCIF['events'][i]['rounds']) - 1):
                    lst[i].append(WCIF['events'][i]['rounds'][j]['advancementCondition']['level'])
        return lst



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
                    f.write('{%s}{%s}{%s}{%s}{1}{%s}%%\n' % (pers.name, str(pers.id), event_dict[event][0], self.cutoffs[count], pers.groups[count]))
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
                        f.write('{}{}{%s}{}{%s}{}%%\n' % (event_dict[event][0], str(i + 2)))
                    f.write('\pagereset\n')
                count += 1

        # Blank cards
        for i in range(num_blank):
            f.write('\\scorecard{}{}{}{}{}{}%\n')
        f.write('\pagereset\n')

        f.close()

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

    def __init__(self, WCIF):
        '''Competition constructor'''
        self.name = WCIF['name']
        self.id = WCIF['id']
        self.events = self.build_events(WCIF)
        self.cutoffs = self.build_cutoffs(WCIF)
        self.limits = self.build_limits(WCIF)
        self.rounds = self.build_rounds(WCIF)
        self.competitors = Person.build_persons(WCIF)
