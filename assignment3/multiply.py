import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    matrix,row,col,val = record
    if matrix == 'a':
    	key=col
    else key = row
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: trimmed DNA seq
    # values: sequence IDs
    for record in list_of_values:
    
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
