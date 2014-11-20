from xlrd import open_workbook

#Rows we are intered in comparing
inrows = [3, 7, 14, 18]

inlist = []


wb = open_workbook('../grade_crossing_ex.xlsx')

#Iterate over spreadsheet, form interesting row as an array
#Add row arrays to container array
for s in wb.sheets():
    for row in inrows:
        tmplist = []
        for col in xrange(s.ncols):
            tmplist.append(s.cell(row,col).value)
        inlist.append(tmplist)

#print JSON object for graph view
f = open('ex_out.json', 'w')

#print vertices for the graph
f.write('{\n')
f.write('"nodes":\n')
f.write('\t[\n')

hacklist = list()

i = 0
j = 0
for x in inlist:
    for y in xrange(0, len(x)):
        f.write('{"name":"' + str(i) + '","value":"' + str(x[y]) + '","itemnum":' + str(j) + ',"attrn":' + str(y) + '},\n')
        toadd = list()
        toadd.append(str(i))
        toadd.append(str(x[y]))
        toadd.append(str(j))
        toadd.append(str(y))
        hacklist.append(toadd)
        i += 1
    j += 1

f.write('],\n')
f.write('"links":[\n')

for obj1 in hacklist:
    for obj2 in hacklist:
        if obj1[2] == '2' and obj2[2] == '4':
            if obj1[1] == obj2[1] and obj1[1] != '':
                if obj1[3] == obj2[3] and obj1[3] != '':
                   f.write('{"source":' + obj1[0] + ',"target":' + obj2[0] + '},\n')
        if obj1[2] == '0' and obj2[2] == '3':
            if obj1[1] == obj2[1] and obj1[1] != '':
                   if obj1[3] == obj2[3] and obj1[3] != '':
                      f.write('{"source":' + obj1[0] + ',"target":' + obj2[0] + '},\n')


f.write('\t]\n')
f.write('}\n')

