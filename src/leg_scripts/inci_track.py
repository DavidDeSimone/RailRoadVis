import csv
import dbf

class report:
    def __init__(self, crossing):
        self.crossing = crossing
        self.incilist = []

    def append_inci(self, inci):
        self.incilist.append(inci)


def main():
    table = dbf.Table('../gcispubl.DBF')

    tabledict = set()

    for record in table:
        to_add = report(record)
        tabledict.add(to_add)

    incis = csv.open('inci.csv', 'rb')
    for row in incis:
        print row
    


if __name__ == "__main__":
    main()
