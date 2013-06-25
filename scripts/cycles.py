# -*- coding: utf-8 -*-
import networkx as nx
import csv

INPUT   = "incidents_clean.csv"
OUTPUT  = "cycles.txt"
GEXF    = "cycles.gexf"
GRAPHML = "cycles.graphml"
DEBUG_CYCLES = False
# [0] process instance
#[12] owner

def write_to_file(fo, process_id, cycles):   
  fo.write(process_id)
  fo.write('\n')
  for cycle in cycles:
    fo.write(", ".join(owner.encode('utf-8') for owner in cycle))
    # for owner in cycle:
      # fo.write(owner.encode('utf-8').strip());
      # fo.write(", ")
    fo.write('\n')
  fo.write('\n')

  
g = None
g_all = nx.MultiDiGraph()
current_process_id = None
current_owner = None
number_of_processes = 0

fo = open(OUTPUT, "wb")

with open(INPUT, 'rb') as f:
  reader = csv.reader(f, delimiter=";")
  reader.next() # suppresses the header line
  for row in reader:
    process_id = row[0]
    owner = row[12].decode('utf-8')
    if process_id == current_process_id:
      if owner != current_owner:
        g.add_edge(current_owner, owner)
        current_owner = owner
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
      g.add_node(owner)
      current_process_id = process_id
      current_owner = owner
      number_of_processes += 1
fo.close()    
      
nx.write_gexf(g_all, GEXF)
nx.write_graphml(g_all, GRAPHML)