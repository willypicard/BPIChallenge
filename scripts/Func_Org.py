import csv



FILE = 'func_org_line.csv'
FILE_OUTPUT = 'Func_org_matrix.txt'

func_in_org = dict()
orgs = []
 
number_of_records = 0 

with open(FILE, 'rb') as f:
  reader = csv.reader(f, delimiter=";")
  reader.next() # suppresses the header line
  for row in reader:
    number_of_records += 1
    func = row[0]
    org = row[1]
    if len(func)==0 :
      func = "unset"
      continue
    if len(org)==0 :
      org = "unset"
    if func in func_in_org.keys():
      if org not in func_in_org[func]:
        func_in_org[func].append(org)
    else:
      func_in_org[func] = [org]
    if org not in orgs:
      orgs.append(org)

#print func_in_org

print ''
print ''
print ''

print "Found", str(number_of_records), "records"
print func_in_org
print ''
print ''
print ''

number_of_orgs = len(orgs)
stats=list()
for i in range(number_of_orgs):
  stats.append([0]*number_of_orgs)
  
#print stats

def indexes_list(sub_list, list):
  indexes = []
  for item in sub_list:
    indexes.append(list.index(item))
  return indexes
  
for func in func_in_org:
  func_orgs = func_in_org[func]
  indexes = indexes_list(func_orgs, orgs)
  print "Function:", func
  print "Orgs:", func_orgs
  print "indexes=", indexes
  print
  index = orgs.index(func_orgs[0])
#  print func_orgs[0], "@", index, "in", orgs
#  print func_orgs[0], index,"in", orgs
  if len(func_orgs) == 1:
    stats[index][index] += 1
  else:
    for i in range(len(func_orgs)-1):
      for j in range(i+1, len(func_orgs)):
        stats[indexes[i]][indexes[j]] += 1
        stats[indexes[j]][indexes[i]] += 1

  if len(func_orgs) == 0:
    print "Found 0 orgs for ", func

fo = open(FILE_OUTPUT, "wb")
for i in stats:
  fo.write( str(i));
  fo.write(',\n')
fo.close()    

print
print
print
print orgs
print

for s in stats:
  print s
    
