#Compiles statistics on given numerical distribution 
def comp_stats(stat_distro, print_s=False, crossing_d=None, inci_d=None):
    stat_dic = dict()

    if crossing_d is not None and inci_d is not None:
        validation(stat_distro, crossing_d, inci_d, verbose=True)

    mean, median, mode = compute_basic(stat_distro)
    stat_dic['MEAN'] = mean
    stat_dic['MEDIAN'] = median
    stat_dic['MODE'] = mode

    if print_s:
        printstats(stat_dic)


def compute_basic(stat_distro):
    return None, None, None

def validation(stat_distro, crossing_d, inci_d, verbose=False):
    if verbose:
        print size_check(stat_distro, inci_d)
        print crossing_sum(stat_distro, crossing_d)


def size_check(stat_distro, inci_d):
    if len(stat_distro) != len(inci_d):
        to_print = 'Number of entries in stat distrobution incorrect:\n Size of stat Distro: ' + str(len(stat_distro)) + '\nSize of Incident List' + str(len(inci_d))
    else:
        to_print = 'Number of incidents matches size of stat distribution'

    return to_print

def crossing_sum(stat_distro, crossing_d):
    sdsum = sum(stat_distro)
    cssum = 0
    
    for key, value in crossing_d.iteritems():
        crossing_t = value
        inci_ls = crossing_t.get_inci()

        cssum += len(inci_ls)

    if sdsum != cssum:
        to_print = 'Sums not equal, ' + str(sdsum) + ':' + cssum
    else:
        to_print = 'Stat Distribution and Crossing List agree'

    return to_print

#Prints the contents of a dictionary with relevant statistical information
def printstats(stat_dic):
    for key, value in stat_dic.iteritems():
        print str(key) + '- ' + str(value)
