import csv

FILE = 'raw_ST_lines.csv'

STs = dict()
  
with open(FILE, 'rb') as f:
  reader = csv.reader(f, delimiter=";")
  reader.next() # suppresses the header line
  for row in reader:
    owner = row[0]
    ST = row[1]
    line = row[2]
 #   if ST == 'V13':
#      print ST, line
 #     print "ST in STs=", ST in STs
 #     if ST in STs:
 #       print "STs[ST]=", STs[ST]
 #       print "line not in STs[ST]", line not in STs[ST]
 #       print
    if ST in STs:
      if line not in STs[ST]:
        STs[ST].append(str(line))
    else:
      STs[ST] = [line]

for ST in STs:
  if len(STs[ST]) > 1:
    print ST, STs[ST]
    
print "========================"
print "========================"
print "========================"

for ST in STs:
  if ST == 'V13':
    print ST, STs[ST]

one = "1st"
two = "2nd"
three = "3rd"

STs_1_2 = []
STs_1_3 = []
STs_2_3 = []
STs_others = []
for ST in STs:
  lines = STs[ST]
  if len(lines) < 2:
    continue
  if lines[0] == one:
    if lines[1] == two:
      STs_1_2.append(ST)
    elif lines[1] == three:
      STs_1_3.append(ST)
    else:
      STs_others.append(ST)
  elif lines[0] == two:
    if lines[1] == one:
      STs_1_2.append(ST)
    elif lines[1] == three:
      STs_2_3.append(ST)
    else:
      STs_others.append(ST)
  elif lines[0] == three:
    if lines[1] == one:
      STs_1_3.append(ST)
    elif lines[1] == two:
      STs_2_3.append(ST)
    else:
      STs_others.append(ST)
  else:
      STs_others.append(ST)
  
print "=========================="
print "======= 1st-2nd =========="
print STs_1_2
print

print "=========================="
print "======= 2nd-3rd =========="
print STs_2_3
print

print "=========================="
print "======= 1st-3rd =========="
print STs_1_3
print

print "=========================="
print "======= others ==========="
print STs_others
print


    