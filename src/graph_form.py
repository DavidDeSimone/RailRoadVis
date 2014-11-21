import networkx as nx
import data_parser as dp
import json
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import os

IGNORE = ['NARR4', 'NARR2', 'NARR3', 'NARR1', 'combtxt', 'VIDEOT']

def main():
    G = nx.Graph()
    
    totalls = dp.getTable()
    dbfT = dp.openDBFTable('../gcispubl.DBF')
    csvT = dp.openCSVTable('../MasterGradeCrossingFile.csv')

    print 'Opening DBF Value list...'

    #Create a node for each value of each field in the DBF
    #dbf_values_list = dp.getDBFValues(dbfT)
    
    print 'List Opened'

    #for entry in dbf_values_list:
    #    if entry is not None:
            #Retreive the field name (entry[0]) and the possible value (entry[1])
    #        G.add_node(str(entry[0]) + ':' + str(entry[1]) + ':cross')

    print 'DBF Nodes added'

    print 'Opening CSV Values'
    
    #Create a node for each value of each field in the CSV
    #csv_values_list = dp.getCSVValues(csvT)

    print 'CSV Values read'

    #for entry in csv_values_list:
    #    if entry is not None:
    #        G.add_node(str(entry[0]) + ':' + str(entry[1]) + ':inci')

    print 'CSV Nodes Added'

    #Iterate over the crossings
    #iterate over the incidents in the crossing
    #Increase the weight of any crossing:incident value pair you see

    #Remove edges of weight 0
    print 'Adding Edges'

    #Get the list of crossings
    crossls = totalls[0]

    #For each crossing
    counter = 0

    #Number of non-incident holding crossings we examine
    THRESHOLD = 3000

    #Minimum number of incidents needed for print to console
    INCI_T = 2

    #Variable to determine if sorted output list should be called
    SORT = True


    ls = sortDict(crossls)
    printls(ls)
        

    #for key, value in crossls.iteritems():
    for value in reversed(ls):
        Gp = nx.Graph()
        Gp.graph['crossing'] = value
 
        cross_d = value.get_dict(dbfT)
        incils = value.get_inci()

        if incils != []:
            counter += 1
            #print 'Examining Crossing ' + str(cross_d['crossing'])

        if len(incils) > INCI_T:
            print 'Multi Incidident at ' + str(cross_d['crossing']) + ' with num : ' + str(len(incils))

        for inci in incils:
            for c_key, c_value in cross_d.iteritems():
                
                #Get the Incident dictionary
                inci_d = inci.get_dict()

                #If the graph already has edge
                for i_key, i_value in inci_d.iteritems():
                    try:
                       if Gp.has_edge(unicode(c_key) + unicode(':') + unicode(c_value) + unicode(':cross'),unicode(i_key) + unicode(':') + unicode(i_value) + unicode(':inci')):
                        #print 'Adding Weight'
                           Gp[unicode(c_key) + unicode(':') + unicode(c_value) + unicode(':cross')][unicode(i_key) + unicode(':') + unicode(i_value) + unicode(':inci')]['weight'] += 1 #Increase weight by 1
                       else:
                        #Else add edge to graph
                           Gp.add_edge(unicode(c_key) + unicode(':') + unicode(c_value) + unicode(':cross'), unicode(i_key) + unicode(':') + unicode(i_value) + unicode(':inci'), {'weight':1})
                            #Gp[unicode(c_key) + unicode(':') + unicode(c_value) + unicode(':cross')]['isCrossing'] = True
                            #Gp[unicode(i_key) + unicode(':') + unicode(i_value) + unicode(':inci')]['isCrossing'] = False
                    except UnicodeDecodeError:
                            #print c_key
                            #print c_value
                            #print i_key
                            #print i_value
                        x = 1

                        #Work around until the narratives are properly added
                        #data = json_graph.node_link_data(G)
                        #write_t = open('f_out.json', 'w')
                        #write_t.write(json.dumps(data))
                        #write_t.close()
                        #return

        
        #G = nx.union(G, Gp)
        if len(Gp.nodes()) > 1:
            printGr(Gp, str(value.get_value('crossing')) + '.json', 'crossings/' + str(value.get_value('crossing') + '/'), True)
        
        if counter > THRESHOLD:
            break
                
    #nx.draw_spectral(G)
    #plt.show()
    print 'Graph Formed'
    print len(G.nodes())
    print len(G.edges())

    printGr(G, 'output.json')


def printGr(G, filename, path='.', meta_info=False):
    if not os.path.exists(path):
        os.makedirs(path)

    if meta_info is True:
        printMeta(G, filename, path)

    write_t = open(path + filename, 'w')

    #Remove Meta information for now
    G.graph['crossing'] = None
    data = json_graph.node_link_data(G)
    write_t.write(json.dumps(data))
    write_t.close()

def printMeta(G, filename, path='.'):
    write_t = open(path + filename + '.info', 'w')

    node_num = len(G.nodes())
    edge_num = len(G.edges())
    #print 'Node num ' + str(node_num)
    #print 'Edge num ' + str(edge_num)
    crossing = G.graph['crossing']

    write_t.write('Number of Vertices ' + str(node_num) + '\n')
    write_t.write('Number of Edges ' + str(edge_num) + '\n')

    if edge_num != 0:
        write_t.write('Average Degree ' + str( (2 * edge_num) / node_num) + '\n')
    else:
        write_t.write('No Edges present, so no average degree!')
    
    inci_ls = crossing.get_inci()
    write_t.write('Incident List:')
    
    count = 0
    for inci in inci_ls:

        if(count == (len(inci_ls) - 1)):
            write_t.write(str(inci.get_value('INCDTNO')) + ';')
        else:
            write_t.write(str(inci.get_value('INCDTNO')) + ',')
        count += 1

    write_t.write('\n')
    

    crossingCnt = 0
    for n in G.nodes():
        ln = n.split(':')
        if ln[2] == 'cross':
            crossingCnt += 1
    
    write_t.write('Number of Crossing Vertices ' + str(crossingCnt) + '\n')
    write_t.write('Number of Incident Vertices ' + str(node_num - crossingCnt) + '\n')
    #print 'Number of Crossing Vertices ' + str(crossingCnt)
    #print 'Number of Inci vertices ' + str(node_num - crossingCnt)
    
    write_t.close()

    #appendMaster(filename, path)

#def appendMaster(filename, path='.'):

def sortDict(dic, sort_values=False, key='.', reverse_t=False):
    ls = dic.values()

    sorted_ls = sorted(ls, key=lambda item: len(item.get_inci()), reverse=reverse_t)

    return sorted_ls

def printls(ls):
    if len(ls) == 0:
        print 'List is empty!'
        return

    for item in ls:
        print 'Crossing ' + item.get_value('crossing') + ': ' + str(len(item.get_inci()))


if __name__=="__main__":
    main()
