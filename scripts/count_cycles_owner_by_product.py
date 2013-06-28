import operator

FILE = '../data/txt/cycles_owner.txt'
OUTPUT = '../data/txt/cycles_owner_count_by_product.txt'

all_cycles = {}
with open(FILE, 'r') as infile:
	current_product = None
	for line in infile:
		if len(line) == 0 or line[0] == ' ':
			continue
		if line[0] == '1':
			current_product = line[line.index(' ')+1:-1]
			continue
		if current_product not in all_cycles:
			product_cycles = {}
			all_cycles[current_product] = product_cycles
		product_cycles = all_cycles[current_product]
		if line in product_cycles:
			product_cycles[line] +=1
		else:
			product_cycles[line] = 1


f = open(OUTPUT, 'w')

for product in all_cycles:
	cycles = all_cycles[product]
	cycles = sorted(cycles.iteritems(), key=operator.itemgetter(1), reverse=True)
	f.write(str(product)+" - "+str(len(cycles)))
	f.write('\n')
	for cycle in cycles:
		if not cycle[0].strip():
			continue
		f.write(str(cycle[1]))
		f.write(';')
		f.write(str(cycle[0]))
	f.write('\n')
	
f.close()