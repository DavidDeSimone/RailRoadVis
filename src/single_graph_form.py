import networkx as nx 
import data_parser as dp 
import json
from networkx.readwrite import json_graph
import os
import sys

#Used for writing to local directory
local = './crossings/'

#Template for node dictionary for JSON
nodeTemplate = {'x' : 1, 'y': 1, 'r': 4, 'id': -1, 'color': 'green', 'label': 'nop', 'visible': True, 'pinned': False, 'shape': 'square', 'type': 'node' }

#Template for edge dictionary for JSON
edgeTemplate = {'value': 1, 'visible': True, 'type': 'link', 'value': 0}

def main():
	
	if len(sys.argv) == 0:
		print 'Error, invalid number of command line args'
		return

	if sys.argv[1] == 'ls':
		printCrossings()
		return

	if sys.argv[1] == 'all':
		printAll(sys.argv[2])
		return

	#Open Relevant Files
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	#construct graphs for relevant files
	for index in xrange(1, len(sys.argv)):
		ID = unicode(sys.argv[index])
		graph = construct(ID, dbfT, inci_dic)
		printJSON(graph, ID)

def construct(ID, dbfT, inci_dic, threshold=0):
	G = nx.Graph()
	dbfT.open()

	if ID not in inci_dic:
		#print 'Crossing does not have any incidents'
		return None, 0

	#Find the incident list for this crossing
	inci_ls = inci_dic[ID]
	num_incidents = len(inci_ls)

	print 'Comparing ' + str(num_incidents) + ' < ' + str(threshold)
	print num_incidents < 4
	if num_incidents < 4:
		print 'Returning'
		return None, 0

	print 'Number of incidents for crossing ' + str(ID) + ' is ' + str(len(inci_ls))

	#convert this crossing to a python dictionary
	crossing_dict = getCrossingDict(dbfT, ID)


	#For each co-occuring key value pair, form an edge and 
	#incriment the co-occurnece of that pair
	idLabel = 0
	for inci in inci_ls:
		for c_key_t, c_value_t in crossing_dict.iteritems():
			
			c_key = str(c_key_t)
			c_value = str(c_value_t)

			crossingKey = c_key + ':' + c_value


			if not G.has_node(crossingKey):
				G.add_node(crossingKey)
				G.node[crossingKey]['x'] = 1
				G.node[crossingKey]['y'] = 1
				G.node[crossingKey]['r'] = 4
				#G.node[crossingKey]['id'] = idLabel
				G.node[crossingKey]['color'] = 'orange'
				G.node[crossingKey]['label'] = crossingKey
				G.node[crossingKey]['visible'] = True
				G.node[crossingKey]['pinned'] = False
				G.node[crossingKey]['shape'] = 'cross'
				G.node[crossingKey]['type'] = 'node'

				idLabel += 1


			inci_dict = inci.get_dict()

			for i_key_t, i_value_t in inci_dict.iteritems():
				i_key = str(i_key_t)
				i_value = str(i_value_t)

				inciKey = i_key + ':' + i_value

				if not G.has_node(inciKey):
					G.add_node(inciKey)
					G.node[inciKey]['x'] = 1
					G.node[inciKey]['y'] = 1
					G.node[inciKey]['r'] = 4
					#G.node[inciKey]['id'] = idLabel
					G.node[inciKey]['color'] = 'blue'
					G.node[inciKey]['label'] = inciKey
					G.node[inciKey]['visible'] = True
					G.node[inciKey]['pinned'] = False
					G.node[inciKey]['shape'] = 'circle'
					G.node[inciKey]['type'] = 'node'

					idLabel += 1



				try:
					if G.has_edge(crossingKey, inciKey):
						G.edge[crossingKey][inciKey]['value'] += 1
					else:
						G.add_edge(crossingKey, inciKey, edgeTemplate)
						G.edge[crossingKey][inciKey]['value'] = 1
						G.edge[crossingKey][inciKey]['visible'] = True
						G.edge[crossingKey][inciKey]['color'] = "green"
						G.edge[crossingKey][inciKey]['type'] = 'link'
				except UnicodeDecodeError:
					print 'Unicode Error'



	#dbfT.close()
	return G, num_incidents



g_file = open('full_list.json', 'a')
def printJSON(graph, ID):
	if graph is None:
		return

	write_t = open(local + ID + '.json', 'w')

	data = json_graph.node_link_data(graph)
	write_t.write(json.dumps(data))
	write_t.close()

	g_file.write(ID + '.json')



def getCrossingDict(dbfT, ID):
	ret_dict = dict()

	for record in dbfT:
		if record.crossing == ID:
			for field_name in dbfT.field_names:
				ret_dict[field_name] = record[field_name]
		
	return ret_dict

def printCrossings():
	print "Crossing List:"
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	dbfT.open()

	for crossing in dbfT:
		print crossing.crossing

def printAll(threshold):
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	dbfT.open()

	graph_ls = list()

	for crossing in dbfT:
		ID = unicode(crossing.crossing)
		graph, num_incidents = construct(ID, dbfT, inci_dic, threshold)
		printJSON(graph, ID + '(' + unicode(num_incidents) + ')')

if __name__=="__main__":
	main()