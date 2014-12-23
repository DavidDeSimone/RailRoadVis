import data_parser as dp
import operator
import sys

def main():
    print 'Reading Table....'

    total_ls = dp.getTable()

    print 'Table Read....'

    while(True):
        print 'Enter Query...'
        query = raw_input()
        execute(total_ls, query)

def execute(table, query_str):
    if(query_str == ''):
        return

    tokens = query_str.split()
    command = tokens[0]

    if(command == 'printcr'):
        printcr(table, tokens[1])
    elif(command == 'printcrs'):
        for x in xrange(1, len(tokens)):
            printcr(table, tokens[x])
    elif(command == 'compcrs'):
        compcrs(table, tokens[1], tokens[2])
    elif(command == 'highest'):
        highest(table, tokens[1], tokens[2])
    elif(command == 'lowest'):
        lowest(table, tokens[1], tokens[2])
    elif(command == 'lsa'):
        print_inci_st(table)
    elif(command == 'iprint'):
        print_cooc(table, tokens[1])
    elif(command == 'across'):
        comp_across(table, tokens[1])
    elif(command == 'common'):
        common(table, tokens[1:])
    elif(command == 'attr'):
        print_crs_attr(table, tokens[1:])
    elif(command == 'q'):
        'Quitting...'
        sys.exit()
    else:
        print 'Command not found!'


#Prints the information profile for a crossing
def printcr(table, crossingID):
    crossing_ls = table[0]

    if crossingID in crossing_ls:
        print crossing_ls[crossingID].get_values()
    else:
        print 'Entry not found!'
        
#Prints two crossings side by side
def compcrs(table, crossingOne, crossingTwo, diff=True):
    crossing_ls = table[0]

    for field_name in crossing_ls[crossingOne].get_values().field_names:
        color = '\033[94m'
        if diff == True and str(crossing_ls[crossingOne].get_values()[field_name]) != str(crossing_ls[crossingTwo].get_values()[field_name]):
            color = '\033[92m' 

        print color + field_name + ' | ' + crossingOne + ' : '+ str(crossing_ls[crossingOne].get_values()[field_name]) + " ::: " + crossingTwo + ' : ' + str(crossing_ls[crossingTwo].get_values()[field_name])
        
#Prints sorted crossing list with key values appended
def print_crs_attr(table, key_ls, sorter=0):
    crossing_dic = table[0]

    mark_ls = list()

    for crossing in crossing_dic.values():
        value_ls = list()
        for key in key_ls:
            value = crossing.get_value(key) 
            value_ls.append([key, value])
        mark_ls.append([crossing, value_ls])

    sorted_ls = sorted(mark_ls, key=lambda item: len(item[0].get_inci()))

    for item in sorted_ls:
        sys.stdout.write('Crossing ' + str(item[0].get_values()['crossing']) + ' : (Ival)' + str(len(item[0].get_inci())))
        for sub_item in item[1]:
            sys.stdout.write(' ::: ' + str(sub_item[0]) + ' : ' + str(sub_item[1]))
        
        sys.stdout.write('\n')


#Pritns cooccurnece list for a crossing
def print_cooc(table, crossing_str, print_t=True):
    crossing_dic = table[0]
    crossing = crossing_dic[crossing_str]

    inci_ls = crossing.get_inci()
    
    final_dic = dict()

    for inci in inci_ls:
        inci_dic = inci.get_dict()
        
        for i_key, i_value in inci_dic.iteritems():
            item = str(i_key) + " ::: " +  str(i_value)
            if item in final_dic:
                final_dic[item] += 1
            else:
                final_dic[item] = 1

    sorted_ls = sorted(final_dic.items(), key=operator.itemgetter(1))
    for item in sorted_ls:
        if print_t == True:
            print item

    return sorted_ls

#Prints the common elements of a group of crossings
def common(table, examine_ls):
    crossing_dic = table[0]
    
    current_dic = dict()

    for field_name in crossing_dic[examine_ls[0]].get_values().field_names:
        current_dic[field_name] = crossing_dic[examine_ls[0]].get_values()[field_name]


    for x in xrange(1, len(examine_ls)):
        curr_cross = examine_ls[x]
        
        for field_name in crossing_dic[curr_cross].get_values().field_names:
            if field_name in current_dic:
                if current_dic[field_name] != crossing_dic[curr_cross].get_values()[field_name]:
                    del current_dic[field_name]
    

    for key, value in current_dic.iteritems():
        print '\033[92m' + str(key) + ' ::: ' + str(value)


    return current_dic


#Compares co-occurnece of indicents across crossings
def comp_across(table, key_str):
    crossing_dic = table[0]
    crossing_ls = crossing_dic.values()
    
    ls = list()

    for crossing in crossing_ls:
        incv_ls = print_cooc(table, crossing.get_value('crossing'), False)
        for item in incv_ls:
            items = item[0].split()
            if(items[0] == key_str):
                ls.append([item, crossing.get_value('crossing')])


    sorted_ls = sorted(ls, key=lambda item: item[0][1])
    for lsi in sorted_ls:
        print str(lsi[0]) + ' || ' + str(lsi[1])


#Prints crossing list sorted by number of incidents
def print_inci_st(table):
    crossing_dic = table[0]
    ls = crossing_dic.values()

    sorted_dic = sorted(ls, key=lambda item: len(item.get_inci()), reverse=False)

    for value in sorted_dic:
        inci_ls = value.get_inci()
        print 'Incident at ' + str(value.get_value('crossing')) + ' with num: ' + str(len(inci_ls))


if __name__=="__main__":
    main()
