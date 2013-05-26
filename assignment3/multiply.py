import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line
a_nrow = 5
a_ncol = 5
b_nrow = 5
b_ncol = 5
#assert(a_ncol = b_nrow

def mapper(record):
    # key: document identifier
    # value: document contents
    matrix,row,col,val = record
    if matrix == 'a':
		for k in xrange(b_ncol):
			mr.emit_intermediate((row,k),record)
    elif matrix == 'b':
    	for i in xrange(a_nrow):
    		mr.emit_intermediate((i,col),record)
    else: raise Exception('invalid matrix')

def reducer(key, list_of_values):
    # key: (i,k)
    # values: full record
    a_vals = [i for i in list_of_values if i[0] == 'a']
    a_vals.sort(key=lambda x: x[2])
    b_vals = [i for i in list_of_values if i[0] == 'b']
    b_vals.sort(key=lambda x: x[1])
    total = 0
    while len(a_vals) > 0:
    	a = a_vals.pop()
    	j = a[2]
    	while b_vals[-1][1] > j:
    		b_vals.pop()
    	if b_vals[-1][1] == j:
    		b = b_vals.pop()
    		total+=a[-1]*b[-1]
    	else: continue
    mr.emit((key[0],key[1],total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
