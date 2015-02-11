import dbf
import csv
import os
from xlrd import open_workbook
from data_structs import Crossing, Incident

import resource

def getTable():
    print 'Reading DBF...'
    dbf = openDBFTable('../gcispubl.DBF')
    print 'Reading XLS...'
    xls_ls = openXLSFiles('../IncidentData')
    #csv = openCSVTable('../MasterGradeCrossingFile.csv')
    print 'Merging Tables...'
    mergedTable = mergeXLSTables(dbf, xls_ls)
    
    return mergedTable

def openDBFTable(dbfName):
    table = dbf.Table(dbfName)
    return table


def openXLSFiles(xlsDIR):
    ret_ls = list()

    for filename in os.listdir(xlsDIR):
        if filename != '.' or filename != '..':
            ret_ls.append(xlsDIR + '/' + filename)

    print ret_ls
    return ret_ls


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
            if i > 0:
                if j < len(key_list):
                    ret_l.append([key_list[j], field])
            j += 1
        i += 1
    
    return ret_l

def getXLSValues(xls):
    ret_l = list()

    book = open_workbook(xls, on_demand=True)
    sheet = book.sheet_by_index(0)

    for x in xrange(0, sheet.nrows):
        j = 0
        for col in sheet.row(x):
            ret_l.append([sheet.cell_value(rowx=0, colx = j), sheet.cell_value(rowx=x, colx=j)])
            j += 1

    return ret_l

def getKeyList(csvF):
    ret_l = list()
    for row in csvF:
        for field in row:
            ret_l.append(field)
        break

    return ret_l


def mergeTables(dbfT, xls_ls):

    crossingls = dict()
    incils = list()

    #Iterate over rows of dbf
    for record in dbfT:
        cross = Crossing()
        cross.set_values(record)
        crossingls[record.crossing] = cross

    for csv in csv_ls:
        #Fill out the list of keys for the csv file
        keyls = getKeyList(csv)

        #For each row, create an incident object
        rowCount = 0
        for row in csv:
            if rowCount > 0:

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


def mergeXLSTables(dbfT, xls_ls):
    crossing_dict = dict()
    inci_ls = list()

    dbfT.open()
    
    for x in xrange(0, len(dbfT)):
        y = dbfT[x]
        crossing_dict[y.crossing] = Crossing(y.crossing, dbfT)
        print x

    for xls in xls_ls:
        book = open_workbook(xls, on_demand=True)
        sheet = book.sheet_by_index(0)

        for x in xrange(1, sheet.nrows):
            j = 0
            inci = Incident()

            for col in sheet.row(x):
                inci.add_keyvalue(sheet.cell_value(rowx=0, colx=j), sheet.cell_value(rowx=x, colx=j))
                j += 1

            inci_ls.append(inci)

        for incident in inci_ls:
            if incident.get_value('GXID') in crossing_dict:
                crs = crossing_dict[incident.get_value('GXID')]
                crs_ls = crs.get_inci()

                if crs_ls is not None:
                    crs_ls.append(incident)

    return [crossing_dict, inci_ls]

def getInciDict(xls_ls):
    inci_dic = dict()

    for xls in xls_ls:
        book = open_workbook(xls, on_demand=True)
        sheet = book.sheet_by_index(0)

        for x in xrange(1, sheet.nrows):
            j = 0
            inci = Incident()

            for col in sheet.row(x):
                inci.add_keyvalue(sheet.cell_value(rowx=0, colx=j), sheet.cell_value(rowx=x, colx=j))
                j += 1


            key = inci.get_value('GXID')

            if key not in inci_dic:
                inci_dic[key] = list()

            inci_dic[key].append(inci)



    return inci_dic 



#getTable()
