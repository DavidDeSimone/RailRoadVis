import networkx as nx
import data_parser as dp
import graph_form as gf
import json
import os

def main():
    total_ls = dp.getTable()
    crossing_dic = total_ls[0]
    crossing_dic_sorted = gf.sortDict(crossing_dic)

    for crossing in reversed(ls):
        Gc = nx.Graph()
        Gc.graph['crossing'] = value

        inci_ls = crossing.get_inci()
        for inci in inci_ls:
            inci_dic = inci.get_dict()

            try:
                for key, value in inci_dic.iteritems():
                    if Gc.has_node(unicode(key + ':' + value)):
                        Gc[unicode(key + ':' + value)]['val'] += 1
                    else:
                        Gc[unicode(key + ':' + value)]['val'] = 1
            except UnicodeError:
                x = 1
        gf.printGr(Gc, str(crossing.get_value('crossing')) + '.json', 'crossings/' + str(crossing.get_value('crossing') + '/'))


if __name__=="__main__":
    main()