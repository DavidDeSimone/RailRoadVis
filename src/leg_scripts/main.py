import csv
import dbf
from incifields import *
from collections import OrderedDict

tableSet = []

def main():

    table = dbf.Table('../gcispubl.DBF')

    print table

    trackdict = dict()

    for record in table:
        if record.state in trackdict:
            trackdict[record.state] += 1
        else:
            trackdict[record.state] = 1


    ordered = OrderedDict(sorted(trackdict.items(), key=lambda t: t[1]))
    print ordered
    


    record1 = table[1]
    record2 = table[2]


    #for f in record1:
        #print f

        
   # createCompareJson(record1, record2)

   # crossing_set = set()
        
   # for record in table:

      #  cross = crossing.get_cross(record)

       # if cross not in crossing_set:
       #     crossing_set.add(cross)

      #  date = incifields.get_date(record)
     #   driver = incifields.get_driver(record)
    #    driverbeh = incifields.get_driver_beh(record)
   #     casualities = incifields.get_cas(record)
  #      narrative = incifields.get_narr(record)

 #       record_init = incifields(date, driver, driverbeh, casualities, narrative)

#        cross.add_incident(record_init)

        
    print 'Table Read...'
   #printJson('example.json', tableSet)



def createCompareJson(record1, record2):

    to_write = open('output.json', 'w')

    to_write.write('{\n')
    to_write.write('"nodes":\n')
    to_write.write('\t[\n')

    line = 0
    for f in record1:
        if f != '':
            to_write.write('{"name":"' + str(line) + '","value":"' + str(f) + '"},\n')
            line +=1 

    for f in record2:
        if f != '':
            to_write.write('{"name":"' + str(line) + '","value":"' + str(f) + '"},\n')
            line += 1


    to_write.write('],\n')
    to_write.write('"links":[\n')

    for x in xrange(0, len(record1)):
        if record1[x] != '' and record2[x] != '':
            if record1[x] == record2[x]:
                to_write.write('{"source":' + str(x) + ',"target":' + str(len(record1) + x) + ',"value":' + str(x) + '},\n') 

    to_write.write('\t]\n')
    to_write.write('}\n')


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
