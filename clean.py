file_name = '2016m.csv'
out = 'clean_data_2016.csv'

with open(file_name,'r') as in_file, open(out,'w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    p = 0
    for line in in_file:
        line = ','.join(line.split(',')[1:])
        if p < 2:
            print(line)
            p = p + 1
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)
