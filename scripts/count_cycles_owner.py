import operator

FILE = '../data/txt/cycles.txt'
OUTPUT = '../data/txt/cycles_count.txt'

cycles = {}
with open(FILE, 'r') as infile:
	for line in infile:
		if len(line) == 0:
			continue
		if line[0] == '1':
			continue
		if line in cycles:
			cycles[line] +=1
		else:
			cycles[line] = 1

cycles = sorted(cycles.iteritems(), key=operator.itemgetter(1), reverse = True)
f = open(OUTPUT, 'w')
for cycle in cycles:
	if not cycle[0].strip():
		continue
	f.write(str(cycle[1]))
	f.write(';')
	f.write(str(cycle[0]))
#	f.write('\n')
	
f.close()