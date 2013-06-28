# -*- coding: utf-8 -*-
import networkx as nx
import csv
import operator

DIR_CSV = '../data/csv/'
DIR_TXT = '../data/txt/'
DIR_GRAPHS = '../graphs/'

suffix = 'owner'
csv_index = 12

source = 'incidents'

def get_CSV_input(source):
  return DIR_CSV + source

def get_cycles_txt(suffix):
  return DIR_TXT + 'cycles_'+source+"_"+suffix+'.txt'

def get_cycles_count_txt(suffix):
  return DIR_TXT + 'cycles_'+source+"_"+suffix+'_count.txt'

def get_cycles_count_by_product_txt(suffix):
  return DIR_TXT + 'cycles_'+source+"_"+suffix+'_count_by_product.txt'


def get_gexf_file(suffix):
  return DIR_GRAPHS + 'cycles_'+source+"_"+suffix+'.gexf'

def get_graphml_file(suffix):
  return DIR_GRAPHS + 'cycles_'+source+"_"+suffix+'.graphml'

DEBUG_CYCLES = False
# [0] process instance
#[12] function

def write_to_file(fo, process_id, cycles):   
  fo.write(process_id)
  fo.write('\n')
  for cycle in cycles:
    fo.write(", ".join(function.encode('utf-8') for function in cycle))
    # for function in cycle:
      # fo.write(function.encode('utf-8').strip());
      # fo.write(", ")
    fo.write('\n')
  fo.write('\n')

def generate_graph(source, suffix, csv_index):
  g = None
  g_all = nx.MultiDiGraph()
  current_process_id = None
  current_function = None
  number_of_processes = 0

  fo = open(get_cycles_txt(suffix), "wb")

  with open(get_CSV_input(source), 'rb') as f:
    reader = csv.reader(f, delimiter=";")
    reader.next() # suppresses the header line
    for row in reader:
      process_id = row[0]
      function = row[csv_index].decode('utf-8')
      if not function.strip() or function == 'Uknown':
        continue
      product = row[9].decode('utf-8')
      process_id = process_id+" "+product
      if process_id == current_process_id:
        if function != current_function:
          g.add_edge(current_function, function)
          current_function = function
      else:
        if g != None:
          cycles = nx.simple_cycles(g)
          if len(cycles) > 0:
            for cycle in cycles:
              g_all.add_cycle(cycle)
            write_to_file(fo, current_process_id, cycles)
            if DEBUG_CYCLES:
              print current_process_id, cycles
        g = nx.DiGraph()
        g.add_node(function)
        current_process_id = process_id
        current_function = function
        number_of_processes += 1
  fo.close()    
        
  nx.write_gexf(g_all, get_gexf_file(suffix))
  nx.write_graphml(g_all, get_graphml_file(suffix))


def count_cycles(suffix):

  cycles = {}
  with open(get_cycles_txt(suffix), 'r') as infile:
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
  f = open(get_cycles_count_txt(suffix), 'w')
  for cycle in cycles:
    if not cycle[0].strip():
      continue
    f.write(str(cycle[1]))
    f.write(';')
    f.write(str(cycle[0]))
    
  f.close()


def count_cycles_by_product(suffix):
  OUTPUT = '../data/txt/cycles_ST_count_by_product.txt'

  all_cycles = {}
  with open(get_cycles_txt(suffix), 'r') as infile:
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

  f = open(get_cycles_count_by_product_txt(suffix), 'w')

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

sources = {'incidents':'incidents_clean.csv', 'problems_open':'problems_open-cleaned.csv', 'problems_closed':'problems_closed-cleaned.csv'}

params = [('owner',12), ('ST', 6), ('Func', 4), ('org', 5)]

for my_source in sources:
  source = my_source
  for param in params:
    generate_graph(sources[source], param[0], param[1])
    count_cycles(param[0])
    count_cycles_by_product(param[0])