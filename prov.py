import re

file_name = 'clean_data_2016.csv'
out = 'prov2016.csv' 

with open(file_name,'r') as in_file, open(out,'w') as out_file:
    ind = 0
    first = True
    for line in in_file:
        if first:
            out_file.write(line)
            first = False
            continue
        line = [x.lower() for x in line.split(',')]       
        if "providence" in line[0]:
            if ind < 10:
                print(line)
                ind = ind + 1
            l = line[0].split()
            for i in range(len(l)):
                if l[i] == 'north' or l[i] == 'east':
                    if l[i + 1] == 'providence':
                        break
                if l[i] == 'providence':
                    out_file.write(','.join(line))
