import csv
import dbf
from incident import Incident

tableSet = []

def main():

    table = dbf.Table('../gcispubl.DBF')
    

    for record in table:
        print record.state
        print record.citycd

#    for record in table:
 #       obj = Incident(record.effdate, record.crossing, record.ttstn, record.nearest, record.cntycd, record.state, record.latitude, record.longitud)
  #      tableSet.append(obj)
        
    print 'Table Read...'
   # printJson('example.json', tableSet)



def printJson(filename, t_set):
    print 'Printing JSON File...'

    to_write = open(filename, 'w')

    #Write the JSON Header
    to_write.write("{\n")
    to_write.write("\"coords\":\n")
    to_write.write("\t[\n")
    

    #Write the data Objects
    for incident in t_set:
        print 'Printing Object in t_set'
        to_write.write("{\"lat\":")
        to_write.write(str(incident.lat_c)[:2] + '.' + str(incident.lat_c)[2:6])
        if(str(incident.lat_c)[0] == '0'):
            to_write.write('0')


        to_write.write(", \"long\":")

        #A Hack so we get the first 3 digits if the number is greater
        #than 100, but only the first 2 if it is less then 100
        #We also need to account for the - sign
        val = 3
        if(len(str(incident.long_c)) > 1 and str(incident.long_c)[1] == '1'):
            val = 4

        to_write.write(str(incident.long_c)[:val] + '.' + str(incident.long_c)[2:6])

        if(str(incident.long_c)[0] == '0'):
            to_write.write('0')


        to_write.write("},\n")


    #Write the JSON Footer
    to_write.write("\t]\n")
    to_write.write("}\n")

    to_write.close()

if __name__ == "__main__":
    main()
