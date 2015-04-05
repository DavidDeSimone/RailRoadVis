
import os

file_t = open('complete_list.json', 'a')
file_t.write('[')
for json in os.listdir('./crossings'):
	if json != '.' and json != '..':
		file_t.write('"' + json + '",\n')

file_t.write(']\n')
file_t.close()