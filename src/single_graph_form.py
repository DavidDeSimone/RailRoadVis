import networkx as nx 
import data_parser as dp 
import json
from networkx.readwrite import json_graph
import os
import sys
import xlwt

#Used for writing to local directory
local = './crossings/'

THRESH = 7

def main():
	
	if len(sys.argv) == 0:
		print 'Error, invalid number of command line args'
		return


	#exports degree distro in spreadsheet
	if sys.argv[1] == 'print_inci_dist':
		printInciDistro()
		return

	#exports data into spreadsheet format
	if sys.argv[1] == 'export_all':
		exportAll()
		return

	#Command 'ls', list all of the current crossings
	if sys.argv[1] == 'ls':
		printCrossings()
		return

	#Command 'all', print the graphs for all crossings
	if sys.argv[1] == 'all':
		printAll(sys.argv[2])
		return

	#Open Relevant Files
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	#construct graphs for relevant files
	for index in xrange(1, len(sys.argv)):
		ID = unicode(sys.argv[index])
		graph, num_incidents, ID = construct(ID, dbfT, inci_dic)
		if graph is not None:
			printJSON(graph, ID)

def construct(ID, dbfT, inci_dic, threshold=0):
	G = nx.Graph()
	dbfT.open()

	if ID not in inci_dic:
		#print 'Crossing does not have any incidents'
		return None, 0, None

	#Find the incident list for this crossing
	inci_ls = inci_dic[ID]
	num_incidents = len(inci_ls)

	if num_incidents < THRESH:
		print 'Returning'
		return None, 0, None

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
				G.node[crossingKey]['isInci'] = False
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
					G.node[inciKey]['isInci'] = True
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
						G.add_edge(crossingKey, inciKey)
						G.edge[crossingKey][inciKey]['value'] = 1
						G.edge[crossingKey][inciKey]['visible'] = True
						G.edge[crossingKey][inciKey]['color'] = "green"
						G.edge[crossingKey][inciKey]['type'] = 'link'
				except UnicodeDecodeError:
					print 'Unicode Error'



	#dbfT.close()
	return G, num_incidents, ID

g_file = open('full_list.json', 'a')
g_file.write("[")
def printJSON(graph, ID):
	if graph is None:
		return

	write_t = open(local + ID + '.json', 'w')

	data = json_graph.node_link_data(graph)
	write_t.write(json.dumps(data))
	write_t.close()

	g_file.write('"' + ID + '.json",\n')



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

def exportAll():
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	dbfT.open()

	graph_ls = list()

	for crossing in dbfT:
		ID = unicode(crossing.crossing)
		graph, num_incidents, ID = construct(ID, dbfT, inci_dic)
		if graph is not None:
			graph_ls.append([graph, num_incidents, ID])

	conv_spread_sheet(graph_ls)

#TODO move this to another file
def conv_spread_sheet(graph_pairs):
	filename = 'exportSheet.xls'

	book = xlwt.Workbook()
	sh = book.add_sheet('sheet1')

	num_cols = 6

	sh.write(0, 0, "crossID")
	sh.write(0, 1, "num_incidents")
	sh.write(0, 2, "star 1")
	sh.write(0, 3, "star 2")
	sh.write(0, 4, "outliers")
	sh.write(0, 5, "num_outliers")

	output_list = list()

	for pair in graph_pairs:
		item = gen_list(pair)
		output_list.append(item)

	for x in xrange(0, len(output_list)):
		item = output_list[x]
		for y in xrange(0, num_cols):
			sh.write(x + 1, y, output_list[x][y])

	book.save(filename)	

#Generates a list in the following form
#[crossingID, num_incidents, star1, star2, outliers, num_outliers]
def gen_list(pair):
	ret_list = list()
	graph = pair[0]
	num_incidents = pair[1]
	ID = pair[2]

	ret_list.append(str(ID))
	ret_list.append(str(num_incidents))

	#Find the maximum spanning tree of the graph
	MST = nx.minimum_spanning_tree(graph, 'value')

	nodes = graph.nodes(data=True)
	star1 = nodes[0]
	star2 = nodes[0]
	for node in nodes:
		if MST.degree(node[0]) >= MST.degree(star1[0]):
			star2 = star1
			star1 = node
		elif MST.degree(node[0]) >= MST.degree(star2[0]):
			star2 = node

	outlier_list = list()
	for node in nodes:
		neighbors = nx.neighbors(MST, node[0])
		print neighbors
		if star1[1]['isInci']:
			if node[1]['isInci'] is False and star1[0] not in neighbors:
				outlier_list.append(node)
		else: #else star1 is not an incident node 
			if node[1]['isInci'] and star1[0] not in neighbors:
				outlier_list.append(node)
		if star2[1]['isInci']:
			if node[1]['isInci'] is False and star2[0] not in neighbors:
				outlier_list.append(node)
		else: #star2 is not an incident node
			if node[1]['isInci'] and star2[0] not in neighbors:
				outlier_list.append(node)

	ret_list.append(star1[1]['label'])
	ret_list.append(star2[1]['label'])

	strt = ""
	for out in outlier_list:
		strt += "||" + out[1]['label']

	ret_list.append(strt)
	ret_list.append(str(len(outlier_list)))
	return ret_list



def printInciDistro():
	filename = 'inci_distro.xls'

	book = xlwt.Workbook()
	sh = book.add_sheet('sheet1', cell_overwrite_ok=True)

	num_cols = 2

	sh.write(0, 0, "inci_degree")
	sh.write(0, 1, "freq")

	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	dbfT.open()

	tmp_dict = dict()

	for x in xrange(0, 37):
		tmp_dict[x] = 0

	for record in dbfT:
		if record.crossing not in inci_dic:
			if 0 not in tmp_dict:
				tmp_dict[0] = 1
			else:
				tmp_dict[0] += 1

			sh.write(1, 0, 0)
			sh.write(1, 1, tmp_dict[0])

		else:
			inci_ls = inci_dic[unicode(record.crossing)]
			num_inci = len(inci_ls)
			if num_inci not in tmp_dict:
				tmp_dict[num_inci] = 1
			else:
				tmp_dict[num_inci] += 1

			sh.write(num_inci + 1, 0, num_inci)
			sh.write(num_inci + 1, 1, tmp_dict[num_inci])


	#saving....
	book.save(filename)

def printAll(threshold):
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	dbfT.open()

	graph_ls = list()

	for crossing in dbfT:
		ID = unicode(crossing.crossing)
		graph, num_incidents, ID = construct(ID, dbfT, inci_dic, threshold)
		if graph is not None:
			printJSON(graph, ID + '(' + unicode(num_incidents) + ')')

if __name__=="__main__":
	main()