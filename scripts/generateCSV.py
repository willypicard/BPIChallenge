import csv

FILE = 'raw_ST_lines.csv'

ST_in_lines = dict()
  
with open(FILE, 'rb') as f:
  reader = csv.reader(f, delimiter=";")
  reader.next() # suppresses the header line
  for row in reader:
    if row[0] in ST_in_lines.keys():
      ST_in_lines[row[0]].append(row[1])
      print "found multiple lines for", row[0]
    else:
      ST_in_lines[row[0]] = [row[1]]

print ST_in_lines

print ''
print ''
print ''

line_numbers= {"1st":0, "2nd":1, "3rd":2, "2nd 3rd":3}

stats = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]
         
for st in ST_in_lines:
  lines = ST_in_lines[st]
  index = line_numbers[lines[0]]
  if len(lines) > 1:
    print st, lines
    index1 = line_numbers[lines[1]]
    stats[index][index1] += 1
    stats[index1][index] += 1
    print lines, index, index1
  if len(lines) == 1:
    print lines, index
    stats[index][index] += 1
    
for s in stats:
  print s
    
