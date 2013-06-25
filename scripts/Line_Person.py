import csv

#[0] = person
#[2] = line

FILE = 'raw_ST_lines.csv'
FILE_OUTPUT = "matrix_Line_Person.txt"

def read_dist():      
  nodes_on_edges = dict()
  nodes_names = []
  with open(FILE, 'rb') as f:
    reader = csv.reader(f, delimiter=";")
    reader.next() # suppresses the header line
    for row in reader:
      edge = row[0]
      node = row[2]
      if edge in nodes_on_edges.keys():
        if node not in nodes_on_edges[edge]:
          nodes_on_edges[edge].append(node)
      else:
        nodes_on_edges[edge] = [node]
      if node not in nodes_names:
        nodes_names.append(node)
  return nodes_on_edges, nodes_names
  

def indexes_list(sub_list, list):
  indexes = []
  for item in sub_list:
    indexes.append(list.index(item))
  return indexes

def create_empty_matrix(node_names):
  stats=list()
  number_of_edges = len(node_names)
  for i in range(number_of_edges):
    stats.append([0]*number_of_edges)
  return stats

def create_matrix(data, node_names):
  stats = create_empty_matrix(node_names)
  for edge in data:
    nodes = data[edge]
    indexes = indexes_list(nodes, node_names)
    index = indexes[0]
    if len(indexes) == 1:
      stats[index][index] += 1
    else:
      for i in range(len(indexes)-1):
        for j in range(i+1, len(indexes)):
          stats[indexes[i]][indexes[j]] += 1
          stats[indexes[j]][indexes[i]] += 1
  return stats

def write_to_file(node_names, stats):   
  fo = open(FILE_OUTPUT, "wb")
  fo.write(str(node_names))
  fo.write(',\n')
  for i in stats:
    fo.write( str(i));
    fo.write(',\n')
  fo.close()    

  
ST_in_lines, lines_names = read_dist()
stats = create_matrix(ST_in_lines, lines_names)
write_to_file(lines_names, stats)

print "lines_names", lines_names
print ''
for s in stats:
  print s

  

    