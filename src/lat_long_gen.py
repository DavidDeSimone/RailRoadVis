import data_parser as dp 

BOUND = 5

def main():
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	dbfT.open()

	output = open('map_points.json', 'a')
	output.write('[')
	for x in xrange(0, len(dbfT)):
		record = dbfT[x]
		ID = record.crossing
		if ID in inci_dic:

			#Find the incident list for this crossing
			inci_ls = inci_dic[ID]
			num_incidents = len(inci_ls)

			if num_incidents > BOUND:
				lat_f = int(record.latitude)
				long_f = int(record.longitud)

				while(lat_f > 90 or lat_f < -90 ):
					lat_f /= 10

				while(long_f > 180 or long_f < -180):
					long_f /= 10

				output.write('[' + str(lat_f) + ',' + str(long_f) + ',"' + str(ID) + '(' + str(num_incidents) + ')' + '"]')
				if(x != len(dbfT) - 1):
					output.write(',')
			

	output.write(']')

if __name__=="__main__":
	main()
