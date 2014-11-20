import dbf
import csv
from data_structs import Crossing, Incident

import resource

def getTable():
    dbf = openDBFTable('../gcispubl.DBF')
    csv = openCSVTable('../MasterGradeCrossingFile.csv')

    mergedTable = mergeTables(dbf, csv)
    
    return mergedTable

def openDBFTable(dbfName):
    table = dbf.Table(dbfName)
    return table

def openCSVTable(csvName):
    f = open(csvName, 'rU')

    csvF = csv.reader(f, delimiter = ',', quotechar = '|')
    return csvF

#Returns an array (from a DBF file) of pairs in the form
#[KEY, POSSIBLE VALUE]
def getDBFValues(dbfT):
    ret_l = list()

    return ['foo', 'bar']

    for field_name in dbfT.field_names:
        print field_name
        for record in dbfT:
            if [field_name, record[field_name]] not in ret_l:
                ret_l.append([field_name, record[field_name]])

    return ret_l

#Returns an array (from a CSV file) of pairs in the form
#[KEY, POSSIBLE VALUE]
def getCSVValues(csvF):
    ret_l = list()

    key_list = getKeyList(csvF)

    i = 0
    for row in csvF:
        j = 0
        for field in row:
            if i % 2 == 1 and i > 0:
                if j < len(key_list):
                    ret_l.append([key_list[j], field])
            j += 1
        i += 1
    
    print ret_l
    return ret_l


def getKeyList(csvF):
    ret_l = list()
    for row in csvF:
        for field in row:
            ret_l.append(field)
        break

    return ret_l


def mergeTables(dbfT, csv):

    crossingls = dict()
    incils = list()

    #Iterate over rows of dbf
    for record in dbfT:
        cross = Crossing()
        cross.set_values(record)
        crossingls[record.crossing] = cross

    #Fill out the list of keys for the csv file
    keyls = getKeyList(csv)

    #For each row, create an incident object
    rowCount = 0
    for row in csv:
        if rowCount % 2 == 1 and rowCount > 0:

            inci = Incident()

            for y in xrange(0, len(keyls)):
                if y < len(row):
                    #print 'Adding key value ' + str(keyls[y]) + str(row[y])
                    inci.add_keyvalue(keyls[y], row[y])

            incils.append(inci)


        rowCount += 1

    #find the corresponding crossing in the crossing list
    #add incident to crossings' inci list
    for incident in incils:
        if incident.get_value('GXID') in crossingls:
            crs = crossingls[incident.get_value('GXID')]
            crsls = crs.get_inci()

            if crsls is not None:
                crsls.append(incident)
                
    return [crossingls, incils]

def createGraph(mergedTable):
    return None

def printJSON(graph):
    return None


getTable()
