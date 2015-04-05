import networkx as nx 
import data_parser as dp 
import json
from networkx.readwrite import json_graph
import os
import sys
import xlwt
from multiprocessing import Process, Lock, Value

#Used for writing to local directory
local = './crossings/'

#Global Spreadsheet variables
CURRENT_ROW = 1

LOWER_BOUND = 6
UPPER_BOUND = 32

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

	#Command multi_all will generate all graphs within range
	#with multi-core optimizations
	if(sys.argv[1] == 'multi_all'):
		multi_all()
		return

	#Command multi_export will export the statistic spreadsheet
	#of all graphs within range with multi-core optimization
	if(sys.argv[1] == 'multi_export'):
		multi_export()
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

	if num_incidents < LOWER_BOUND or num_incidents > UPPER_BOUND:
		return None, 0, None

	#print 'Number of incidents for crossing ' + str(ID) + ' is ' + str(len(inci_ls))

	#convert this crossing to a python dictionary
	crossing_dict = getCrossingDict(dbfT, ID)

	#For each co-occuring key value pair, form an edge and 
	#incriment the co-occurnece of that pair
	##TODO fix possibility of unicode error on casts to strings in the below segment
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

def printJSON(graph, ID):
	if graph is None:
		return

	write_t = open(local + ID + '.json', 'w')

	data = json_graph.node_link_data(graph)
	write_t.write(json.dumps(data))
	write_t.close()

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


def multi_export():
	lock = Lock()
	book, sh = initalize_export()
	CURRENT_ROW = Value('i', 1)
	exportRange(0, 150000, book, sh, CURRENT_ROW, lock)
	#Process(target=exportRange, args=[0, 50000, book, sh, CURRENT_ROW, lock]).start()
	#Process(target=exportRange, args=[50001, 100000, book, sh, CURRENT_ROW, lock]).start()
	#Process(target=exportRange, args=[100001, 150000, book, sh, CURRENT_ROW, lock]).start()
	#Process(target=exportRange, args=[150001, 199999, book, sh, CURRENT_ROW, lock]).start()

def initalize_export():
	book = xlwt.Workbook()
	sh = book.add_sheet('sheet1')

	sh.write(0, 0, "crossID")
	sh.write(0, 1, "num_incidents")
	sh.write(0, 2, "star co_occurrence")
	sh.write(0, 3, "star 1")
	sh.write(0, 4, "star 2")
	sh.write(0, 5, "outliers_roots")
	sh.write(0, 6, "outlier_children")
	sh.write(0, 7, "num_outlier_roots")
	sh.write(0, 8, "num_children")

	return book, sh

def exportRange(min_value, max_value, book, sh, CURRENT_ROW, lock):
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	dbfT.open()

	for x in xrange(min_value, max_value):
		crossing = dbfT[x]
		ID = unicode(crossing.crossing)
		graph, num_incidents, ID = construct(ID, dbfT, inci_dic)
		if graph is not None:
			write_to_sheet(graph, num_incidents, ID, book, sh, CURRENT_ROW, lock)

def write_to_sheet(graph, num_incidents, ID, book, sh, CURRENT_ROW, lock):
	item = gen_list([graph, num_incidents, ID])
		
	lock.acquire()
	print 'Lock acquired'
	for y in xrange(0, len(item)):
		sh.write(CURRENT_ROW.value, y, item[y])	

	print CURRENT_ROW.value
	CURRENT_ROW.value += 1
	print 'Saving sheet..'
	book.save('exportSheet_m.xls')
	print 'lock released'
	lock.release()


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
	ret_list.append(num_incidents)

	#Find the maximum spanning tree of the graph
	MST = nx.minimum_spanning_tree(graph, 'value')

	nodes = graph.nodes(data=True)
	star1 = None
	star2 = None

	nodes_ls = sorted(nodes, key=lambda item: MST.degree(item[0]), reverse=True)
	star1 = nodes_ls[0]
	star2 = nodes_ls[1]
	
	print star1[0]
	print star2[0]
	

	if graph.has_edge(star1[0], star2[0]):
		edge = graph.edge[star1[0]][star2[0]]['value']
		ret_list.append(edge)
	elif graph.has_edge(star2[0], star1[0]):
		edge = graph.edge[star2[0]][star1[0]]['value']
		ret_list.append(edge)
	else:
		ret_list.append(0)

	outlier_parents = list()
	outlier_list = list()
	for node in nodes:
		if node[0] not in nx.neighbors(MST, star1[0]):
			if node[1]['isInci'] != star1[1]['isInci']:
				outlier_list.append(node)
				if nx.neighbors(MST, node[0])[0] not in outlier_parents:
					outlier_parents.append(nx.neighbors(MST, node[0])[0])
		if node[0] not in nx.neighbors(MST, star2[0]):
			if node[1]['isInci'] != star2[1]['isInci']:
				outlier_list.append(node)
				if nx.neighbors(MST, node[0])[0] not in outlier_parents:
					outlier_parents.append(nx.neighbors(MST, node[0])[0])

	ret_list.append(star1[1]['label'])
	ret_list.append(star2[1]['label'])

	
	stn = ""
	for out in outlier_parents:
		stn += "||" + out

	strt = ""
	for out in outlier_list:
		strt += "||" + out[1]['label']

	ret_list.append(stn)
	ret_list.append(strt)
	ret_list.append(len(outlier_parents))
	ret_list.append(len(outlier_list))

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

def multi_all():
	Process(target=printSubSet, args=[0, 50000]).start()
	Process(target=printSubSet, args=[50001, 100000]).start()
	Process(target=printSubSet, args=[100001, 150000]).start()
	Process(target=printSubSet, args=[150001, 199999]).start()

def printSubSet(lower, upper):
	dbfT = dp.openDBFTable('../gcispubl.DBF')
	inci_dic = dp.getInciDict(dp.openXLSFiles('../IncidentData'))

	dbfT.open()

	graph_ls = list()

	for x in xrange(lower, upper):
		crossing = dbfT[x]
		ID = unicode(crossing.crossing)
		graph, num_incidents, ID = construct(ID, dbfT, inci_dic)
		if graph is not None:
			printJSON(graph, ID + '(' + unicode(num_incidents) + ')')


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
