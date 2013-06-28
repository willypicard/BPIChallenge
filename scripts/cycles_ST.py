# -*- coding: utf-8 -*-
import networkx as nx
import csv

DIR_CSV = '../data/csv/'
DIR_TXT = '../data/txt/'
DIR_GRAPHS = '../graphs/'

INPUT   = DIR_CSV + "incidents_clean.csv"
OUTPUT  = DIR_TXT + "cycles_ST.txt"
GEXF    = DIR_GRAPHS + "cycles_ST.gexf"
GRAPHML = DIR_GRAPHS + "cycles_ST.graphml"
DEBUG_CYCLES = False
# [0] process instance
#[12] ST

def write_to_file(fo, process_id, cycles):   
  fo.write(process_id)
  fo.write('\n')
  for cycle in cycles:
    fo.write(", ".join(ST.encode('utf-8') for ST in cycle))
    # for ST in cycle:
      # fo.write(ST.encode('utf-8').strip());
      # fo.write(", ")
    fo.write('\n')
  fo.write('\n')

  
g = None
g_all = nx.MultiDiGraph()
current_process_id = None
current_ST = None
number_of_processes = 0

fo = open(OUTPUT, "wb")

with open(INPUT, 'rb') as f:
  reader = csv.reader(f, delimiter=";")
  reader.next() # suppresses the header line
  for row in reader:
    process_id = row[0]
    ST = row[6].decode('utf-8')
    product = row[9].decode('utf-8')
    process_id = process_id+" "+product
    if process_id == current_process_id:
      if ST != current_ST:
        g.add_edge(current_ST, ST)
        current_ST = ST
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
      g.add_node(ST)
      current_process_id = process_id
      current_ST = ST
      number_of_processes += 1
fo.close()    
      
nx.write_gexf(g_all, GEXF)
nx.write_graphml(g_all, GRAPHML)