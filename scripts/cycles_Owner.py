# -*- coding: utf-8 -*-
import networkx as nx
import csv

DIR_CSV = '../data/csv/'
DIR_TXT = '../data/txt/'
DIR_GRAPHS = '../graphs/'

SUFFIX = 'owner'
CSV_INDEX = 12

INPUT   = DIR_CSV + 'incidents_clean.csv'
OUTPUT  = DIR_TXT + 'cycles_'+SUFFIX+'.txt'
GEXF    = DIR_GRAPHS + 'cycles_'+SUFFIX+'.gexf'
GRAPHML = DIR_GRAPHS + 'cycles_'+SUFFIX+'.graphml'
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

  
g = None
g_all = nx.MultiDiGraph()
current_process_id = None
current_function = None
number_of_processes = 0

fo = open(OUTPUT, "wb")

with open(INPUT, 'rb') as f:
  reader = csv.reader(f, delimiter=";")
  reader.next() # suppresses the header line
  for row in reader:
    process_id = row[0]
    function = row[CSV_INDEX].decode('utf-8')
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
      
nx.write_gexf(g_all, GEXF)
nx.write_graphml(g_all, GRAPHML)