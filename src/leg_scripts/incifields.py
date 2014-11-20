class crossing:
    #TODO Add other crossing fields
    def __init__(self, crossing_id):
        self.crossing_id = crossing_id
        self.incilist = []

    def add_incident(self, incident):
        incilist.append(incident)

    def get_cross(record):
        return crossing(record.crossing)


class incifields:
    def __init__(self, date, driver, driverbeh, casualities, narrative):
        self.date = date
        self.driver = driver
        self.driverbeh = driverbeh
        self.casualities = casualities
        self.narrative = narrative

    def get_date(record):
        return record.effdate

    def get_driver(record):
        return None

    def get_driver_beh(record):
        return None

    def get_cas(record):
        return None

    def get_narr(record):
        return None

class driver:
    def __init__(self, age, gender):
        self.age = age
        self.gender = gender

#The technical meaning of these fields can be found in the 
#attached documentation
class driverbeh:
    def __init__(self, f40, f41, f42, f43):
        self.f40 = f40
        self.f41 = f41
        self.f42 = f42
        self.f43 = f43

class casualities:
    def __init__(self, f44, f45, f46, f47, f48, f49, f50, f51, f52):
        self.f44 = f44
        self.f45 = f45
        self.f46 = f46
        self.f47 = f47
        self.f48 = f48
        self.f49 = f49
        self.f50 = f50
        self.f51 = f51
        self.f52 = f52
