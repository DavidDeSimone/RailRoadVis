import networkx as nx
import data_parser as dp
import json
from networkx.readwrite import json_graph
import matplotlib

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
    THRESHOLD = 5
    for key, value in crossls.iteritems():
        cross_d = value.get_dict(dbfT)
        incils = value.get_inci()
        
        
        if incils != []:
            counter += 1
        for inci in incils:
            for c_key, c_value in cross_d.iteritems():
                inci_d = inci.get_dict()
                for i_key, i_value in inci_d.iteritems():
                    try:
                        G.add_edge(unicode(c_key) + unicode(':') + unicode(c_value) + unicode(':cross'), unicode(i_key) + unicode(':') + unicode(i_value) + unicode(':inci'))
                    except UnicodeDecodeError:
                        print c_key
                        print c_value
                        print i_key
                        print i_value
                        
                        #Work around until the narratives are properly added
                        #data = json_graph.node_link_data(G)
                        #write_t = open('f_out.json', 'w')
                        #write_t.write(json.dumps(data))
                        #write_t.close()
                        return

        if counter > THRESHOLD:
            break


    nx.draw(G)
    print 'Graph Formed'
    print len(G.nodes())
    print len(G.edges())

    write_t = open('full_out.json', 'w')
    data = json_graph.node_link_data(G)
    write_t.write(json.dumps(data))
    write_t.close()



if __name__=="__main__":
    main()
