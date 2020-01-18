class Person:
    def __init__(self, name, ID, events, wcaid, role, num_events):
        '''Person constructor'''
        self.name = name
        self.id = ID
        self.events = events
        self.wcaid = wcaid
        self.role = role
        self.groups = [''] * num_events
        
    @staticmethod
    def build_persons(WCIF):
        '''Builds an array of competitors from WCIF data'''
        lst = []
        i = 0 # Counter
        for pers in WCIF['persons']: # Loops over each person registered
            # Build competitors
            if pers['registration'] != None:
                if 'delegate' in pers['roles']:
                    role = 'delegate'
                elif 'organizer' in pers['roles']:
                    role = 'organizer'
                else:
                    role = 'competitor'
                lst.append(Person(pers['name'], pers['registrantId'], pers['registration']['eventIds'], pers['wcaId'], role, len(WCIF['events'])))
                if lst[i].wcaid == None:
                    lst[i].wcaid = ''
                i += 1
        return lst
