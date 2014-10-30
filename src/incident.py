class Incident:
    def __init__(self, date, railroad, inum, station, county, state, lat_c, long_c):
        #Year incident occured
        self.date = date

        #Reporting railroad 
        self.railroad = railroad

        #Incident number
        self.inum = inum
        
        #Station of incident
        self.station = station

        #County of incident
        self.county = county

        #State of incident
        self.state = state

        #Latitude
        self.lat_c = lat_c

        #Longitude
        self.long_c = long_c
        
